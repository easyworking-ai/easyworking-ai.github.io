#!/usr/bin/env python3
"""
Final assembly script for EP02 expanded radio episode.
Combines VoxCPM2 IRO + LOOP chunks with:
- Intro/outro music stingers
- Section transition sounds  
- Natural pacing (cross-speaker gaps, section breaks)
- Background music bed (subtle)
- Final loudnorm for broadcast quality
"""

import subprocess
import os
import sys

SCRIPT_DIR = "/Users/macbook/easyworking-ai.github.io/scripts/ep02-voice-proofs"
OUTPUT_DIR = "/Users/macbook/easyworking-ai.github.io/quartz/static/radio"

# Episode structure: list of (speaker, source_file, text_for_reference)
# IRO lines come from ko_iro_final/output_001.wav etc.
# LOOP lines come from ko_loop_final/output_001.wav etc.

# Interleave order: IRO[0], IRO[1], IRO[2], IRO[3], LOOP[0], LOOP[1], LOOP[2], LOOP[3],
#                   IRO[4], IRO[5], LOOP[4], LOOP[5], IRO[6], IRO[7], IRO[8],
#                   LOOP[6], LOOP[7], IRO[9], IRO[10], LOOP[8], LOOP[9],
#                   IRO[11], LOOP[10], LOOP[11], LOOP[12],
#                   IRO[12], IRO[13], LOOP[13], LOOP[14], IRO[14]

# Pattern based on script content flow:
# IRO intro (4) → LOOP explains (4) → IRO reaction (2) → LOOP detail (2) →
# IRO transition (3) → LOOP HF incident (2) → IRO reflection (2) → LOOP insight (2) →
# IRO news roundup (2) → LOOP news detail (3) → IRO experiment (1) → LOOP experiment (1) →
# IRO outro (2) → LOOP outro (1)

INTERLEAVE = [
    # Section 1: Intro + Opus 5 announcement
    ("iro", 1), ("iro", 2), ("iro", 3),  # IRO opens
    ("loop", 1), ("loop", 2),  # LOOP intro + 1771 points
    # Section 2: What changed - two key features
    ("iro", 4),  # IRO asks what changed
    ("loop", 3), ("loop", 4),  # LOOP explains two features
    ("iro", 5), ("iro", 6),  # IRO: meeting notes example
    ("loop", 5),  # LOOP: precise example
    # Section 3: Implications
    ("iro", 7),  # IRO: runs code, fixes mistakes
    ("iro", 8),  # IRO: scary but interesting
    ("loop", 6),  # LOOP: autonomy needs boundaries
    # Section 4: Hugging Face incident
    ("iro", 9), ("iro", 10),  # IRO: HF attack intro
    ("loop", 7), ("loop", 8),  # LOOP: 581 points, capability without control
    ("iro", 11),  # IRO: two stories side by side
    ("loop", 9),  # LOOP: permission boundaries
    # Section 5: Other news
    ("iro", 12),  # IRO: other news?
    ("loop", 10), ("loop", 11), ("loop", 12),  # LOOP: Gemini, Cursor, Aurora
    # Section 6: Experiment + Outro
    ("iro", 13),  # IRO: experiment suggestion
    ("loop", 13),  # LOOP: good experiment, meeting notes example
    ("iro", 14),  # IRO: outro
    ("loop", 14),  # LOOP: outro
]

# Section break points (insert long silence + transition sound)
# After: intro (3), features (6), implications (10), HF incident (15), news (18), experiment (19)
SECTION_BREAK_AFTER_INDEX = {2, 5, 9, 14, 17, 19}


def get_chunk_path(speaker, num):
    """Get the WAV file path for a chunk."""
    dirname = f"ko_{speaker}_final"
    return f"{SCRIPT_DIR}/{dirname}/output_{num:03d}.wav"


def assemble(lang="ko"):
    """Assemble the final episode."""
    work = f"{SCRIPT_DIR}/{lang}_final_assemble"
    os.makedirs(work, exist_ok=True)
    
    # Step 1: Normalize each chunk to consistent format
    print("Normalizing chunks...")
    norm_files = []
    for i, (speaker, num) in enumerate(INTERLEAVE):
        src = get_chunk_path(speaker, num)
        if not os.path.exists(src):
            print(f"  MISSING: {src}")
            continue
        dst = f"{work}/seg_{i:03d}_{speaker}.wav"
        subprocess.run([
            "ffmpeg", "-y", "-i", src, "-ar", "44100", "-ac", "1",
            "-af", "loudnorm=I=-18:TP=-1.5:LRA=11",
            dst
        ], capture_output=True)
        norm_files.append((dst, speaker))
        print(f"  seg_{i:03d} ({speaker}): normalized")
    
    # Step 2: Create silence/gap files
    print("\nCreating gap files...")
    for dur, name in [(0.3, "sil_short"), (0.6, "sil_mid"), (1.2, "sil_section")]:
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi", "-i",
            f"anullsrc=channel_layout=mono:sample_rate=44100",
            "-t", str(dur), f"{work}/{name}.wav"
        ], capture_output=True)
    
    # Step 3: Build concat list
    print("\nBuilding concat list...")
    concat_entries = []
    
    # Intro stinger
    concat_entries.append(f"file '{SCRIPT_DIR}/intro_sting.wav'")
    concat_entries.append(f"file '{work}/sil_mid.wav'")
    
    for i, (wav_file, speaker) in enumerate(norm_files):
        concat_entries.append(f"file '{wav_file}'")
        
        if i < len(norm_files) - 1:
            if i in SECTION_BREAK_AFTER_INDEX:
                # Section break: silence + transition + silence
                concat_entries.append(f"file '{work}/sil_section.wav'")
                concat_entries.append(f"file '{SCRIPT_DIR}/transition.wav'")
                concat_entries.append(f"file '{work}/sil_section.wav'")
            else:
                next_speaker = norm_files[i+1][1]
                if speaker != next_speaker:
                    # Cross-speaker gap (slightly longer)
                    concat_entries.append(f"file '{work}/sil_mid.wav'")
                else:
                    # Same speaker continuation
                    concat_entries.append(f"file '{work}/sil_short.wav'")
    
    # Outro
    concat_entries.append(f"file '{work}/sil_section.wav'")
    concat_entries.append(f"file '{SCRIPT_DIR}/outro_sting.wav'")
    
    # Write concat file
    concat_file = f"{work}/concat.txt"
    with open(concat_file, "w") as f:
        f.write("\n".join(concat_entries))
    
    # Step 4: Concat all
    print("\nConcatenating...")
    raw_output = f"{work}/{lang}_raw.wav"
    result = subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", concat_file, "-c", "copy", raw_output
    ], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ERROR: {result.stderr[:500]}")
        return None
    
    # Check raw duration
    dur_result = subprocess.run([
        "ffprobe", "-v", "quiet", "-show_entries", "format=duration",
        "-of", "csv=p=0", raw_output
    ], capture_output=True, text=True)
    raw_dur = float(dur_result.stdout.strip())
    print(f"  Raw duration: {raw_dur:.1f}s ({raw_dur/60:.1f}min)")
    
    # Step 5: Mix with background music
    print("\nMixing with background music...")
    fade_start = max(0, raw_dur - 3)
    final_output = f"{OUTPUT_DIR}/episode-02-{lang}.mp3"
    
    result = subprocess.run([
        "ffmpeg", "-y",
        "-i", raw_output,
        "-i", f"{SCRIPT_DIR}/bg_music.wav",
        "-filter_complex",
        f"[1:a]volume=0.10,afade=t=in:st=0:d=2,afade=t=out:st={fade_start}:d=3[bg];"
        f"[0:a][bg]amix=inputs=2:duration=first:dropout_transition=0,"
        f"loudnorm=I=-16:TP=-1.5:LRA=11",
        "-b:a", "128k",
        final_output
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"  ERROR: {result.stderr[:500]}")
        return None
    
    # Check final duration
    final_dur_result = subprocess.run([
        "ffprobe", "-v", "quiet", "-show_entries", "format=duration",
        "-of", "csv=p=0", final_output
    ], capture_output=True, text=True)
    final_dur = float(final_dur_result.stdout.strip())
    
    print(f"\n✓ Final episode: {final_output}")
    print(f"  Duration: {final_dur:.1f}s ({final_dur/60:.1f}min)")
    print(f"  Size: {os.path.getsize(final_output) / 1024 / 1024:.1f}MB")
    
    return final_output


if __name__ == "__main__":
    assemble("ko")
