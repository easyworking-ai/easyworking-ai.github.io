#!/usr/bin/env python3
"""
Render + assemble EP02 EN/JA v3 with consistent voices.
Uses --reference-audio cloning for voice consistency.
"""
import subprocess
import os
import shutil
from pathlib import Path

VOXCPM = "/Users/macbook/.venvs/voxcpm2/bin/voxcpm"
SCRIPT_DIR = Path("/Users/macbook/easyworking-ai.github.io/scripts/ep02-voice-proofs")
OUTPUT_DIR = Path("/Users/macbook/easyworking-ai.github.io/quartz/static/radio")

CONTROLS = {
    "en": {
        "iro": "A natural clear English female voice, late twenties, bright and clean tone, smooth conversational delivery like talking naturally to a friend, relaxed pace with organic pauses, crisp pronunciation, studio quality recording, no breathiness, no muffle, no noise",
        "loop": "A polished English male voice, calm and trustworthy, well-modulated radio host delivery, smooth and even, clean diction, moderate pace, professional broadcast quality, reassuring and competent",
    },
    "ja": {
        "iro": "A natural clear Japanese female voice, late twenties, bright and clean tone, smooth conversational delivery like talking naturally to a friend, relaxed pace with organic pauses, crisp pronunciation, studio quality recording, no breathiness, no muffle, no noise",
        "loop": "A polished Japanese male voice, calm and trustworthy, well-modulated radio host delivery, smooth and even, clean diction, moderate pace, professional broadcast quality, reassuring and competent",
    },
}

# Dialogue flow: (speaker, line_number_in_clean_file)
# EN: Iro 9 lines, Loop 11 lines
# JA: Iro 8 lines, Loop 11 lines
FLOWS = {
    "en": [
        ("iro", 1),    # Hi, I'm Iro...
        ("loop", 1),   # And I'm Loop...
        ("iro", 2),    # Loop, what does it actually change
        ("loop", 2),   # Two things. First...
        ("loop", 3),   # Second, it runs code
        ("iro", 3),    # Until now, AI gave you a meeting summary
        ("loop", 4),   # Previous models lost direction after five steps
        ("loop", 5),   # The era of humans manually connecting
        ("iro", 4),    # But here's the scary part
        ("loop", 6),   # The Hugging Face incident proves this
        ("loop", 7),   # Better models don't mean delegate everything
        ("iro", 5),    # As AI gets more capable
        ("iro", 6),    # So this week's experiment
        ("loop", 8),   # Other news this week
        ("iro", 7),    # For meeting notes
        ("loop", 9),   # Good experiment
        ("iro", 8),    # Next week, a new trend
        ("loop", 10),  # (not needed - skip)
        ("iro", 9),    # Thanks for listening
    ],
    "ja": [
        ("iro", 1),    # こんにちは、イロです
        ("loop", 1),   # そしてループです
        ("iro", 2),    # ループ、会社員にとって何が変わるの？
        ("loop", 2),   # 二つです
        ("loop", 3),   # 以前のモデルは5ステップで
        ("iro", 3),    # これまではAIが議事録をまとめて
        ("loop", 4),   # 人が各ステップを手動で
        ("loop", 5),   # しかし自律性が広がるほど
        ("iro", 4),    # でも同じ週に怖いニュースも
        ("loop", 6),   # Hugging Faceの事件が
        ("loop", 7),   # モデルが良くなるということは
        ("iro", 5),    # AIが賢くなるほど
        ("iro", 6),    # 今週の実験
        ("loop", 8),   # 今週の他のニュース
        ("iro", 7),    # 議事録なら
        ("loop", 9),   # 良い実験です
        ("iro", 8),    # 来週は新しいトレンドで
        ("loop", 10),  # (skip if doesn't exist)
        ("loop", 11),  # 聞いてくださって
    ],
}


def render_consistent(lines_file, output_dir, control):
    lines = [l.strip() for l in Path(lines_file).read_text().strip().split("\n") if l.strip()]
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Reference clip
    ref_dir = output_dir / "_ref"
    ref_dir.mkdir(exist_ok=True)
    (ref_dir / "ref.txt").write_text(lines[0])
    subprocess.run([VOXCPM, "batch", "--input", str(ref_dir/"ref.txt"), "--output-dir", str(ref_dir),
                     "--control", control, "--cfg-value", "2.0", "--inference-timesteps", "30",
                     "--normalize", "--denoise"], check=True, capture_output=True, timeout=300)
    ref_audio = ref_dir / "output_001.wav"

    for i, line in enumerate(lines):
        num = f"{i+1:03d}"
        print(f"    {i+1}/{len(lines)}: {line[:40]}...", end="", flush=True)
        lf = output_dir / f"_tmp_{num}.txt"
        lf.write_text(line)
        subprocess.run([VOXCPM, "batch", "--input", str(lf), "--output-dir", str(output_dir),
                         "--reference-audio", str(ref_audio), "--cfg-value", "2.0",
                         "--inference-timesteps", "30", "--normalize", "--denoise"],
                        check=True, capture_output=True, timeout=120)
        gen = output_dir / "output_001.wav"
        final = output_dir / f"line_{num}.wav"
        if final.exists(): final.unlink()
        gen.rename(final)
        lf.unlink()
        print(" DONE")

    shutil.rmtree(ref_dir, ignore_errors=True)


def assemble(flow, iro_dir, loop_dir, work_dir, output_mp3):
    work_dir.mkdir(exist_ok=True)
    segments = []
    for idx, (sp, ln) in enumerate(flow):
        src = Path(iro_dir if sp == "iro" else loop_dir) / f"line_{ln:03d}.wav"
        if not src.exists():
            print(f"  SKIP missing: {src}")
            continue
        dst = work_dir / f"seg_{idx:03d}_{sp}.wav"
        subprocess.run(["ffmpeg", "-y", "-i", str(src), "-ar", "44100", "-ac", "1",
                         "-af", "loudnorm=I=-18:TP=-1.5:LRA=11", str(dst)], capture_output=True)
        segments.append((dst, sp))

    for name, dur in [("sil_s", 0.25), ("sil_m", 0.5), ("sil_l", 1.0)]:
        subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=channel_layout=mono:sample_rate=44100",
                         "-t", str(dur), str(work_dir/f"{name}.wav")], capture_output=True)

    section_breaks = {4, 8, 12, 14}
    entries = [f"file '{SCRIPT_DIR}/intro_sting.wav'", f"file '{work_dir}/sil_m.wav'"]
    for i, (wav, sp) in enumerate(segments):
        entries.append(f"file '{wav}'")
        if i < len(segments) - 1:
            if i in section_breaks:
                entries += [f"file '{work_dir}/sil_l.wav'", f"file '{SCRIPT_DIR}/transition.wav'", f"file '{work_dir}/sil_l.wav'"]
            else:
                nxt = segments[i+1][1]
                entries.append(f"file '{work_dir}/{('sil_m' if sp != nxt else 'sil_s')}.wav'")
    entries += [f"file '{work_dir}/sil_l.wav'", f"file '{SCRIPT_DIR}/outro_sting.wav'"]

    (work_dir/"concat.txt").write_text("\n".join(entries)+"\n")
    raw = work_dir / "raw.wav"
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(work_dir/"concat.txt"),
                     "-c", "copy", str(raw)], capture_output=True)
    rd = float(subprocess.run(["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
                                "-of", "csv=p=0", str(raw)], capture_output=True, text=True).stdout.strip())
    fade = max(0, rd - 3)
    subprocess.run(["ffmpeg", "-y", "-i", str(raw), "-i", str(SCRIPT_DIR/"bg_music.wav"),
                     "-filter_complex",
                     f"[1:a]volume=0.08,afade=t=in:st=0:d=2,afade=t=out:st={fade:.1f}:d=3[bg];"
                     f"[0:a][bg]amix=inputs=2:duration=first:dropout_transition=0,loudnorm=I=-16:TP=-1.5:LRA=11",
                     "-b:a", "128k", str(output_mp3)], capture_output=True)
    fd = float(subprocess.run(["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
                                "-of", "csv=p=0", str(output_mp3)], capture_output=True, text=True).stdout.strip())
    print(f"  Final: {fd:.1f}s ({fd/60:.1f}min)")


if __name__ == "__main__":
    for lang in ["en", "ja"]:
        print(f"\n=== {lang.upper()} ===")
        print(f"  Rendering Iro...")
        render_consistent(str(SCRIPT_DIR/f"{lang}_iro_v3_clean.txt"),
                          str(SCRIPT_DIR/f"{lang}_iro_v3_clean_out"),
                          CONTROLS[lang]["iro"])
        print(f"  Rendering Loop...")
        render_consistent(str(SCRIPT_DIR/f"{lang}_loop_v3_clean.txt"),
                          str(SCRIPT_DIR/f"{lang}_loop_v3_clean_out"),
                          CONTROLS[lang]["loop"])
        print(f"  Assembling...")
        assemble(FLOWS[lang],
                 str(SCRIPT_DIR/f"{lang}_iro_v3_clean_out"),
                 str(SCRIPT_DIR/f"{lang}_loop_v3_clean_out"),
                 SCRIPT_DIR/f"{lang}_v3_assemble",
                 str(OUTPUT_DIR/f"episode-02-{lang}.mp3"))
    print("\n=== ALL DONE ===")
