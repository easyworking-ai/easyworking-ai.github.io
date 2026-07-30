#!/usr/bin/env python3
"""
이로 보이스 "딱딱함" 개선용 A/B/C/D 샘플
같은 대사 2줄을 서로 다른 control로 렌더링 → 20초 샘플 비교
"""
import subprocess
from pathlib import Path

VOXCPM = "/Users/macbook/.venvs/voxcpm2/bin/voxcpm"
SCRIPT_DIR = Path("/Users/macbook/easyworking-ai.github.io/scripts/ep02-voice-proofs")

# 비교용 대사 (발표 + 반응 섞인 대표적 라인)
TEST_LINES = [
    "먼저 Claude Opus 5입니다. 이번 주 가장 화제였던 소식입니다.",
    "그러니까 검증된 결과를 가져온다는 거잖아요. 실무에서 신뢰하고 쓸 수 있다는 뜻이겠네요.",
]

# 4가지 변형
VARIANTS = {
    "A": (
        "A young Korean woman, mid twenties, podcast host energy. "
        "Bright, animated, energetic. Speaks fast and lively, "
        "lots of natural emphasis and emotion. "
        "She's excited about what she's saying. "
        "Close mic, studio quality. "
        "NOT formal, NOT stiff, NOT reading. "
        "Talking like she just can't wait to tell you something cool."
    ),
    "B": (
        "A friendly Korean woman in her late twenties. "
        "Warm, casual, chatty — like talking to a coworker over coffee. "
        "Her voice goes up and down with genuine interest. "
        "She laughs a little when she's amused. "
        "Relaxed, informal, spontaneous. "
        "NOT a news anchor. NOT reading a script. "
        "Just a natural, expressive person having fun talking."
    ),
    "C": (
        "A natural Korean female voice, mid twenties. "
        "Casual YouTuber style — bright, bouncy, expressive. "
        "High energy, talks with hands even though you can't see them. "
        "Sentences speed up when she's excited, slow down for emphasis. "
        "Warm, approachable, a little playful. "
        "Studio mic, clean audio. "
        "Conversational delivery, NOT narration."
    ),
    "D": (
        "A Korean woman, late twenties, radio DJ personality. "
        "Warm, confident, naturally animated. "
        "Her voice has texture and personality — not flat or monotone. "
        "She emphasizes key words naturally, "
        "pauses at unexpected moments like she's thinking. "
        "Professional but not stiff. "
        "She sounds genuinely entertained by what she's saying."
    ),
}

def render_batch(text_lines, control, output_dir, label):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    input_file = output_dir / "input.txt"
    input_file.write_text("\n".join(text_lines))
    subprocess.run([
        VOXCPM, "batch", "--input", str(input_file),
        "--output-dir", str(output_dir),
        "--control", control,
        "--cfg-value", "3.0",  # cfg 올림 → 더 표현력
        "--inference-timesteps", "30",
        "--normalize", "--denoise",
    ], check=True, capture_output=True, timeout=300)
    return sorted(output_dir.glob("output_*.wav"))

def make_sample(clips, output_mp3, label):
    """2개 클립을 간격과 함께 결합 → 20초 샘플"""
    work = output_mp3.parent / f"work_{label}"
    work.mkdir(exist_ok=True)
    norm = []
    for i, wav in enumerate(clips):
        dst = work / f"n{i}.wav"
        subprocess.run(["ffmpeg", "-y", "-i", str(wav), "-ar", "44100", "-ac", "1",
                         "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", str(dst)], capture_output=True)
        norm.append(dst)
    # 0.4초 간격
    sil = work / "sil.wav"
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i",
                     "anullsrc=channel_layout=mono:sample_rate=44100",
                     "-t", "0.5", str(sil)], capture_output=True)
    concat = work / "concat.txt"
    entries = []
    for i, n in enumerate(norm):
        entries.append(f"file '{n}'")
        if i < len(norm) - 1:
            entries.append(f"file '{sil}'")
    concat.write_text("\n".join(entries) + "\n")
    raw = work / "raw.wav"
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0",
                     "-i", str(concat), "-c", "copy", str(raw)], capture_output=True)
    subprocess.run(["ffmpeg", "-y", "-i", str(raw),
                     "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
                     "-b:a", "128k", str(output_mp3)], capture_output=True)
    dur = subprocess.run(["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
                           "-of", "csv=p=0", str(output_mp3)],
                          capture_output=True, text=True).stdout.strip()
    print(f"  {label}: {float(dur):.1f}s → {output_mp3.name}")

OUT = SCRIPT_DIR / "iro_stiff_test"
OUT.mkdir(exist_ok=True)

for label, control in VARIANTS.items():
    print(f"\n=== Variant {label} ===")
    clips = render_batch(TEST_LINES, control, OUT / f"variant_{label}", label)
    make_sample(clips, OUT / f"iro_sample_{label}.mp3", label)

print("\n=== ALL DONE ===")
