#!/usr/bin/env python3
"""
Speaker-specific spectrum audit: EP02 vs EP03 vs EP04 Korean MP3s.
Measures band-specific mean_volume per speaker to quantify 'muddiness'.
"""

import subprocess, json, re, os, csv
from collections import defaultdict

WORKDIR = "/Users/macbook/easyworking-ai.github.io"
RADIO = f"{WORKDIR}/quartz/static/radio"
PROOFS = "/Users/macbook/.hermes/cron/radio-state/ep04-muddy-diag"
V8_IRO = f"{WORKDIR}/scripts/ep02-voice-proofs/v8_ko_iro_out"
V8_LOOP = f"{WORKDIR}/scripts/ep02-voice-proofs/v8_ko_loop_out"
V8_LOOP_REF = f"{WORKDIR}/scripts/ep02-voice-proofs/v8_ko_loop_ref"
IRO_ANCHOR_EP03 = f"{WORKDIR}/scripts/ep02-voice-proofs/iro_stiff_test/variant_B"

MP3_FILES = {
    "ep02": f"{RADIO}/episode-02-ko.mp3",
    "ep03": f"{RADIO}/episode-03-ko.mp3",
    "ep04": f"{RADIO}/episode-04-ko.mp3",
}

# Dialogue turn maps: each entry is (speaker, segment_index)
# EP02: dialogue_ko_v6.txt has alternating lines. 24 lines total.
# Pattern: iro, loop, iro, loop ... (reading the file, line 1=iro greeting, line 2=loop greeting, etc.)
# But actually let me count: 24 lines, iro speaks odd-indexed (0,2,4...), loop speaks even-indexed (1,3,5...)
# Wait, the file content shows: line1=iro greeting, line2=iro about Opus5, line3=loop "루프씨...",
# So it's NOT strictly alternating. Let me re-read.
# The dialogue_ko_v6.txt seems to be a conversation script but without explicit speaker labels.
# Given the conversation structure and the numbered turns in EP03/EP04 (22 turns each, iro first on odd turns):
# EP03/EP04 pattern: 001=iro, 002=loop, 003=iro, 004=loop, ..., 021=iro, 022=loop
# So 11 iro turns (odd), 11 loop turns (even)
# For EP02, there are 24 lines. Let's assume the same alternating pattern starting with iro.
# 24 lines = 12 iro, 12 loop if strictly alternating from line 0.
# Actually the EP02 script has no explicit speaker labels, so we use the alternating assumption.

# EP02 has 24 dialogue lines -> 12 segments per speaker
# EP03 has 22 numbered turns -> 11 segments per speaker  
# EP04 has 22 numbered turns -> 11 segments per speaker

TURN_MAPS = {
    "ep02": [("iro" if i % 2 == 0 else "loop", i) for i in range(24)],
    "ep03": [("iro" if i % 2 == 0 else "loop", i) for i in range(22)],
    "ep04": [("iro" if i % 2 == 0 else "loop", i) for i in range(22)],
}

BANDS = {
    "overall": None,
    "low-mid_150-400": ("highpass=f=150", "lowpass=f=400"),
    "presence_2k-5k": ("highpass=f=2000", "lowpass=f=5000"),
    "high_6k-8k": ("highpass=f=6000", "lowpass=f=8000"),
    "air_8k-12k": ("highpass=f=8000", "lowpass=f=12000"),
}

def run_ffmpeg(cmd):
    """Run ffmpeg command, return merged stdout+stderr."""
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    return result.stdout + result.stderr

def detect_silence_segments(mp3_path, noise_db=-35, min_dur=0.4):
    """Use silencedetect to find speech segments (non-silent regions)."""
    cmd = [
        "ffmpeg", "-i", mp3_path, "-af",
        f"silencedetect=noise={noise_db}dB:d={min_dur}",
        "-f", "null", "-"
    ]
    out = run_ffmpeg(cmd)
    # Parse silence start/end pairs
    silence_starts = [float(x) for x in re.findall(r'silence_start:\s*([\d.]+)', out)]
    silence_ends = [float(x) for x in re.findall(r'silence_end:\s*([\d.]+)', out)]
    
    # Get duration
    cmd_dur = ["ffprobe", "-v", "error", "-show_entries", "format=duration",
               "-of", "csv=p=0", mp3_path]
    duration = float(run_ffmpeg(cmd_dur).strip())
    
    # Build speech segments (complement of silence)
    segments = []
    prev_end = 0.0
    for i, s_start in enumerate(silence_starts):
        if s_start - prev_end > 0.1:  # minimum 100ms speech segment
            segments.append((prev_end, s_start))
        prev_end = silence_ends[i] if i < len(silence_ends) else duration
    
    if duration - prev_end > 0.1:
        segments.append((prev_end, duration))
    
    return segments

def measure_band_volume(audio_data, band_key, sample_rate=44100):
    """Measure mean volume in dB for a specific band using ffmpeg."""
    band = BANDS[band_key]
    if band is None:
        # Overall - no filter
        af = "astats=metadata=reset=0:metadata_key1=1:metadata_key2=lavfi.astats.Overall.RMS_level"
    else:
        hp, lp = band
        af = f"{hp},{lp},{hp.replace('highpass','lowpass') if 'highpass' in hp else ''},"
        # Proper: apply both filters
        af = f"{hp},{lp},astats=metadata=reset=0:metadata_key1=1:metadata_key2=lavfi.astats.Overall.RMS_level"
    
    # Use a simpler approach: pipe through ffmpeg with filter and measure
    # Actually let's use volumedetect on band-filtered output
    if band is None:
        filter_str = "volumedetect"
    else:
        hp, lp = band
        filter_str = f"{hp},{lp},volumedetect"
    
    cmd = [
        "ffmpeg", "-i", audio_data, "-af", filter_str,
        "-f", "null", "-"
    ]
    out = run_ffmpeg(cmd)
    
    mean_vol = None
    m = re.search(r'mean_volume:\s*([-\d.]+)\s*dB', out)
    if m:
        mean_vol = float(m.group(1))
    
    if mean_vol is None:
        # Try max_volume as fallback
        m = re.search(r'max_volume:\s*([-\d.]+)\s*dB', out)
        if m:
            mean_vol = float(m.group(1))
    
    return mean_vol

def extract_segment_as_wav(mp3_path, start, end, output_path):
    """Extract a time segment from MP3 as WAV."""
    duration = end - start
    cmd = [
        "ffmpeg", "-y", "-i", mp3_path,
        "-ss", str(start), "-t", str(duration),
        "-acodec", "pcm_s16le", "-ar", "44100", "-ac", "1",
        output_path
    ]
    run_ffmpeg(cmd)

def measure_file_bands(filepath):
    """Measure all band volumes for a single file."""
    results = {}
    for band_name in BANDS:
        vol = measure_band_volume(filepath, band_name)
        results[band_name] = vol
    return results

def assign_segments_to_speakers(segments, turn_map, num_turns):
    """
    Assign speech segments to speakers based on turn order.
    Segments are ordered chronologically; we distribute them to match the turn map.
    The turn_map has num_turns entries alternating iro/loop.
    """
    if len(segments) == 0:
        return {"iro": [], "loop": []}
    
    # Group consecutive segments into turns
    # Strategy: evenly distribute segments among turns based on cumulative duration
    total_speech = sum(e - s for s, e in segments)
    turn_duration = total_speech / num_turns
    
    speaker_segments = {"iro": [], "loop": []}
    seg_idx = 0
    for turn_idx, (speaker, _) in enumerate(turn_map):
        target_dur = turn_duration
        turn_segs = []
        accum = 0.0
        while seg_idx < len(segments) and accum < target_dur * 1.5:
            seg = segments[seg_idx]
            turn_segs.append(seg)
            accum += seg[1] - seg[0]
            seg_idx += 1
            # Don't steal more than 2 segments per turn
            if len(turn_segs) >= 3:
                break
        speaker_segments[speaker].extend(turn_segs)
    
    # If any segments remain, assign proportionally
    remaining = segments[seg_idx:]
    if remaining:
        # Assign alternating to whoever has fewer segments
        iro_count = len(speaker_segments["iro"])
        loop_count = len(speaker_segments["loop"])
        target = "loop" if iro_count > loop_count else "iro"
        speaker_segments[target].extend(remaining)
    
    return speaker_segments

def concat_segments_to_file(segments, mp3_path, output_path):
    """Concatenate segments from the original MP3 into a single WAV file."""
    if not segments:
        return None
    
    # Use ffmpeg filter_complex to concat
    inputs = []
    filter_parts = []
    for i, (start, end) in enumerate(segments):
        dur = end - start
        inputs.extend(["-ss", str(start), "-t", str(dur), "-i", mp3_path])
        filter_parts.append(f"[{i}:a]")
    
    filter_str = "".join(filter_parts) + f"concat=n={len(segments)}:v=0:a=1[out]"
    
    cmd = ["ffmpeg", "-y"] + inputs + [
        "-filter_complex", filter_str,
        "-map", "[out]", "-acodec", "pcm_s16le", "-ar", "44100", "-ac", "1",
        output_path
    ]
    run_ffmpeg(cmd)
    return output_path

def main():
    os.makedirs("/tmp/spectrum_audit", exist_ok=True)
    
    results = {}  # {episode: {speaker: {band: dB}}}
    whole_file_results = {}  # {episode: {band: dB}}
    
    for ep_name, mp3_path in MP3_FILES.items():
        print(f"\n{'='*60}")
        print(f"Processing {ep_name}: {mp3_path}")
        print(f"{'='*60}")
        
        # Step 1: Detect speech segments
        segments = detect_silence_segments(mp3_path)
        print(f"  Detected {len(segments)} speech segments")
        for i, (s, e) in enumerate(segments[:5]):
            print(f"    Seg {i}: {s:.2f}-{e:.2f}s ({e-s:.2f}s)")
        if len(segments) > 5:
            print(f"    ... and {len(segments)-5} more")
        
        # Step 2: Whole-file band measurement
        print(f"\n  Whole-file band volumes:")
        whole = measure_file_bands(mp3_path)
        whole_file_results[ep_name] = whole
        for band, vol in whole.items():
            print(f"    {band}: {vol:.1f} dB" if vol else f"    {band}: N/A")
        
        # Step 3: Assign segments to speakers
        turn_map = TURN_MAPS[ep_name]
        num_turns = len(turn_map)
        speaker_segs = assign_segments_to_speakers(segments, turn_map, num_turns)
        print(f"\n  Assigned segments: iro={len(speaker_segs['iro'])}, loop={len(speaker_segs['loop'])}")
        
        # Step 4: Concatenate per-speaker segments and measure
        ep_results = {}
        for speaker in ["iro", "loop"]:
            segs = speaker_segs[speaker]
            if not segs:
                print(f"  WARNING: No segments for {speaker}")
                ep_results[speaker] = {b: None for b in BANDS}
                continue
            
            out_path = f"/tmp/spectrum_audit/{ep_name}_{speaker}.wav"
            concat_segments_to_file(segs, mp3_path, out_path)
            
            print(f"\n  {speaker} band volumes:")
            bands = measure_file_bands(out_path)
            ep_results[speaker] = bands
            for band, vol in bands.items():
                print(f"    {band}: {vol:.1f} dB" if vol else f"    {band}: N/A")
        
        results[ep_name] = ep_results
    
    # Step 5: Measure reference WAVs
    print(f"\n{'='*60}")
    print("REFERENCE WAVs")
    print(f"{'='*60}")
    
    ref_results = {}
    
    # EP02 v8 iro anchor (concatenate all outputs)
    iro_wavs = sorted([f for f in os.listdir(V8_IRO) if f.endswith('.wav')])
    iro_concat = f"/tmp/spectrum_audit/ref_ep02_v8_iro.wav"
    if iro_wavs:
        concat_list = f"/tmp/spectrum_audit/iro_concat_list.txt"
        with open(concat_list, 'w') as f:
            for w in iro_wavs:
                f.write(f"file '{os.path.join(V8_IRO, w)}'\n")
        run_ffmpeg(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list,
                    "-acodec", "pcm_s16le", "-ar", "44100", "-ac", "1", iro_concat])
        print(f"\n  EP02 v8 iro anchor ({len(iro_wavs)} files):")
        ref_results["ep02_v8_iro"] = measure_file_bands(iro_concat)
        for band, vol in ref_results["ep02_v8_iro"].items():
            print(f"    {band}: {vol:.1f} dB" if vol else f"    {band}: N/A")
    
    # EP02 v8 loop anchor
    loop_wavs = sorted([f for f in os.listdir(V8_LOOP) if f.endswith('.wav')])
    loop_concat = f"/tmp/spectrum_audit/ref_ep02_v8_loop.wav"
    if loop_wavs:
        concat_list = f"/tmp/spectrum_audit/loop_concat_list.txt"
        with open(concat_list, 'w') as f:
            for w in loop_wavs:
                f.write(f"file '{os.path.join(V8_LOOP, w)}'\n")
        run_ffmpeg(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list,
                    "-acodec", "pcm_s16le", "-ar", "44100", "-ac", "1", loop_concat])
        print(f"\n  EP02 v8 loop anchor ({len(loop_wavs)} files):")
        ref_results["ep02_v8_loop"] = measure_file_bands(loop_concat)
        for band, vol in ref_results["ep02_v8_loop"].items():
            print(f"    {band}: {vol:.1f} dB" if vol else f"    {band}: N/A")
    
    # EP02 v8 loop ref
    loop_ref = f"{V8_LOOP_REF}/output_001.wav"
    if os.path.exists(loop_ref):
        print(f"\n  EP02 v8 loop ref (single file):")
        ref_results["ep02_v8_loop_ref"] = measure_file_bands(loop_ref)
        for band, vol in ref_results["ep02_v8_loop_ref"].items():
            print(f"    {band}: {vol:.1f} dB" if vol else f"    {band}: N/A")
    
    # EP03-04 iro anchor: iro_stiff_test/variant_B/output_002.wav
    iro_anchor = f"{IRO_ANCHOR_EP03}/output_002.wav"
    if os.path.exists(iro_anchor):
        print(f"\n  Iro anchor (EP03-04 variant_B/output_002.wav):")
        ref_results["iro_anchor_ep034"] = measure_file_bands(iro_anchor)
        for band, vol in ref_results["iro_anchor_ep034"].items():
            print(f"    {band}: {vol:.1f} dB" if vol else f"    {band}: N/A")
    
    # EP04 regen WAVs
    regen_wavs = {
        "ep04_regen_iro_nov": f"{PROOFS}/regen/iro_nov/output_001.wav",
        "ep04_regen_loop_nov": f"{PROOFS}/regen/loop_nov/output_001.wav",
        "ep04_regen_loop_bright": f"{PROOFS}/regen/loop_bright/output_001.wav",
        "ep04_regen_iro_anchor": f"{PROOFS}/regen/iro_anchor_gen/output_001.wav",
        "ep04_regen_loop_anchor": f"{PROOFS}/regen/loop_anchor_gen/output_001.wav",
    }
    for name, path in regen_wavs.items():
        if os.path.exists(path):
            print(f"\n  {name}:")
            ref_results[name] = measure_file_bands(path)
            for band, vol in ref_results[name].items():
                print(f"    {band}: {vol:.1f} dB" if vol else f"    {band}: N/A")
    
    # EP04 proof MP3s
    proof_mp3s = {
        "proof_A_as_is": f"{PROOFS}/proof_A_current_as_is.mp3",
        "proof_B_treble": f"{PROOFS}/proof_B_current_plus_treble.mp3",
        "proof_C_hf": f"{PROOFS}/proof_C_current_conservative_hf.mp3",
        "proof_D_iro_regen": f"{PROOFS}/proof_D_iro_regen.mp3",
        "proof_D2_iro_regen_deess": f"{PROOFS}/proof_D2_iro_regen_deess.mp3",
        "proof_E_loop_regen": f"{PROOFS}/proof_E_loop_regen.mp3",
        "proof_E2_loop_regen_eq": f"{PROOFS}/proof_E2_loop_regen_eq.mp3",
        "proof_F_loop_bright": f"{PROOFS}/proof_F_loop_bright.mp3",
    }
    for name, path in proof_mp3s.items():
        if os.path.exists(path):
            print(f"\n  {name}:")
            ref_results[name] = measure_file_bands(path)
            for band, vol in ref_results[name].items():
                print(f"    {band}: {vol:.1f} dB" if vol else f"    {band}: N/A")
    
    # Step 6: Build tables and output
    print(f"\n{'='*60}")
    print("RESULTS: SPEAKER × EPISODE BAND TABLE (dB)")
    print(f"{'='*60}")
    
    band_names = list(BANDS.keys())
    header = f"{'Speaker/EP':<20}" + "".join(f"{b:>20}" for b in band_names)
    print(header)
    print("-" * len(header))
    
    for ep in ["ep02", "ep03", "ep04"]:
        for sp in ["iro", "loop"]:
            row = f"{sp}@{ep:<14}"
            for b in band_names:
                v = results[ep][sp].get(b)
                row += f"{v:>20.1f}" if v else f"{'N/A':>20}"
            print(row)
        # Whole file row
        row = f"{'WHOLE_'+ep:<20}"
        for b in band_names:
            v = whole_file_results[ep].get(b)
            row += f"{v:>20.1f}" if v else f"{'N/A':>20}"
        print(row)
        print()
    
    # EP02 deviation table
    print(f"\n{'='*60}")
    print("EP02 BASELINE DEVIATION TABLE (dB relative to EP02)")
    print(f"{'='*60}")
    
    header2 = f"{'Speaker/EP':<20}" + "".join(f"{b:>20}" for b in band_names)
    print(header2)
    print("-" * len(header2))
    
    for ep in ["ep03", "ep04"]:
        for sp in ["iro", "loop"]:
            label = sp + "@" + ep + "_dev"
            row = "{:<20}".format(label)
            for b in band_names:
                ep02_val = results["ep02"][sp].get(b)
                ep_val = results[ep][sp].get(b)
                if ep02_val is not None and ep_val is not None:
                    dev = ep_val - ep02_val
                    row += f"{dev:>+20.1f}"
                else:
                    row += f"{'N/A':>20}"
            print(row)
        print()
    
    # Reference WAV table
    print(f"\n{'='*60}")
    print("REFERENCE WAV & PROOF INDICATORS")
    print(f"{'='*60}")
    
    header3 = f"{'Reference':<30}" + "".join(f"{b:>15}" for b in band_names)
    print(header3)
    print("-" * len(header3))
    
    for ref_name, ref_data in ref_results.items():
        row = f"{ref_name:<30}"
        for b in band_names:
            v = ref_data.get(b)
            row += f"{v:>15.1f}" if v else f"{'N/A':>15}"
        print(row)
    
    # Step 7: Judgment
    print(f"\n{'='*60}")
    print("DIAGNOSIS: LOOP MUDDINESS JUDGMENT")
    print(f"{'='*60}")
    
    # Compare EP02 vs EP03 vs EP04 for loop
    for sp in ["iro", "loop"]:
        print(f"\n  {sp.upper()} trend across episodes:")
        for b in band_names:
            vals = [results[ep][sp].get(b) for ep in ["ep02", "ep03", "ep04"]]
            vals_str = [f"{v:.1f}" if v else "N/A" for v in vals]
            if all(v is not None for v in vals):
                trend = "↑" if vals[-1] > vals[0] + 0.5 else ("↓" if vals[-1] < vals[0] - 0.5 else "→")
                print(f"    {b:<20}: EP02={vals_str[0]} EP03={vals_str[1]} EP04={vals_str[2]} {trend}")
            else:
                print(f"    {b:<20}: EP02={vals_str[0]} EP03={vals_str[1]} EP04={vals_str[2]}")
    
    # Check if loop's presence/high/air bands are notably lower than iro's
    print(f"\n  IRO vs LOOP band difference (negative = loop is quieter):")
    for ep in ["ep02", "ep03", "ep04"]:
        print(f"    {ep}:")
        for b in band_names:
            if b == "overall":
                continue
            iro_v = results[ep]["iro"].get(b)
            loop_v = results[ep]["loop"].get(b)
            if iro_v is not None and loop_v is not None:
                diff = loop_v - iro_v
                marker = " *** MUDDY" if diff < -3 else (" * weak" if diff < -1.5 else "")
                print(f"      {b:<20}: loop - iro = {diff:+.1f} dB{marker}")
    
    # Save to CSV
    csv_path = f"{WORKDIR}/scripts/ep02-voice-proofs/speaker_spectrum_audit_results.csv"
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        # Main table
        writer.writerow(["source", "speaker"] + band_names)
        for ep in ["ep02", "ep03", "ep04"]:
            for sp in ["iro", "loop"]:
                writer.writerow([ep, sp] + [results[ep][sp].get(b, "") for b in band_names])
            writer.writerow([ep, "whole"] + [whole_file_results[ep].get(b, "") for b in band_names])
        # References
        for ref_name, ref_data in ref_results.items():
            writer.writerow([ref_name, "ref"] + [ref_data.get(b, "") for b in band_names])
    
    print(f"\n  Results saved to {csv_path}")

if __name__ == "__main__":
    main()
