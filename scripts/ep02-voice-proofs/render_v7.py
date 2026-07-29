#!/usr/bin/env python3
"""
EP02 v7: 신호→소식, AI 표현 제거, 자연스러운 대화체, ts30
"""
import subprocess
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from dialogues_v7 import DIALOGUES

VOXCPM = "/Users/macbook/.venvs/voxcpm2/bin/voxcpm"
SCRIPT_DIR = Path("/Users/macbook/easyworking-ai.github.io/scripts/ep02-voice-proofs")
OUTPUT_DIR = Path("/Users/macbook/easyworking-ai.github.io/quartz/static/radio")

CONTROLS = {
    "ko": {
        "iro": (
            "A natural Korean female voice, early thirties, "
            "having a real conversation with a colleague. Warm, thoughtful, slightly curious. "
            "Speaks at a relaxed pace like she's sitting across from you. "
            "Close mic, clean recording. "
            "Not reading a script — talking naturally with genuine interest."
        ),
        "loop": (
            "A natural Korean male voice, mid thirties, "
            "warm and engaged in conversation. Not a news anchor — "
            "more like a knowledgeable friend explaining something with genuine enthusiasm. "
            "Relaxed, personable, occasionally pauses to think. "
            "Close mic, clean recording. Conversational, not robotic."
        ),
    },
    "en": {
        "iro": (
            "A natural English female voice, early thirties, "
            "having a real conversation. Warm, thoughtful, slightly curious. "
            "Relaxed pace, close mic, clean recording. "
            "Not reading — talking naturally with genuine interest."
        ),
        "loop": (
            "A natural English male voice, mid thirties, "
            "warm and engaged. Not a news anchor — a knowledgeable friend "
            "explaining something with genuine enthusiasm. "
            "Relaxed, personable. Close mic, clean recording."
        ),
    },
    "ja": {
        "iro": (
            "A natural Japanese female voice, early thirties, "
            "having a real conversation. Warm, thoughtful, slightly curious. "
            "Relaxed pace, close mic, clean recording. "
            "Not reading — talking naturally."
        ),
        "loop": (
            "A natural Japanese male voice, mid thirties, "
            "warm and engaged. Not a news anchor — a knowledgeable friend. "
            "Relaxed, personable. Close mic, clean recording."
        ),
    },
}


def generate_ref(lang, speaker, text, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "ref.txt").write_text(text)
    subprocess.run([
        VOXCPM, "batch", "--input", str(output_dir / "ref.txt"),
        "--output-dir", str(output_dir), "--control", CONTROLS[lang][speaker],
        "--cfg-value", "2.0", "--inference-timesteps", "30",
        "--normalize", "--denoise",
    ], check=True, capture_output=True, timeout=300)
    return output_dir / "output_001.wav"


def render_remaining(lines_file, output_dir, prompt_audio, prompt_text):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        VOXCPM, "batch", "--input", str(lines_file), "--output-dir", str(output_dir),
        "--prompt-audio", str(prompt_audio), "--prompt-text", prompt_text,
        "--cfg-value", "2.0", "--inference-timesteps", "30",
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
    iro_entries = [(i, t) for i, (s, t) in enumerate(dlg) if s == "iro"]
    loop_entries = [(i, t) for i, (s, t) in enumerate(dlg) if s == "loop"]

    print("  Refs...")
    iro_ref = generate_ref(lang, "iro", iro_entries[0][1], f"{SCRIPT_DIR}/{lang}_v7_ref_iro")
    loop_ref = generate_ref(lang, "loop", loop_entries[0][1], f"{SCRIPT_DIR}/{lang}_v7_ref_loop")

    iro_rem = [t for _, t in iro_entries[1:]]
    loop_rem = [t for _, t in loop_entries[1:]]

    if iro_rem:
        f = Path(f"{SCRIPT_DIR}/{lang}_v7_iro_rem.txt")
        f.write_text("\n".join(iro_rem))
        print(f"  Iro remaining ({len(iro_rem)})...")
        render_remaining(f, f"{SCRIPT_DIR}/{lang}_v7_iro_out", iro_ref, iro_entries[0][1])
    if loop_rem:
        f = Path(f"{SCRIPT_DIR}/{lang}_v7_loop_rem.txt")
        f.write_text("\n".join(loop_rem))
        print(f"  Loop remaining ({len(loop_rem)})...")
        render_remaining(f, f"{SCRIPT_DIR}/{lang}_v7_loop_out", loop_ref, loop_entries[0][1])

    iro_clips = [iro_ref] + sorted(Path(f"{SCRIPT_DIR}/{lang}_v7_iro_out").glob("output_*.wav"))
    loop_clips = [loop_ref] + sorted(Path(f"{SCRIPT_DIR}/{lang}_v7_loop_out").glob("output_*.wav"))
    ii, li = 0, 0
    segs = []
    for sp, _ in dlg:
        if sp == "iro" and ii < len(iro_clips):
            segs.append((iro_clips[ii], sp)); ii += 1
        elif sp == "loop" and li < len(loop_clips):
            segs.append((loop_clips[li], sp)); li += 1

    print(f"  Assemble {len(segs)}...")
    assemble(segs, f"{SCRIPT_DIR}/{lang}_v7_assemble", OUTPUT_DIR / f"episode-02-{lang}.mp3")


if __name__ == "__main__":
    for lang in ["ko", "en", "ja"]:
        process(lang)
    print("\n=== ALL DONE ===")
