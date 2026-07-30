#!/usr/bin/env python3
"""
EP02 v8: 이로 보이스 고정 (B variant output_002 기준)
- 이로: B output_002.wav를 --prompt-audio로 고정 → 전체 대사 클로닝
- 루프: 기존 v7 ref 방식 유지
- 3개 언어 (ko/en/ja)
"""
import subprocess
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from dialogues_v7 import DIALOGUES

VOXCPM = "/Users/macbook/.venvs/voxcpm2/bin/voxcpm"
SCRIPT_DIR = Path("/Users/macbook/easyworking-ai.github.io/scripts/ep02-voice-proofs")
OUTPUT_DIR = Path("/Users/macbook/easyworking-ai.github.io/quartz/static/radio")

# ── B variant control (이로 고정 톤) ──
IRO_CONTROL = (
    "A friendly Korean woman in her late twenties. "
    "Warm, casual, chatty — like talking to a coworker over coffee. "
    "Her voice goes up and down with genuine interest. "
    "She laughs a little when she's amused. "
    "Relaxed, informal, spontaneous. "
    "NOT a news anchor. NOT reading a script. "
    "Just a natural, expressive person having fun talking."
)

# 영어/일본어용 B 톤
IRO_CONTROLS = {
    "ko": IRO_CONTROL,
    "en": (
        "A friendly English-speaking woman in her late twenties. "
        "Warm, casual, chatty — like talking to a coworker over coffee. "
        "Her voice goes up and down with genuine interest. "
        "Relaxed, informal, spontaneous. "
        "NOT a news anchor. NOT reading a script. "
        "A natural, expressive person having fun talking."
    ),
    "ja": (
        "A friendly Japanese woman in her late twenties. "
        "Warm, casual, chatty — like talking to a coworker over coffee. "
        "Her voice goes up and down with genuine interest. "
        "Relaxed, informal, spontaneous. "
        "NOT a news anchor. NOT reading a script. "
        "A natural, expressive person having fun talking."
    ),
}

LOOP_CONTROLS = {
    "ko": (
        "A natural Korean male voice, mid thirties, "
        "warm and engaged in conversation. Not a news anchor — "
        "more like a knowledgeable friend explaining something with genuine enthusiasm. "
        "Relaxed, personable, occasionally pauses to think. "
        "Close mic, clean recording. Conversational, not robotic."
    ),
    "en": (
        "A natural English male voice, mid thirties, "
        "warm and engaged. Not a news anchor — a knowledgeable friend "
        "explaining something with genuine enthusiasm. "
        "Relaxed, personable. Close mic, clean recording."
    ),
    "ja": (
        "A natural Japanese male voice, mid thirties, "
        "warm and engaged. Not a news anchor — a knowledgeable friend "
        "explaining something with genuine enthusiasm. "
        "Relaxed, personable. Close mic, clean recording."
    ),
}

# B variant 두 번째 클립 (이로 고정 reference)
IRO_KO_PROMPT_AUDIO = SCRIPT_DIR / "iro_stiff_test/variant_B/output_002.wav"
IRO_KO_PROMPT_TEXT = "그러니까 검증된 결과를 가져온다는 거잖아요. 실무에서 신뢰하고 쓸 수 있다는 뜻이겠네요."


def generate_ref(lang, control, text, output_dir):
    """batch+control로 1줄 ref 생성 (영어/일본어 이로, 전체 루프용)"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "ref.txt").write_text(text)
    subprocess.run([
        VOXCPM, "batch", "--input", str(output_dir / "ref.txt"),
        "--output-dir", str(output_dir), "--control", control,
        "--cfg-value", "3.0", "--inference-timesteps", "30",
        "--normalize", "--denoise",
    ], check=True, capture_output=True, timeout=300)
    return output_dir / "output_001.wav"


def render_with_prompt(all_lines, prompt_audio, prompt_text, output_dir):
    """prompt-audio로 전체 대사 클로닝 (보이스 고정)"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    input_file = output_dir / "all_lines.txt"
    input_file.write_text("\n".join(all_lines))
    subprocess.run([
        VOXCPM, "batch", "--input", str(input_file),
        "--output-dir", str(output_dir),
        "--prompt-audio", str(prompt_audio),
        "--prompt-text", prompt_text,
        "--cfg-value", "3.0", "--inference-timesteps", "30",
        "--normalize", "--denoise",
    ], check=True, capture_output=True, timeout=600)


def assemble(segments, work_dir, output_mp3):
    work_dir = Path(work_dir)
    work_dir.mkdir(exist_ok=True)

    norm = []
    for idx, (wav, sp) in enumerate(segments):
        dst = work_dir / f"seg_{idx:03d}_{sp}.wav"
        subprocess.run(["ffmpeg", "-y", "-i", str(wav), "-ar", "44100", "-ac", "1",
                         "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", str(dst)], capture_output=True)
        norm.append((dst, sp))

    for name, dur in [("s1", 0.2), ("s2", 0.4), ("s3", 0.8), ("s4", 1.2)]:
        subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=channel_layout=mono:sample_rate=44100",
                         "-t", str(dur), str(work_dir / f"{name}.wav")], capture_output=True)

    breaks = {2, 9, 15, 21}
    entries = [f"file '{SCRIPT_DIR}/intro_sting.wav'", f"file '{work_dir}/s3.wav'"]
    for i, (wav, sp) in enumerate(norm):
        entries.append(f"file '{wav}'")
        if i < len(norm) - 1:
            nxt = norm[i + 1][1]
            if i in breaks:
                entries += [f"file '{work_dir}/s4.wav'", f"file '{SCRIPT_DIR}/transition.wav'", f"file '{work_dir}/s3.wav'"]
            elif sp != nxt:
                entries.append(f"file '{work_dir}/s2.wav'")
            else:
                entries.append(f"file '{work_dir}/s1.wav'")
    entries += [f"file '{work_dir}/s3.wav'", f"file '{SCRIPT_DIR}/outro_sting.wav'"]

    (work_dir / "concat.txt").write_text("\n".join(entries) + "\n")
    raw = work_dir / "raw.wav"
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(work_dir / "concat.txt"),
                     "-c", "copy", str(raw)], capture_output=True)
    rd = float(subprocess.run(["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
                                "-of", "csv=p=0", str(raw)], capture_output=True, text=True).stdout.strip())
    fade = max(0, rd - 3)
    subprocess.run(["ffmpeg", "-y", "-i", str(raw), "-i", str(SCRIPT_DIR / "bg_music.wav"),
                     "-filter_complex",
                     f"[1:a]volume=0.06,afade=t=in:st=0:d=2,afade=t=out:st={fade:.1f}:d=3[bg];"
                     f"[0:a][bg]amix=inputs=2:duration=first:dropout_transition=0,loudnorm=I=-16:TP=-1.5:LRA=11",
                     "-b:a", "128k", str(output_mp3)], capture_output=True)
    fd = float(subprocess.run(["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
                                "-of", "csv=p=0", str(output_mp3)], capture_output=True, text=True).stdout.strip())
    print(f"  {output_mp3.stem}: {fd:.1f}s ({fd/60:.1f}min)")


def process(lang):
    print(f"\n=== {lang.upper()} ===")
    dlg = DIALOGUES[lang]
    iro_lines = [t for s, t in dlg if s == "iro"]
    loop_lines = [t for s, t in dlg if s == "loop"]

    # ── 이로: 전체 대사를 prompt-audio로 클로닝 ──
    if lang == "ko":
        # 한국어: B output_002.wav를 직접 prompt로 사용
        iro_prompt_audio = IRO_KO_PROMPT_AUDIO
        iro_prompt_text = IRO_KO_PROMPT_TEXT
    else:
        # 영어/일본어: B 톤 control로 ref 생성
        print(f"  Iro ref ({lang})...")
        iro_ref_dir = f"{SCRIPT_DIR}/v8_{lang}_iro_ref"
        iro_prompt_audio = generate_ref(lang, IRO_CONTROLS[lang], iro_lines[0], iro_ref_dir)
        iro_prompt_text = iro_lines[0]

    print(f"  Iro all ({len(iro_lines)})...")
    iro_out_dir = f"{SCRIPT_DIR}/v8_{lang}_iro_out"
    render_with_prompt(iro_lines, iro_prompt_audio, iro_prompt_text, iro_out_dir)

    # ── 루프: 기존 방식 (ref → prompt-audio) ──
    print(f"  Loop ref...")
    loop_ref_dir = f"{SCRIPT_DIR}/v8_{lang}_loop_ref"
    loop_prompt_audio = generate_ref(lang, LOOP_CONTROLS[lang], loop_lines[0], loop_ref_dir)
    loop_prompt_text = loop_lines[0]

    print(f"  Loop remaining ({len(loop_lines) - 1})...")
    loop_rem_dir = f"{SCRIPT_DIR}/v8_{lang}_loop_out"
    if len(loop_lines) > 1:
        render_with_prompt(loop_lines[1:], loop_prompt_audio, loop_prompt_text, loop_rem_dir)

    # ── 클립 수집 ──
    iro_clips = sorted(Path(iro_out_dir).glob("output_*.wav"))
    loop_clips = [loop_prompt_audio]
    if Path(loop_rem_dir).exists():
        loop_clips += sorted(Path(loop_rem_dir).glob("output_*.wav"))

    # ── 인터리빙 ──
    ii, li = 0, 0
    segs = []
    for sp, _ in dlg:
        if sp == "iro" and ii < len(iro_clips):
            segs.append((iro_clips[ii], sp)); ii += 1
        elif sp == "loop" and li < len(loop_clips):
            segs.append((loop_clips[li], sp)); li += 1

    print(f"  Assemble {len(segs)}...")
    assemble(segs, f"{SCRIPT_DIR}/v8_{lang}_assemble", OUTPUT_DIR / f"episode-02-{lang}.mp3")


if __name__ == "__main__":
    for lang in ["ko", "en", "ja"]:
        process(lang)
    print("\n=== ALL DONE ===")
