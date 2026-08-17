#!/usr/bin/env python3
"""Publish an approved weekly radio draft.

The human-facing source is a Markdown draft. This script is the explicit
approval gate between the draft and public site publication.

Commands:
  approve --episode NN
  publish --episode NN --confirm [--wait 120]
  verify --episode NN
  show
"""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Iterable

try:
    import yaml
except ImportError as exc:  # pragma: no cover - environment guard
    raise SystemExit("PyYAML is required: python3 -m pip install pyyaml") from exc


ROOT = Path(__file__).resolve().parents[2]
RADIO_DIR = ROOT / "quartz/static/radio"
EPISODES_PATH = RADIO_DIR / "episodes.json"
SCRIPT_DIR = ROOT / "scripts/ep02-voice-proofs"
DEFAULT_STATE_DIR = Path.home() / ".hermes/cron/radio-state"
VOXCPM = Path.home() / ".venvs/voxcpm2/bin/voxcpm"
# 이로 한국어 고정 앵커 (2026-08-17 사용자 승인 D 음색).
# EP03~04에 쓰던 iro_stiff_test/variant_B 앵커는 어두운 톤(presence -31dB)이라
# EP04에서 대사 렌더가 전체적으로 둥글게(탁하게) 나온 원인이 되어 교체했다.
IRO_KO_PROMPT_AUDIO = SCRIPT_DIR / "iro_anchor_v2/output_001.wav"
# 이로 한국어 prompt-text: VoxCPM2 batch에서 이 텍스트가 오디오로 출력되지 않도록
# 대본에 등장하지 않는 짧은 문장을 사용해야 한다 (EP03 대사를 사용하면
# 해당 대사가 렌더 결과에 누출됨: voxcpm batch 버그).
# 아래 문장은 iro_anchor_v2/output_001.wav에 실제로 들어 있는 문장이다.
IRO_KO_PROMPT_TEXT = "오늘도 소식 하나하나를 같이 짚어 보면 좋겠네요. 그럼 바로 시작해 볼까요?"
LANGS = ("ko", "en", "ja")
SPEAKERS = ("iro", "loop")

IRO_CONTROLS = {
    "en": (
        "A friendly English-speaking woman in her late twenties. "
        "Warm, casual, chatty — like talking to a coworker over coffee. "
        "Her voice goes up and down with genuine interest. "
        "Relaxed, informal, spontaneous. NOT a news anchor. "
        "A natural, expressive person having fun talking."
    ),
    "ja": (
        "A friendly Japanese woman in her late twenties. "
        "Warm, casual, chatty — like talking to a coworker over coffee. "
        "Her voice goes up and down with genuine interest. "
        "Relaxed, informal, spontaneous. NOT a news anchor. "
        "A natural, expressive person having fun talking."
    ),
}
LOOP_CONTROLS = {
    "ko": (
        "A natural Korean male voice, mid thirties, warm and engaged in conversation. "
        "Not a news anchor — more like a knowledgeable friend explaining something "
        "with genuine enthusiasm. Relaxed, personable, occasionally pauses to think. "
        "Close mic, clean recording. Conversational, not robotic."
    ),
    "en": (
        "A natural English male voice, mid thirties, warm and engaged. "
        "Not a news anchor — a knowledgeable friend explaining something with genuine enthusiasm. "
        "Relaxed, personable. Close mic, clean recording."
    ),
    "ja": (
        "A natural Japanese male voice, mid thirties, warm and engaged. "
        "Not a news anchor — a knowledgeable friend explaining something with genuine enthusiasm. "
        "Relaxed, personable. Close mic, clean recording."
    ),
}

FORBIDDEN_KO = (
    "신호",
    "의미하는 바는",
    "패턴입니다",
    "선행되어야",
    "핵심 키워드",
    "전체적인 흐름",
    "가능하게 된다",
)


class PipelineError(RuntimeError):
    pass


def iso_now() -> str:
    return dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")


def run_cmd(
    args: list[str],
    *,
    cwd: Path | None = None,
    timeout: int = 600,
    capture: bool = True,
) -> subprocess.CompletedProcess[str]:
    try:
        result = subprocess.run(
            args,
            cwd=str(cwd) if cwd else None,
            capture_output=capture,
            text=True,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise PipelineError(f"명령 실행 실패: {' '.join(args)}: {exc}") from exc
    if result.returncode != 0:
        stderr = (result.stderr or result.stdout or "").strip()
        if len(stderr) > 1500:
            stderr = stderr[-1500:]
        raise PipelineError(f"명령 실패({result.returncode}): {' '.join(args)}\n{stderr}")
    return result


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise PipelineError(f"파일이 없습니다: {path}") from exc
    except json.JSONDecodeError as exc:
        raise PipelineError(f"JSON 파싱 실패: {path}: {exc}") from exc


def write_text_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def write_json_atomic(path: Path, data: Any) -> None:
    write_text_atomic(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def episodes_data() -> dict[str, Any]:
    data = load_json(EPISODES_PATH)
    if not isinstance(data.get("episodes"), list):
        raise PipelineError("episodes.json의 episodes가 배열이 아닙니다")
    latest = data.get("latest")
    if not isinstance(latest, int):
        raise PipelineError("episodes.json의 latest가 정수가 아닙니다")
    return data


def latest_episode(data: dict[str, Any]) -> int:
    nums: list[int] = []
    for ep in data["episodes"]:
        if isinstance(ep, dict) and isinstance(ep.get("num"), int):
            nums.append(ep["num"])
    if not nums:
        return int(data["latest"])
    actual = max(nums)
    if actual != data["latest"]:
        raise PipelineError(f"episodes.json drift: latest={data['latest']} 실제 최대 번호={actual}")
    return actual


def extract_frontmatter(text: str) -> tuple[dict[str, Any], str, str]:
    match = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n?(.*)\Z", text, re.S)
    if not match:
        raise PipelineError("draft.md에 YAML frontmatter가 없습니다")
    raw = match.group(1)
    try:
        frontmatter = yaml.safe_load(raw) or {}
    except yaml.YAMLError as exc:
        raise PipelineError(f"draft.md frontmatter 파싱 실패: {exc}") from exc
    if not isinstance(frontmatter, dict):
        raise PipelineError("draft.md frontmatter가 객체가 아닙니다")
    return frontmatter, raw, match.group(2)


def parse_dialogues(body: str) -> dict[str, list[dict[str, str]]]:
    result: dict[str, list[dict[str, str]]] = {lang: [] for lang in LANGS}
    section_matches = list(re.finditer(r"(?m)^## Dialogue:\s*(ko|en|ja)\s*$", body))
    for index, section_match in enumerate(section_matches):
        lang = section_match.group(1)
        end = section_matches[index + 1].start() if index + 1 < len(section_matches) else len(body)
        section_body = body[section_match.end() : end]
        headers = list(
            re.finditer(
                r"(?m)^###\s+(\d{3})\s+·\s+(iro|loop)\s+·\s+([a-z0-9-]+)\s*$",
                section_body,
            )
        )
        for header_index, header in enumerate(headers):
            text_end = headers[header_index + 1].start() if header_index + 1 < len(headers) else len(section_body)
            text = section_body[header.end() : text_end].strip()
            text = " ".join(line.strip() for line in text.splitlines() if line.strip())
            result[lang].append(
                {
                    "number": header.group(1),
                    "speaker": header.group(2),
                    "section": header.group(3),
                    "text": text,
                }
            )
    return result


def parse_open_source_links(body: str) -> list[dict[str, Any]]:
    """Parse the optional JSON block used for links shown under the player."""
    match = re.search(
        r"(?ims)^##\s+(?:Open[- ]source links|오픈소스 링크)\s*$\n(.*?)(?=^##\s+|\Z)",
        body,
    )
    if not match:
        return []
    block = re.search(r"```json\s*(.*?)```", match.group(1), re.S | re.I)
    if not block:
        return []
    try:
        value = json.loads(block.group(1).strip())
    except json.JSONDecodeError as exc:
        raise PipelineError(f"Open-source links JSON 파싱 실패: {exc}") from exc
    if not isinstance(value, list):
        raise PipelineError("Open-source links는 배열이어야 합니다")
    for index, entry in enumerate(value, start=1):
        if not isinstance(entry, dict):
            raise PipelineError(f"Open-source links {index}번 항목이 객체가 아닙니다")
        if not isinstance(entry.get("url"), str) or not re.match(r"^https?://", entry["url"]):
            raise PipelineError(f"Open-source links {index}번 URL이 올바르지 않습니다")
        if not entry.get("name") or not entry.get("description"):
            raise PipelineError(f"Open-source links {index}번 항목에 name/description이 없습니다")
    return value


def parse_draft(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise PipelineError(f"draft.md가 없습니다: {path}")
    text = path.read_text(encoding="utf-8")
    frontmatter, _, body = extract_frontmatter(text)
    frontmatter["_path"] = str(path)
    frontmatter["_dialogues"] = parse_dialogues(body)
    frontmatter["_open_source_links"] = parse_open_source_links(body)
    frontmatter["_body"] = body
    return frontmatter


def find_draft(episode: int | None, state_dir: Path) -> Path:
    if episode is not None:
        path = state_dir / f"draft-ep{episode:02d}.md"
        if not path.exists():
            raise PipelineError(f"초안이 없습니다: {path}")
        return path
    candidates = sorted(state_dir.glob("draft-ep*.md"))
    if not candidates:
        raise PipelineError(f"초안이 없습니다: {state_dir}")
    return candidates[-1]


def validate_draft(draft: dict[str, Any], latest: int) -> None:
    required = ("schema_version", "episode", "status", "date")
    missing = [key for key in required if key not in draft]
    if missing:
        raise PipelineError(f"draft frontmatter 필드 누락: {', '.join(missing)}")
    if draft["schema_version"] != 1:
        raise PipelineError(f"지원하지 않는 draft schema_version: {draft['schema_version']}")
    episode = draft["episode"]
    if not isinstance(episode, int):
        raise PipelineError("draft episode가 정수가 아닙니다")
    if draft["status"] in {"pushed", "published"}:
        if episode != latest:
            raise PipelineError(f"발행된 에피소드 번호 불일치: draft={episode}, latest={latest}")
    elif episode != latest + 1:
        raise PipelineError(f"에피소드 번호 불일치: draft={episode}, 예상={latest + 1}")
    if draft["status"] not in {"draft", "approved", "pushed", "published"}:
        raise PipelineError(f"알 수 없는 draft 상태: {draft['status']}")
    for prefix in ("title", "summary"):
        for lang in LANGS:
            key = f"{prefix}_{lang}"
            if not isinstance(draft.get(key), str) or not draft[key].strip():
                raise PipelineError(f"draft 필드 누락 또는 빈 값: {key}")
    dialogues = draft.get("_dialogues", {})
    for lang in LANGS:
        lines = dialogues.get(lang, [])
        if not 20 <= len(lines) <= 35:
            raise PipelineError(f"{lang} 대사 수가 범위를 벗어났습니다: {len(lines)} (허용 20~35)")
        seen_numbers: set[str] = set()
        for line in lines:
            if line["number"] in seen_numbers:
                raise PipelineError(f"{lang} 대사 번호 중복: {line['number']}")
            seen_numbers.add(line["number"])
            if not line["text"]:
                raise PipelineError(f"{lang} {line['number']} 대사가 비어 있습니다")
        if {line["speaker"] for line in lines} != set(SPEAKERS):
            raise PipelineError(f"{lang}에 iro와 loop 대사가 모두 필요합니다")
    sources = re.findall(r"\[[^\]]+\]\(https?://[^)]+\)", draft.get("_body", ""))
    if len(sources) < 3:
        raise PipelineError(f"Markdown Sources에 링크가 3개 미만입니다: {len(sources)}")
    ko_text = " ".join(line["text"] for line in dialogues["ko"])
    for forbidden in FORBIDDEN_KO:
        if forbidden in ko_text:
            raise PipelineError(f"한국어 대본 금지 표현 포함: {forbidden}")


def current_draft(state_dir: Path, episode: int | None = None) -> tuple[Path, dict[str, Any], dict[str, Any]]:
    path = find_draft(episode, state_dir)
    draft = parse_draft(path)
    data = episodes_data()
    latest = latest_episode(data)
    validate_draft(draft, latest)
    return path, draft, data


def replace_frontmatter_value(raw: str, key: str, value: str) -> str:
    pattern = re.compile(rf"(?m)^{re.escape(key)}:\s*.*$")
    replacement = f"{key}: {value}" if value else f"{key}:"
    updated, count = pattern.subn(replacement, raw, count=1)
    if count == 0:
        updated = raw.rstrip() + "\n" + replacement
    return updated


def update_draft_status(path: Path, status: str, *, timestamp_key: str) -> None:
    text = path.read_text(encoding="utf-8")
    frontmatter, raw, body = extract_frontmatter(text)
    updated_raw = replace_frontmatter_value(raw, "status", status)
    updated_raw = replace_frontmatter_value(updated_raw, timestamp_key, iso_now())
    write_text_atomic(path, f"---\n{updated_raw}\n---\n{body}")


def cmd_show(state_dir: Path) -> int:
    paths = sorted(state_dir.glob("draft-ep*.md"))
    if not paths:
        print(f"draft 없음: {state_dir}")
        return 0
    for path in paths:
        draft = parse_draft(path)
        print(f"EP {draft.get('episode')}: status={draft.get('status')} path={path}")
    return 0


def cmd_approve(episode: int | None, state_dir: Path) -> int:
    path, draft, data = current_draft(state_dir, episode)
    if draft["status"] != "draft":
        raise PipelineError(f"승인 가능한 상태가 아닙니다: {draft['status']}")
    update_draft_status(path, "approved", timestamp_key="approved_at")
    print(f"승인 상태 기록 완료: EP {draft['episode']} -> approved")
    print(path)
    return 0


def require_render_assets() -> None:
    required = [
        VOXCPM,
        IRO_KO_PROMPT_AUDIO,
        SCRIPT_DIR / "intro_sting.wav",
        SCRIPT_DIR / "transition.wav",
        SCRIPT_DIR / "outro_sting.wav",
        SCRIPT_DIR / "bg_music.wav",
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise PipelineError("렌더링 자산 누락:\n- " + "\n- ".join(missing))
    for binary in ("ffmpeg", "ffprobe"):
        if shutil.which(binary) is None:
            raise PipelineError(f"필수 명령을 찾을 수 없습니다: {binary}")


def generate_ref(lang: str, control: str, text: str, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    input_file = output_dir / "ref.txt"
    input_file.write_text(text, encoding="utf-8")
    run_cmd(
        [
            str(VOXCPM),
            "batch",
            "--input",
            str(input_file),
            "--output-dir",
            str(output_dir),
            "--control",
            control,
            "--cfg-value",
            "3.0",
            "--inference-timesteps",
            "30",
            "--normalize",
            "--denoise",
        ],
        timeout=600,
    )
    output = output_dir / "output_001.wav"
    if not output.exists():
        raise PipelineError(f"ref 음성 생성 결과가 없습니다: {output}")
    return output


def render_with_prompt(lines: list[dict[str, str]], prompt_audio: Path, prompt_text: str, output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    input_file = output_dir / "all_lines.txt"
    input_file.write_text("\n".join(line["text"] for line in lines), encoding="utf-8")
    run_cmd(
        [
            str(VOXCPM),
            "batch",
            "--input",
            str(input_file),
            "--output-dir",
            str(output_dir),
            "--prompt-audio",
            str(prompt_audio),
            "--prompt-text",
            prompt_text,
            "--cfg-value",
            "3.0",
            "--inference-timesteps",
            "30",
            "--normalize",
            "--denoise",
        ],
        timeout=3600,
    )
    outputs = sorted(output_dir.glob("output_*.wav"))
    if len(outputs) != len(lines):
        raise PipelineError(f"대사 음성 수 불일치: 예상={len(lines)}, 생성={len(outputs)} ({output_dir})")
    return outputs


def ffmpeg_to_wav(source: Path, destination: Path, *, loudnorm: bool = False) -> None:
    filters = ["loudnorm=I=-16:TP=-1.5:LRA=11"] if loudnorm else []
    args = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(source)]
    if filters:
        args += ["-af", filters[0]]
    args += ["-ar", "44100", "-ac", "1", "-c:a", "pcm_s16le", str(destination)]
    run_cmd(args, timeout=300)


def probe_duration(path: Path) -> float:
    result = run_cmd(
        [
            "ffprobe",
            "-v",
            "quiet",
            "-show_entries",
            "format=duration",
            "-of",
            "csv=p=0",
            str(path),
        ],
        timeout=60,
    )
    try:
        return float(result.stdout.strip())
    except ValueError as exc:
        raise PipelineError(f"오디오 duration을 읽을 수 없습니다: {path}: {result.stdout!r}") from exc


def assemble(segments: list[tuple[Path, str, str]], work_dir: Path, output_mp3: Path) -> float:
    work_dir.mkdir(parents=True, exist_ok=True)
    normalized: list[tuple[Path, str, str]] = []
    for index, (source, speaker, section) in enumerate(segments):
        destination = work_dir / f"seg_{index:03d}_{speaker}.wav"
        ffmpeg_to_wav(source, destination, loudnorm=True)
        normalized.append((destination, speaker, section))

    for name, duration in (("s1", 0.2), ("s2", 0.4), ("s3", 0.8), ("s4", 1.2)):
        run_cmd(
            [
                "ffmpeg",
                "-y",
                "-loglevel",
                "error",
                "-f",
                "lavfi",
                "-i",
                "anullsrc=channel_layout=mono:sample_rate=44100",
                "-t",
                str(duration),
                "-c:a",
                "pcm_s16le",
                str(work_dir / f"{name}.wav"),
            ],
            timeout=60,
        )

    intro = work_dir / "intro.wav"
    transition = work_dir / "transition.wav"
    outro = work_dir / "outro.wav"
    ffmpeg_to_wav(SCRIPT_DIR / "intro_sting.wav", intro)
    ffmpeg_to_wav(SCRIPT_DIR / "transition.wav", transition)
    ffmpeg_to_wav(SCRIPT_DIR / "outro_sting.wav", outro)

    entries = [f"file '{intro}'", f"file '{work_dir / 's3.wav'}'"]
    for index, (wav, speaker, section) in enumerate(normalized):
        entries.append(f"file '{wav}'")
        if index < len(normalized) - 1:
            _, next_speaker, next_section = normalized[index + 1]
            if section != next_section:
                entries.extend(
                    [
                        f"file '{work_dir / 's4.wav'}'",
                        f"file '{transition}'",
                        f"file '{work_dir / 's3.wav'}'",
                    ]
                )
            elif speaker != next_speaker:
                entries.append(f"file '{work_dir / 's2.wav'}'")
            else:
                entries.append(f"file '{work_dir / 's1.wav'}'")
    entries.extend([f"file '{work_dir / 's3.wav'}'", f"file '{outro}'"])
    concat_file = work_dir / "concat.txt"
    concat_file.write_text("\n".join(entries) + "\n", encoding="utf-8")

    raw = work_dir / "raw.wav"
    run_cmd(
        [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file),
            "-c",
            "copy",
            str(raw),
        ],
        timeout=300,
    )
    raw_duration = probe_duration(raw)
    if raw_duration < 60:
        raise PipelineError(f"완성 오디오가 너무 짧습니다: {raw_duration:.1f}s")

    output_mp3.parent.mkdir(parents=True, exist_ok=True)
    fade_start = max(0.0, raw_duration - 3.0)
    run_cmd(
        [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-i",
            str(raw),
            "-i",
            str(SCRIPT_DIR / "bg_music.wav"),
            "-filter_complex",
            (
                f"[1:a]volume=0.06,afade=t=in:st=0:d=2,"
                f"afade=t=out:st={fade_start:.1f}:d=3[bg];"
                "[0:a][bg]amix=inputs=2:duration=first:dropout_transition=0,"
                "loudnorm=I=-16:TP=-1.5:LRA=11"
            ),
            "-ar",
            "48000",
            "-ac",
            "1",
            "-b:a",
            "128k",
            str(output_mp3),
        ],
        timeout=300,
    )
    duration = probe_duration(output_mp3)
    if duration < 60 or output_mp3.stat().st_size < 10_000:
        raise PipelineError(f"최종 MP3 검증 실패: {output_mp3} ({duration:.1f}s, {output_mp3.stat().st_size} bytes)")
    return duration


def render_language(lang: str, lines: list[dict[str, str]], episode: int, work_dir: Path) -> tuple[Path, float]:
    iro_lines = [line for line in lines if line["speaker"] == "iro"]
    loop_lines = [line for line in lines if line["speaker"] == "loop"]
    lang_dir = work_dir / lang
    lang_dir.mkdir(parents=True, exist_ok=True)

    if lang == "ko":
        iro_prompt_audio = IRO_KO_PROMPT_AUDIO
        iro_prompt_text = IRO_KO_PROMPT_TEXT
    else:
        iro_prompt_audio = generate_ref(lang, IRO_CONTROLS[lang], iro_lines[0]["text"], lang_dir / "iro_ref")
        iro_prompt_text = iro_lines[0]["text"]
    iro_clips = render_with_prompt(iro_lines, iro_prompt_audio, iro_prompt_text, lang_dir / "iro_out")

    loop_prompt_audio: Path | None = None
    loop_prompt_text = ""
    if lang == "ko":
        # 루프 한국어도 이로처럼 고정 앵커를 쓴다 (EP02 승인 음색).
        # 매주 generate_ref로 새로 만들면 어두운 목소리가 무작위로 뽑혀
        # EP04에서 "탁하다"는 불만이 재발했다.
        loop_prompt_audio = SCRIPT_DIR / "loop_anchor_v2/output_001.wav"
        loop_prompt_text = (SCRIPT_DIR / "loop_anchor_v2/prompt_text.txt").read_text(encoding="utf-8").strip()
    loop_clips: list[Path] = []
    if loop_prompt_audio is not None:
        loop_clips = render_with_prompt(loop_lines, loop_prompt_audio, loop_prompt_text, lang_dir / "loop_out")
    else:
        loop_prompt_audio = generate_ref(lang, LOOP_CONTROLS[lang], loop_lines[0]["text"], lang_dir / "loop_ref")
        loop_clips = [loop_prompt_audio]
        if len(loop_lines) > 1:
            loop_clips.extend(
                render_with_prompt(loop_lines[1:], loop_prompt_audio, loop_lines[0]["text"], lang_dir / "loop_out")
            )

    segments: list[tuple[Path, str, str]] = []
    iro_index = 0
    loop_index = 0
    for line in lines:
        if line["speaker"] == "iro":
            source = iro_clips[iro_index]
            iro_index += 1
        else:
            source = loop_clips[loop_index]
            loop_index += 1
        segments.append((source, line["speaker"], line["section"]))

    output = work_dir / f"episode-{episode:02d}-{lang}.mp3"
    duration = assemble(segments, lang_dir / "assemble", output)
    return output, duration


def duration_label(seconds: float) -> str:
    minutes = seconds / 60
    if abs(minutes - round(minutes)) < 0.05:
        return f"~{int(round(minutes))}분"
    return f"~{minutes:.1f}분"


def episode_record(draft: dict[str, Any], episode: int, duration: float) -> dict[str, Any]:
    return {
        "num": episode,
        "title": {lang: draft[f"title_{lang}"] for lang in LANGS},
        "date": str(draft["date"]),
        "duration": duration_label(duration),
        "topics": {lang: [] for lang in LANGS},
        "summary": {lang: draft[f"summary_{lang}"] for lang in LANGS},
        "openSourceLinks": draft.get("_open_source_links", []),
        "audio": {lang: f"/static/radio/episode-{episode:02d}-{lang}.mp3" for lang in LANGS},
    }


def update_episodes(data: dict[str, Any], record: dict[str, Any]) -> dict[str, Any]:
    updated = copy.deepcopy(data)
    if any(ep.get("num") == record["num"] for ep in updated["episodes"]):
        raise PipelineError(f"episodes.json에 이미 존재하는 에피소드입니다: {record['num']}")
    updated["episodes"].append(record)
    updated["episodes"].sort(key=lambda ep: ep["num"])
    updated["latest"] = record["num"]
    return updated


def static_item(record: dict[str, Any], lang: str) -> str:
    language_label = {"ko": "한국어 · English · 日本語", "en": "Korean · English · Japanese", "ja": "韓国語 · English · 日本語"}[lang]
    title = html.escape(record["title"][lang])
    return (
        f'<div class="ewa-radio-archive-item is-active" data-ep="{record["num"]}" data-lang="{lang}">\n'
        f'<span class="ewa-radio-archive-num">EP {record["num"]:02d}</span>\n'
        f"<div>\n<h4>{title}</h4>\n"
        f'<span>{html.escape(record["date"])} · {html.escape(record["duration"])} · {language_label}</span>\n'
        "</div>\n</div>"
    )


def localized_metadata(value: Any, lang: str) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return str(value.get(lang) or value.get("ko") or value.get("en") or value.get("ja") or "")
    return ""


def static_links(record: dict[str, Any], lang: str) -> str:
    labels = {
        "ko": "방송에서 언급한 오픈소스·개발 프로젝트",
        "en": "Open-source projects mentioned",
        "ja": "番組で紹介したオープンソース・開発プロジェクト",
    }
    items = []
    for entry in record.get("openSourceLinks", []):
        url = html.escape(str(entry.get("url", "")), quote=True)
        name = html.escape(localized_metadata(entry.get("name"), lang))
        description = html.escape(localized_metadata(entry.get("description"), lang))
        if not url or not name:
            continue
        items.append(
            f'<li><a href="{url}" target="_blank" rel="noopener noreferrer">{name}</a>'
            f"<span>{description}</span></li>"
        )
    if not items:
        return '<div id="ep-links" class="ewa-radio-links" aria-live="polite" hidden></div>'
    return (
        '<div id="ep-links" class="ewa-radio-links" aria-live="polite">\n'
        f'<div class="ewa-radio-links-title">{labels[lang]}</div>\n'
        "<ul>\n" + "\n".join(items) + "\n</ul>\n</div>"
    )


def update_radio_page(path: Path, lang: str, record: dict[str, Any]) -> str:
    text = path.read_text(encoding="utf-8")
    num = record["num"]
    title = html.escape(record["title"][lang])
    summary = html.escape(record["summary"][lang])
    label = f"Episode {num} · {'Latest' if lang == 'en' else '최신 에피소드' if lang == 'ko' else '最新エピソード'}"

    replacements = [
        (r'(<span id="ep-num">)EP\s+\d+(</span>)', rf"\g<1>EP {num:02d}\g<2>"),
        (r'(<span class="ewa-radio-ep" id="ep-label">).*?(</span>)', rf"\g<1>{html.escape(label)}\g<2>"),
        (r'(<h2 id="ep-title">).*?(</h2>)', rf"\g<1>{title}\g<2>"),
        (r'(<p id="ep-summary">).*?(</p>)', rf"\g<1>{summary}\g<2>"),
        (r'(<span id="ep-date">).*?(</span>)', rf"\g<1>{html.escape(str(record['date']))}\g<2>"),
        (rf'(<source id="ep-source" src="/static/radio/)episode-\d+-{lang}(\.mp3")', rf"\g<1>episode-{num:02d}-{lang}\g<2>"),
        (r'(<div id="ep-links" class="ewa-radio-links"[^>]*>).*?</div>\n(</div>\n</section>)', static_links(record, lang) + r"\n\g<2>"),
    ]
    for pattern, replacement in replacements:
        text, count = re.subn(pattern, replacement, text, count=1, flags=re.S)
        if count != 1:
            raise PipelineError(f"라디오 fallback 갱신 위치를 찾지 못했습니다: {path} / {pattern}")

    archive_pattern = r'(<div class="ewa-radio-archive-list" id="ep-list">\n).*?(</div>\n</section>)'
    text, count = re.subn(
        archive_pattern,
        rf"\g<1>{static_item(record, lang)}\n\g<2>",
        text,
        count=1,
        flags=re.S,
    )
    if count != 1:
        raise PipelineError(f"라디오 archive fallback 갱신 위치를 찾지 못했습니다: {path}")
    return text


def git_status_paths() -> list[str]:
    result = run_cmd(["git", "status", "--porcelain=v1"], cwd=ROOT)
    paths: list[str] = []
    for line in result.stdout.splitlines():
        if not line:
            continue
        value = line[3:] if len(line) >= 4 else line
        if " -> " in value:
            value = value.split(" -> ", 1)[1]
        paths.append(value)
    return paths


def ensure_clean_repo() -> None:
    paths = git_status_paths()
    if paths:
        raise PipelineError("발행 전에 저장소가 깨끗해야 합니다. 현재 변경:\n- " + "\n- ".join(paths))


def restore_files(backups: dict[Path, bytes | None]) -> None:
    for path, content in backups.items():
        if content is None:
            if path.exists():
                path.unlink()
        else:
            path.write_bytes(content)


def public_url(path: str) -> str:
    return f"https://easyworking-ai.github.io{path}"


def http_probe(url: str, timeout: int = 20) -> tuple[int, bytes]:
    request = urllib.request.Request(url, headers={"User-Agent": "weekly-radio-pipeline/1"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return int(response.status), response.read()
    except urllib.error.HTTPError as exc:
        return int(exc.code), b""
    except urllib.error.URLError as exc:
        raise PipelineError(f"공개 URL 접속 실패: {url}: {exc}") from exc


def verify_public_episode(record: dict[str, Any], wait_seconds: int = 0) -> bool:
    deadline = time.time() + max(0, wait_seconds)
    last: list[str] = []
    while True:
        failures: list[str] = []
        status, body = http_probe(public_url("/static/radio/episodes.json"))
        if status != 200:
            failures.append(f"episodes.json HTTP {status}")
        else:
            try:
                remote = json.loads(body.decode("utf-8"))
                if remote.get("latest") != record["num"]:
                    failures.append(f"latest={remote.get('latest')} expected={record['num']}")
            except (UnicodeDecodeError, json.JSONDecodeError):
                failures.append("episodes.json JSON 파싱 실패")
        for lang, path in record["audio"].items():
            status, _ = http_probe(public_url(path))
            if status != 200:
                failures.append(f"{lang} MP3 HTTP {status}")
        if not failures:
            return True
        last = failures
        if time.time() >= deadline:
            print("공개 URL 검증 대기 실패: " + "; ".join(last), file=sys.stderr)
            return False
        time.sleep(min(15, max(1, int(deadline - time.time()))))


def cmd_verify(episode: int | None, state_dir: Path, wait_seconds: int) -> int:
    path, draft, data = current_draft(state_dir, episode)
    record = next((ep for ep in data["episodes"] if ep.get("num") == draft["episode"]), None)
    if record is None:
        raise PipelineError(f"episodes.json에 EP {draft['episode']}가 없습니다")
    for lang, audio_path in record["audio"].items():
        local = ROOT / "quartz" / audio_path.lstrip("/")
        if not local.exists():
            raise PipelineError(f"로컬 MP3가 없습니다: {local}")
        print(f"local {lang}: {local} {probe_duration(local):.1f}s {local.stat().st_size} bytes")
    ok = verify_public_episode(record, wait_seconds=wait_seconds)
    if ok:
        print(f"public: PASS EP {record['num']}")
        if draft["status"] == "pushed":
            update_draft_status(path, "published", timestamp_key="published_at")
    else:
        print(f"public: WAITING EP {record['num']}")
    return 0 if ok else 1


def cmd_publish(episode: int | None, state_dir: Path, confirm: bool, dry_run: bool, wait_seconds: int) -> int:
    path, draft, data = current_draft(state_dir, episode)
    if draft["status"] != "approved":
        raise PipelineError(f"발행 가능한 상태가 아닙니다: {draft['status']} (먼저 approve 실행)")
    if not dry_run and not confirm:
        raise PipelineError("실제 발행에는 --confirm이 필요합니다")
    require_render_assets()
    ensure_clean_repo()
    episode_number = int(draft["episode"])

    if dry_run:
        print(f"DRY RUN: EP {episode_number}")
        print(f"draft: {path}")
        print("render: ko, en, ja")
        print("update: episodes.json + 3 radio fallback pages + 3 MP3")
        print("build: npm run build:site")
        print("push: origin main")
        return 0

    backups: dict[Path, bytes | None] = {}
    public_targets = [
        RADIO_DIR / f"episode-{episode_number:02d}-{lang}.mp3" for lang in LANGS
    ] + [
        EPISODES_PATH,
        ROOT / "content/radio.md",
        ROOT / "content/en/radio.md",
        ROOT / "content/ja/radio.md",
    ]
    for target in public_targets:
        backups[target] = target.read_bytes() if target.exists() else None

    committed = False
    temp_root = Path(tempfile.mkdtemp(prefix=f"radio-ep{episode_number:02d}-", dir=str(ROOT / "scripts/radio-pipeline")))
    try:
        print(f"렌더링 시작: EP {episode_number}")
        rendered: dict[str, Path] = {}
        durations: dict[str, float] = {}
        for lang in LANGS:
            output, duration = render_language(lang, draft["_dialogues"][lang], episode_number, temp_root)
            rendered[lang] = output
            durations[lang] = duration
            print(f"  {lang}: {duration:.1f}s / {output.stat().st_size} bytes")

        duration = durations["ko"]
        record = episode_record(draft, episode_number, duration)
        for lang in LANGS:
            destination = RADIO_DIR / f"episode-{episode_number:02d}-{lang}.mp3"
            shutil.copy2(rendered[lang], destination)

        write_json_atomic(EPISODES_PATH, update_episodes(data, record))
        for lang, page_path in {
            "ko": ROOT / "content/radio.md",
            "en": ROOT / "content/en/radio.md",
            "ja": ROOT / "content/ja/radio.md",
        }.items():
            write_text_atomic(page_path, update_radio_page(page_path, lang, record))

        print("Quartz build 시작")
        run_cmd(["npm", "run", "build:site"], cwd=ROOT, timeout=900)
        allowed = {
            *(f"quartz/static/radio/episode-{episode_number:02d}-{lang}.mp3" for lang in LANGS),
            "quartz/static/radio/episodes.json",
            "content/radio.md",
            "content/en/radio.md",
            "content/ja/radio.md",
        }
        changed = set(git_status_paths())
        unexpected = changed - allowed
        if unexpected or changed != allowed:
            missing = allowed - changed
            detail = []
            if unexpected:
                detail.append("예상 밖 변경: " + ", ".join(sorted(unexpected)))
            if missing:
                detail.append("변경되지 않은 예상 파일: " + ", ".join(sorted(missing)))
            raise PipelineError("commit 대상 검증 실패: " + " / ".join(detail))

        run_cmd(["git", "add", "--", *sorted(allowed)], cwd=ROOT)
        run_cmd(["git", "diff", "--cached", "--check"], cwd=ROOT)
        run_cmd(["git", "commit", "-m", f"feat: publish weekly radio episode EP{episode_number:02d}"], cwd=ROOT)
        committed = True
        run_cmd(["git", "push", "origin", "main"], cwd=ROOT, timeout=900)
        update_draft_status(path, "pushed", timestamp_key="pushed_at")
        print(f"push 완료: EP {episode_number}")
        if verify_public_episode(record, wait_seconds=wait_seconds):
            update_draft_status(path, "published", timestamp_key="published_at")
            print(f"공개 URL 검증 PASS: EP {episode_number}")
            return 0
        print(f"push는 완료됐지만 Pages 반영 대기 상태입니다: EP {episode_number}")
        return 1
    except Exception:
        if not committed:
            restore_files(backups)
            try:
                run_cmd(["git", "restore", "--staged", "."], cwd=ROOT)
            except PipelineError:
                pass
        raise
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state-dir", type=Path, default=DEFAULT_STATE_DIR)
    sub = parser.add_subparsers(dest="command", required=True)

    approve = sub.add_parser("approve", help="draft.md를 approved 상태로 기록")
    approve.add_argument("--episode", type=int)

    publish = sub.add_parser("publish", help="approved draft를 렌더링·배포")
    publish.add_argument("--episode", type=int)
    publish.add_argument("--confirm", action="store_true")
    publish.add_argument("--dry-run", action="store_true")
    publish.add_argument("--wait", type=int, default=120, help="공개 URL 검증 대기 초")

    verify = sub.add_parser("verify", help="로컬 MP3와 공개 URL 검증")
    verify.add_argument("--episode", type=int)
    verify.add_argument("--wait", type=int, default=0)

    sub.add_parser("show", help="초안 상태 표시")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        args.state_dir.mkdir(parents=True, exist_ok=True)
        if args.command == "show":
            return cmd_show(args.state_dir)
        if args.command == "approve":
            return cmd_approve(args.episode, args.state_dir)
        if args.command == "publish":
            return cmd_publish(args.episode, args.state_dir, args.confirm, args.dry_run, args.wait)
        if args.command == "verify":
            return cmd_verify(args.episode, args.state_dir, args.wait)
        raise PipelineError(f"알 수 없는 명령: {args.command}")
    except PipelineError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
