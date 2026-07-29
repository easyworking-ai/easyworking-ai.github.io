#!/usr/bin/env python3
"""
EP02 v4: batch+control mode (no reference-audio cloning) for better audio quality.
Close-mic control prompts for intimate, present voice.
Interleaved dialogue assembly with natural pacing.
"""
import subprocess
import os
from pathlib import Path

VOXCPM = "/Users/macbook/.venvs/voxcpm2/bin/voxcpm"
SCRIPT_DIR = Path("/Users/macbook/easyworking-ai.github.io/scripts/ep02-voice-proofs")
OUTPUT_DIR = Path("/Users/macbook/easyworking-ai.github.io/quartz/static/radio")

# Close-mic controls: forward, present, intimate
CONTROLS = {
    "ko": {
        "iro": (
            "A natural clear Korean female voice, late twenties, "
            "bright and warm tone, close microphone recording, "
            "intimate and present, forward in the mix, dry with no reverb, "
            "smooth conversational delivery like talking to a friend sitting next to you, "
            "relaxed pace, crisp pronunciation, studio quality"
        ),
        "loop": (
            "A polished Korean male voice, calm and trustworthy, "
            "close microphone radio host delivery, present and forward, "
            "dry recording with no room echo, smooth and even, "
            "clean diction, moderate pace, professional broadcast quality"
        ),
    },
    "en": {
        "iro": (
            "A natural clear English female voice, late twenties, "
            "bright and warm tone, close microphone recording, "
            "intimate and present, forward in the mix, dry with no reverb, "
            "smooth conversational delivery like talking to a friend, "
            "relaxed pace, crisp pronunciation, studio quality"
        ),
        "loop": (
            "A polished English male voice, calm and trustworthy, "
            "close microphone radio host delivery, present and forward, "
            "dry recording with no room echo, smooth and even, "
            "clean diction, moderate pace, professional broadcast quality"
        ),
    },
    "ja": {
        "iro": (
            "A natural clear Japanese female voice, late twenties, "
            "bright and warm tone, close microphone recording, "
            "intimate and present, forward in the mix, dry with no reverb, "
            "smooth conversational delivery like talking to a friend, "
            "relaxed pace, crisp pronunciation, studio quality"
        ),
        "loop": (
            "A polished Japanese male voice, calm and trustworthy, "
            "close microphone radio host delivery, present and forward, "
            "dry recording with no room echo, smooth and even, "
            "clean diction, moderate pace, professional broadcast quality"
        ),
    },
}

# Dialogue flow for each language
# Format: (speaker, line_number_in_file)
FLOWS = {
    "ko": [
        ("iro", 1), ("iro", 2), ("iro", 3),
        ("iro", 4),  # 루프에게 질문
        ("loop", 1), ("loop", 2),
        ("iro", 5),  # 회의록 반응
        ("loop", 3),
        ("iro", 6),  # 권한 경계
        ("loop", 4),
        ("iro", 7),  # 실험 제안
        ("loop", 5),  # 빠른 뉴스 라운드업
        ("iro", 8),  # 회의록 보충
        ("loop", 6),  # 좋은 실험
        ("iro", 9), ("iro", 10),
    ],
    "en": [
        ("iro", 1), ("iro", 2), ("iro", 3),
        ("iro", 4),  # question to Loop
        ("loop", 1), ("loop", 2),
        ("iro", 5),
        ("loop", 3),
        ("iro", 6),
        ("loop", 4), ("loop", 5), ("loop", 6),
        ("iro", 7),
        ("loop", 7),
        ("iro", 8), ("iro", 9),
    ],
    "ja": [
        ("iro", 1), ("iro", 2), ("iro", 3),
        ("iro", 4),  # question
        ("loop", 1), ("loop", 2),
        ("iro", 5),
        ("loop", 3),
        ("iro", 6),
        ("loop", 4), ("loop", 5),
        ("iro", 7),
        ("loop", 6),
        ("iro", 8), ("iro", 9), ("iro", 10),
    ],
}


def render_batch(lines_file, output_dir, control):
    """Render all lines with batch+control mode."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    subprocess.run([
        VOXCPM, "batch",
        "--input", str(lines_file),
        "--output-dir", str(output_dir),
        "--control", control,
        "--cfg-value", "2.0",
        "--inference-timesteps", "30",
        "--normalize", "--denoise",
    ], check=True, capture_output=True, timeout=600)

    n = len(list(output_dir.glob("output_*.wav")))
    print(f"    Rendered {n} clips")
    return n


def assemble(flow, iro_dir, loop_dir, work_dir, output_mp3):
    """Interleave with natural conversation pacing."""
    work_dir = Path(work_dir)
    work_dir.mkdir(exist_ok=True)

    segments = []
    for idx, (speaker, line_num) in enumerate(flow):
        src = Path(iro_dir if speaker == "iro" else loop_dir) / f"output_{line_num:03d}.wav"
        if not src.exists():
            print(f"  SKIP: {src}")
            continue
        dst = work_dir / f"seg_{idx:03d}_{speaker}.wav"
        subprocess.run([
            "ffmpeg", "-y", "-i", str(src), "-ar", "44100", "-ac", "1",
            "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
            str(dst)
        ], capture_output=True)
        segments.append((dst, speaker))

    # Create silence gaps - shorter for same-speaker, longer for switches
    for name, dur in [("sil_tight", 0.15), ("sil_normal", 0.35), ("sil_pause", 0.8), ("sil_break", 1.2)]:
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi",
            "-i", "anullsrc=channel_layout=mono:sample_rate=44100",
            "-t", str(dur), str(work_dir / f"{name}.wav")
        ], capture_output=True)

    # Build concat list with natural pacing
    section_breaks = {3, 7, 11, 14}  # after major topic shifts

    entries = [
        f"file '{SCRIPT_DIR}/intro_sting.wav'",
        f"file '{work_dir}/sil_pause.wav'",
    ]

    for i, (wav, speaker) in enumerate(segments):
        entries.append(f"file '{wav}'")
        if i < len(segments) - 1:
            next_sp = segments[i + 1][1]
            if i in section_breaks:
                entries += [
                    f"file '{work_dir}/sil_break.wav'",
                    f"file '{SCRIPT_DIR}/transition.wav'",
                    f"file '{work_dir}/sil_pause.wav'",
                ]
            elif speaker != next_sp:
                # Speaker switch: natural pause
                entries.append(f"file '{work_dir}/sil_normal.wav'")
            else:
                # Same speaker continuation: tight
                entries.append(f"file '{work_dir}/sil_tight.wav'")

    entries += [
        f"file '{work_dir}/sil_pause.wav'",
        f"file '{SCRIPT_DIR}/outro_sting.wav'",
    ]

    concat_file = work_dir / "concat.txt"
    concat_file.write_text("\n".join(entries) + "\n")

    # Concat
    raw = work_dir / "raw.wav"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_file), "-c", "copy", str(raw)
    ], capture_output=True)

    raw_dur = float(subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", str(raw)],
        capture_output=True, text=True
    ).stdout.strip())
    print(f"  Raw: {raw_dur:.1f}s ({raw_dur/60:.1f}min)")

    # Mix with bg music (very subtle)
    fade = max(0, raw_dur - 3)
    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(raw),
        "-i", str(SCRIPT_DIR / "bg_music.wav"),
        "-filter_complex",
        f"[1:a]volume=0.06,afade=t=in:st=0:d=2,afade=t=out:st={fade:.1f}:d=3[bg];"
        f"[0:a][bg]amix=inputs=2:duration=first:dropout_transition=0,"
        f"loudnorm=I=-16:TP=-1.5:LRA=11",
        "-b:a", "128k", str(output_mp3)
    ], capture_output=True)

    final_dur = float(subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", str(output_mp3)],
        capture_output=True, text=True
    ).stdout.strip())
    print(f"  Final: {final_dur:.1f}s ({final_dur/60:.1f}min)")


def process_lang(lang):
    print(f"\n=== {lang.upper()} ===")
    print(f"  Rendering Iro...")
    render_batch(
        str(SCRIPT_DIR / f"{lang}_iro_v4.txt") if lang != "ko" else str(SCRIPT_DIR / "iro_v4.txt"),
        str(SCRIPT_DIR / f"{lang}_iro_v4_out"),
        CONTROLS[lang]["iro"],
    )
    print(f"  Rendering Loop...")
    loop_file = f"{lang}_loop_v4.txt" if lang != "ko" else "loop_v4.txt"
    render_batch(
        str(SCRIPT_DIR / loop_file),
        str(SCRIPT_DIR / f"{lang}_loop_v4_out"),
        CONTROLS[lang]["loop"],
    )
    print(f"  Assembling...")
    assemble(
        FLOWS[lang],
        str(SCRIPT_DIR / f"{lang}_iro_v4_out"),
        str(SCRIPT_DIR / f"{lang}_loop_v4_out"),
        SCRIPT_DIR / f"{lang}_v4_assemble",
        str(OUTPUT_DIR / f"episode-02-{lang}.mp3"),
    )


if __name__ == "__main__":
    for lang in ["ko", "en", "ja"]:
        process_lang(lang)
    print("\n=== ALL DONE ===")
