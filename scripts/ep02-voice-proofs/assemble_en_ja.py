#!/usr/bin/env python3
"""
Assemble EN and JA episodes from VoxCPM2 batch chunks.
Each script has 13 lines with alternating speakers.
We pick the correct voice (IRO or LOOP) for each line.
"""
import subprocess
import os

SCRIPT_DIR = "/Users/macbook/easyworking-ai.github.io/scripts/ep02-voice-proofs"
OUTPUT_DIR = "/Users/macbook/easyworking-ai.github.io/quartz/static/radio"

# Speaker assignment per line index (0-based)
# Based on script content analysis
SPEAKER_MAP = {
    # EN: 13 lines
    "en": [
        "iro",   # 0: "Every week, IRO and LOOP..."
        "iro",   # 1: "Hacker News scored 1771..."
        "iro",   # 2: "So LOOP, a new model name..."
        "loop",  # 3: "Two things. First..."
        "iro",   # 4: "Right. So beyond meeting notes..."
        "loop",  # 5: "Second, code execution..."
        "iro",   # 6: "That's both exciting..."
        "loop",  # 7: "Yes. 581 points..."
        "iro",   # 8: "As agents get smarter..."
        "loop",  # 9: "Exactly. Better models..."
        "iro",   # 10: "So this week's experiment..."
        "loop",  # 11: "Ten minutes is enough..."
        "iro",   # 12: "See you next week..."
    ],
    "ja": [
        "iro",   # 0: "毎週、IROとLOOPが..."
        "iro",   # 1: "ハッカーニュースで1771..."
        "iro",   # 2: "でもLOOP、モデル名が..."
        "loop",  # 3: "二つ変わります..."
        "iro",   # 4: "なるほど。議事録の整理..."
        "loop",  # 5: "二つ目、コード実行..."
        "iro",   # 6: "それは少し怖くもある..."
        "loop",  # 7: "はい。581ポイント..."
        "iro",   # 8: "エージェントが賢くなるほど..."
        "loop",  # 9: "その通りです..."
        "iro",   # 10: "今週の実験はこれ..."
        "loop",  # 11: "10分でできます..."
        "iro",   # 12: "それでは来週..."
    ],
}

# Section breaks after these indices
SECTION_BREAKS = {2, 5, 8, 9}


def get_chunk(lang, speaker, idx):
    """Get WAV path for a specific chunk."""
    dirname = f"{lang}_{speaker}_batch"
    return f"{SCRIPT_DIR}/{dirname}/output_{idx+1:03d}.wav"


def assemble(lang):
    """Assemble episode for a language."""
    speaker_map = SPEAKER_MAP[lang]
    work = f"{SCRIPT_DIR}/{lang}_assemble_v2"
    os.makedirs(work, exist_ok=True)

    # Normalize chunks
    print(f"\n=== Assembling {lang.upper()} ===")
    norm_files = []
    for i, speaker in enumerate(speaker_map):
        src = get_chunk(lang, speaker, i)
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
        print(f"  seg_{i:03d} ({speaker}): {os.path.getsize(src)//1024}KB")

    # Create silence files
    for dur, name in [(0.3, "sil_short"), (0.6, "sil_mid"), (1.2, "sil_section")]:
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi", "-i",
            f"anullsrc=channel_layout=mono:sample_rate=44100",
            "-t", str(dur), f"{work}/{name}.wav"
        ], capture_output=True)

    # Build concat list
    concat_entries = [
        f"file '{SCRIPT_DIR}/intro_sting.wav'",
        f"file '{work}/sil_mid.wav'",
    ]

    for i, (wav_file, speaker) in enumerate(norm_files):
        concat_entries.append(f"file '{wav_file}'")

        if i < len(norm_files) - 1:
            if i in SECTION_BREAKS:
                concat_entries.append(f"file '{work}/sil_section.wav'")
                concat_entries.append(f"file '{SCRIPT_DIR}/transition.wav'")
                concat_entries.append(f"file '{work}/sil_section.wav'")
            else:
                next_speaker = norm_files[i+1][1]
                if speaker != next_speaker:
                    concat_entries.append(f"file '{work}/sil_mid.wav'")
                else:
                    concat_entries.append(f"file '{work}/sil_short.wav'")

    concat_entries.append(f"file '{work}/sil_section.wav'")
    concat_entries.append(f"file '{SCRIPT_DIR}/outro_sting.wav'")

    # Concat
    concat_file = f"{work}/concat.txt"
    with open(concat_file, "w") as f:
        f.write("\n".join(concat_entries))

    raw_output = f"{work}/{lang}_raw.wav"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", concat_file, "-c", "copy", raw_output
    ], capture_output=True)

    # Check raw duration
    dur_result = subprocess.run([
        "ffprobe", "-v", "quiet", "-show_entries", "format=duration",
        "-of", "csv=p=0", raw_output
    ], capture_output=True, text=True)
    raw_dur = float(dur_result.stdout.strip())
    print(f"  Raw duration: {raw_dur:.1f}s ({raw_dur/60:.1f}min)")

    # Mix with background music
    fade_start = max(0, raw_dur - 3)
    final_output = f"{OUTPUT_DIR}/episode-02-{lang}.mp3"
    subprocess.run([
        "ffmpeg", "-y",
        "-i", raw_output,
        "-i", f"{SCRIPT_DIR}/bg_music.wav",
        "-filter_complex",
        f"[1:a]volume=0.10,afade=t=in:st=0:d=2,afade=t=out:st={fade_start}:d=3[bg];"
        f"[0:a][bg]amix=inputs=2:duration=first:dropout_transition=0,"
        f"loudnorm=I=-16:TP=-1.5:LRA=11",
        "-b:a", "128k",
        final_output
    ], capture_output=True)

    # Final check
    final_dur_result = subprocess.run([
        "ffprobe", "-v", "quiet", "-show_entries", "format=duration",
        "-of", "csv=p=0", final_output
    ], capture_output=True, text=True)
    final_dur = float(final_dur_result.stdout.strip())
    print(f"  ✓ Final: {final_dur:.1f}s ({final_dur/60:.1f}min)")
    print(f"  Size: {os.path.getsize(final_output)/1024/1024:.1f}MB")

    return final_output


if __name__ == "__main__":
    for lang in ["en", "ja"]:
        assemble(lang)
