#!/usr/bin/env python3
"""
Voice-consistent radio renderer.
1. Generate one reference clip with design mode (sets the voice)
2. Render all remaining lines with --reference-audio for consistency
3. Repeat for LOOP voice
"""
import subprocess
import os
import sys
from pathlib import Path

VOXCPM = "/Users/macbook/.venvs/voxcpm2/bin/voxcpm"
SCRIPT_DIR = Path("/Users/macbook/easyworking-ai.github.io/scripts/ep02-voice-proofs")

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


def render_with_consistent_voice(lines_file, output_dir, control, ref_text=None):
    """
    Step 1: Generate reference clip with design mode
    Step 2: Render all lines with --reference-audio for voice consistency
    """
    lines = [l.strip() for l in Path(lines_file).read_text().strip().split("\n") if l.strip()]
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if ref_text is None:
        ref_text = lines[0]  # Use first line as reference

    # Step 1: Generate reference clip
    ref_dir = output_dir / "_ref"
    ref_dir.mkdir(exist_ok=True)
    ref_text_file = ref_dir / "ref_text.txt"
    ref_text_file.write_text(ref_text)

    print(f"  [1/2] Generating reference clip...")
    subprocess.run([
        VOXCPM, "batch",
        "--input", str(ref_text_file),
        "--output-dir", str(ref_dir),
        "--control", control,
        "--cfg-value", "2.0",
        "--inference-timesteps", "30",
        "--normalize", "--denoise",
    ], check=True, capture_output=True, timeout=300)

    ref_audio = ref_dir / "output_001.wav"
    if not ref_audio.exists():
        raise RuntimeError(f"Reference clip not generated: {ref_audio}")

    print(f"  Reference clip: {ref_audio}")

    # Step 2: Render all lines with --reference-audio
    print(f"  [2/2] Rendering {len(lines)} lines with consistent voice...")

    for i, line in enumerate(lines):
        out_num = f"{i+1:03d}"
        line_file = output_dir / f"_line_{out_num}.txt"
        line_file.write_text(line)

        print(f"    Line {i+1}/{len(lines)}: {line[:40]}...", end="", flush=True)

        subprocess.run([
            VOXCPM, "batch",
            "--input", str(line_file),
            "--output-dir", str(output_dir),
            "--reference-audio", str(ref_audio),
            "--cfg-value", "2.0",
            "--inference-timesteps", "30",
            "--normalize", "--denoise",
        ], check=True, capture_output=True, timeout=120)

        # Rename to sequential
        generated = output_dir / "output_001.wav"
        if generated.exists():
            final_path = output_dir / f"line_{out_num}.wav"
            # If already exists (from batch numbering), remove
            if final_path.exists():
                final_path.unlink()
            generated.rename(final_path)
            line_file.unlink()
            print(f" DONE")
        else:
            print(f" FAILED")

    # Clean up ref dir
    import shutil
    shutil.rmtree(ref_dir, ignore_errors=True)

    return len(list(output_dir.glob("line_*.wav")))


def main():
    # Render IRO (이로)
    print("=== Rendering IRO (이로) ===")
    n_iro = render_with_consistent_voice(
        str(SCRIPT_DIR / "iro_v3.txt"),
        str(SCRIPT_DIR / "iro_v3_out"),
        IRO_CONTROL,
    )
    print(f"  IRO: {n_iro} clips rendered\n")

    # Render LOOP (루프)
    print("=== Rendering LOOP (루프) ===")
    n_loop = render_with_consistent_voice(
        str(SCRIPT_DIR / "loop_v3.txt"),
        str(SCRIPT_DIR / "loop_v3_out"),
        LOOP_CONTROL,
    )
    print(f"  LOOP: {n_loop} clips rendered\n")

    print(f"=== DONE: IRO {n_iro} + LOOP {n_loop} ===")


if __name__ == "__main__":
    main()
