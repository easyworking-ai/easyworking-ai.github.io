#!/usr/bin/env python3
"""
Render + assemble EP02 v3 with consistent voices.
1. Render clean IRO (10 lines) and LOOP (9 lines) with --reference-audio
2. Interleave in dialogue order
3. Add music/transitions
4. Output final MP3
"""
import subprocess
import os
import shutil
from pathlib import Path

VOXCPM = "/Users/macbook/.venvs/voxcpm2/bin/voxcpm"
SCRIPT_DIR = Path("/Users/macbook/easyworking-ai.github.io/scripts/ep02-voice-proofs")
OUTPUT_DIR = Path("/Users/macbook/easyworking-ai.github.io/quartz/static/radio")

IRO_CONTROL = (
    "A natural clear Korean female voice, late twenties, bright and clean tone, "
    "smooth conversational delivery like talking naturally to a friend, "
    "relaxed pace with organic pauses, crisp pronunciation, "
    "studio quality recording, no breathiness, no muffle, no noise"
)
LOOP_CONTROL = (
    "A polished Korean male voice, calm and trustworthy, "
    "well-modulated radio host delivery, smooth and even, clean diction, "
    "moderate pace, professional broadcast quality, reassuring and competent"
)

# Dialogue flow: (speaker, line_number_in_clean_file)
# IRO has 10 lines, LOOP has 9 lines
DIALOGUE_FLOW = [
    ("iro", 1),    # 안녕, 이로입니다
    ("loop", 1),   # 그리고 루프입니다
    ("iro", 2),    # 이번 주 최고 화제, Claude Opus 5
    ("iro", 3),    # 루프, 직장인에게 실제로 뭘 바꿔주는 거야?
    ("loop", 2),   # 두 가지입니다
    ("loop", 3),   # 이전 모델은 다섯 단계만 지나도
    ("iro", 4),    # 이전까지는 AI가 회의록 정리하고 끝이었잖아?
    ("loop", 4),   # 맞습니다. 각 단계를 사람이 연결하던 시대가
    ("iro", 5),    # 근데 같은 주에 무서운 뉴스도 있었어
    ("loop", 5),   # 581점을 받은 이 소식이 두 번째로 뜨거웠습니다
    ("loop", 6),   # 능력은 있었지만 어디로 향할지를 통제하지 못한 거죠
    ("iro", 6),    # 능력이 커질수록 권한 경계를 먼저 정해야 해
    ("iro", 7),    # 그래서 이번 주 실험입니다
    ("loop", 7),   # 이번 주 다른 소식을 빠르게 짚겠습니다
    ("iro", 8),    # 회의록이면 AI가 초안을 만들고
    ("loop", 8),   # 좋은 실험입니다
    ("iro", 9),    # 다음 주에 또 새로운 트렌드로
    ("iro", 10),   # 들어주셔서 고맙습니다 (should be loop 9)
    ("loop", 9),   # 들어주셔서 고맙습니다
]

# Fix: both iro 10 and loop 9 say goodbye. Use loop 9 as the final.
CORRECTED_FLOW = [
    ("iro", 1),    # 안녕, 이로입니다
    ("loop", 1),   # 그리고 루프입니다
    ("iro", 2),    # 이번 주 최고 화제, Claude Opus 5
    ("iro", 3),    # 루프, 직장인에게 실제로 뭘 바꿔주는 거야?
    ("loop", 2),   # 두 가지입니다
    ("loop", 3),   # 이전 모델은 다섯 단계
    ("iro", 4),    # 이전까지는 AI가 회의록 정리하고 끝이었잖아?
    ("loop", 4),   # 맞습니다. 각 단계를 사람이 연결하던 시대가
    ("iro", 5),    # 근데 같은 주에 무서운 뉴스도 있었어
    ("loop", 5),   # 581점을 받은 이 소식
    ("loop", 6),   # 능력은 있었지만 어디로 향할지를 통제하지 못한 거죠
    ("iro", 6),    # 능력이 커질수록 권한 경계를 먼저 정해야 해
    ("iro", 7),    # 그래서 이번 주 실험입니다
    ("loop", 7),   # 이번 주 다른 소식을 빠르게
    ("iro", 8),    # 회의록이면 AI가 초안을 만들고
    ("loop", 8),   # 좋은 실험입니다
    ("iro", 9),    # 다음 주에 또 새로운 트렌드로
    ("loop", 9),   # 들어주셔서 고맙습니다
]


def render_consistent(lines_file, output_dir, control):
    """Render all lines with consistent voice using reference-audio cloning."""
    lines = [l.strip() for l in Path(lines_file).read_text().strip().split("\n") if l.strip()]
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: Generate reference clip
    ref_dir = output_dir / "_ref"
    ref_dir.mkdir(exist_ok=True)
    (ref_dir / "ref.txt").write_text(lines[0])

    print(f"  Generating reference clip...")
    subprocess.run([
        VOXCPM, "batch",
        "--input", str(ref_dir / "ref.txt"),
        "--output-dir", str(ref_dir),
        "--control", control,
        "--cfg-value", "2.0", "--inference-timesteps", "30",
        "--normalize", "--denoise",
    ], check=True, capture_output=True, timeout=300)

    ref_audio = ref_dir / "output_001.wav"

    # Step 2: Render each line
    for i, line in enumerate(lines):
        num = f"{i+1:03d}"
        print(f"    Line {i+1}/{len(lines)}: {line[:40]}...", end="", flush=True)
        line_file = output_dir / f"_tmp_{num}.txt"
        line_file.write_text(line)

        subprocess.run([
            VOXCPM, "batch",
            "--input", str(line_file),
            "--output-dir", str(output_dir),
            "--reference-audio", str(ref_audio),
            "--cfg-value", "2.0", "--inference-timesteps", "30",
            "--normalize", "--denoise",
        ], check=True, capture_output=True, timeout=120)

        generated = output_dir / "output_001.wav"
        final = output_dir / f"line_{num}.wav"
        if final.exists():
            final.unlink()
        generated.rename(final)
        line_file.unlink()
        print(" DONE")

    shutil.rmtree(ref_dir, ignore_errors=True)
    return len(lines)


def assemble(flow, iro_dir, loop_dir, output_mp3):
    """Interleave clips and produce final MP3."""
    work = SCRIPT_DIR / "ko_v3_final_assemble"
    work.mkdir(exist_ok=True)

    # Normalize all clips
    segments = []
    for idx, (speaker, line_num) in enumerate(flow):
        src = Path(iro_dir if speaker == "iro" else loop_dir) / f"line_{line_num:03d}.wav"
        if not src.exists():
            print(f"  MISSING: {src}")
            continue
        dst = work / f"seg_{idx:03d}_{speaker}.wav"
        subprocess.run([
            "ffmpeg", "-y", "-i", str(src), "-ar", "44100", "-ac", "1",
            "-af", "loudnorm=I=-18:TP=-1.5:LRA=11",
            str(dst)
        ], capture_output=True)
        segments.append((dst, speaker))

    # Silence files
    for name, dur in [("sil_s", 0.25), ("sil_m", 0.5), ("sil_l", 1.0)]:
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi",
            "-i", "anullsrc=channel_layout=mono:sample_rate=44100",
            "-t", str(dur), str(work / f"{name}.wav")
        ], capture_output=True)

    # Build concat list
    entries = [
        f"file '{SCRIPT_DIR}/intro_sting.wav'",
        f"file '{work}/sil_m.wav'",
    ]

    # Section transitions at these positions
    section_breaks = {4, 8, 12, 14}

    for i, (wav, speaker) in enumerate(segments):
        entries.append(f"file '{wav}'")
        if i < len(segments) - 1:
            if i in section_breaks:
                entries.append(f"file '{work}/sil_l.wav'")
                entries.append(f"file '{SCRIPT_DIR}/transition.wav'")
                entries.append(f"file '{work}/sil_l.wav'")
            else:
                next_sp = segments[i+1][1]
                gap = "sil_m" if speaker != next_sp else "sil_s"
                entries.append(f"file '{work}/{gap}.wav'")

    entries.append(f"file '{work}/sil_l.wav'")
    entries.append(f"file '{SCRIPT_DIR}/outro_sting.wav'")

    concat_file = work / "concat.txt"
    concat_file.write_text("\n".join(entries) + "\n")

    # Concat
    raw = work / "raw.wav"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_file), "-c", "copy", str(raw)
    ], capture_output=True)

    # Duration
    dur = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", str(raw)],
        capture_output=True, text=True
    ).stdout.strip()
    raw_dur = float(dur)
    print(f"  Raw: {raw_dur:.1f}s ({raw_dur/60:.1f}min)")

    # Mix with bg music
    fade = max(0, raw_dur - 3)
    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(raw),
        "-i", str(SCRIPT_DIR / "bg_music.wav"),
        "-filter_complex",
        f"[1:a]volume=0.08,afade=t=in:st=0:d=2,afade=t=out:st={fade:.1f}:d=3[bg];"
        f"[0:a][bg]amix=inputs=2:duration=first:dropout_transition=0,"
        f"loudnorm=I=-16:TP=-1.5:LRA=11",
        "-b:a", "128k", str(output_mp3)
    ], capture_output=True)

    final_dur = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", str(output_mp3)],
        capture_output=True, text=True
    ).stdout.strip()
    print(f"  Final: {float(final_dur):.1f}s ({float(final_dur)/60:.1f}min)")


if __name__ == "__main__":
    import sys

    # Step 1: Render clean scripts with consistent voices
    print("=== Rendering IRO (이로) — 10 lines ===")
    render_consistent(
        str(SCRIPT_DIR / "iro_v3_clean.txt"),
        str(SCRIPT_DIR / "iro_v3_clean_out"),
        IRO_CONTROL,
    )

    print("\n=== Rendering LOOP (루프) — 9 lines ===")
    render_consistent(
        str(SCRIPT_DIR / "loop_v3_clean.txt"),
        str(SCRIPT_DIR / "loop_v3_clean_out"),
        LOOP_CONTROL,
    )

    # Step 2: Assemble
    print("\n=== Assembling KO v3 ===")
    assemble(
        CORRECTED_FLOW,
        str(SCRIPT_DIR / "iro_v3_clean_out"),
        str(SCRIPT_DIR / "loop_v3_clean_out"),
        str(OUTPUT_DIR / "episode-02-ko.mp3"),
    )

    print("\n=== DONE ===")
