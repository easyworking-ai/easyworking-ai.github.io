#!/usr/bin/env python3
"""
30초 샘플 테스트 — 3가지 timesteps × 2 보이스 조합으로 최적값 찾기
"""
import subprocess
from pathlib import Path

VOXCPM = "/Users/macbook/.venvs/voxcpm2/bin/voxcpm"
SCRIPT_DIR = Path("/Users/macbook/easyworking-ai.github.io/scripts/ep02-voice-proofs")
OUT = SCRIPT_DIR / "sample_test"
OUT.mkdir(exist_ok=True)

IRO_CTRL = "A natural Korean female voice, early thirties, having a real conversation with a colleague. Warm, thoughtful, slightly curious. Speaks at a relaxed pace like she's sitting across from you. Close mic, clean recording. Not reading a script — talking naturally with genuine interest."

LOOP_CTRL = "A natural Korean male voice, mid thirties, warm and engaged in conversation. Not a news anchor — more like a knowledgeable friend explaining something with genuine enthusiasm. Relaxed, personable, occasionally pauses to think. Close mic, clean recording. Conversational, not robotic."

# 짧은 대화 — 이로 질문, 루프 답변
IRO_LINE = "루프 씨, 이 모덨이 기존과 근본적으로 다른 점이 뭔가요?"
LOOP_LINE = "가장 큰 변화는, 수십 단계 작업을 끝까지 유지한다는 거예요. 이전 모델들은 대여섯 단계만 돼도 길을 잃었거든요."

# 테스트할 timesteps
TIMESTEPS = [30, 50, 80]

def render(text, ctrl, out_file, timesteps):
    """단일 라인 렌더"""
    input_file = OUT / f"_input_{out_file.stem}.txt"
    input_file.write_text(text)

    subprocess.run([
        VOXCPM, "batch",
        "--input", str(input_file),
        "--output-dir", str(OUT),
        "--control", ctrl,
        "--cfg-value", "2.0",
        "--inference-timesteps", str(timesteps),
        "--normalize", "--denoise",
    ], check=True, capture_output=True, timeout=300)

    # batch는 output_001.wav로 저장
    generated = OUT / "output_001.wav"
    if generated.exists():
        generated.rename(out_file)
    input_file.unlink()


def main():
    print("=== IRO samples ===")
    for ts in TIMESTEPS:
        out = OUT / f"iro_ts{ts}.wav"
        print(f"  timesteps={ts}...", end="", flush=True)
        render(IRO_LINE, IRO_CTRL, out, ts)

        # 볼륨 체크
        vol = subprocess.run(
            ["ffmpeg", "-i", str(out), "-af", "volumedetect", "-f", "null", "-"],
            capture_output=True, text=True
        ).stderr
        mean = [l for l in vol.split("\n") if "mean_volume" in l]
        print(f" done ({mean[0].strip() if mean else '?'})")

    print("\n=== LOOP samples ===")
    for ts in TIMESTEPS:
        out = OUT / f"loop_ts{ts}.wav"
        print(f"  timesteps={ts}...", end="", flush=True)
        render(LOOP_LINE, LOOP_CTRL, out, ts)

        vol = subprocess.run(
            ["ffmpeg", "-i", str(out), "-af", "volumedetect", "-f", "null", "-"],
            capture_output=True, text=True
        ).stderr
        mean = [l for l in vol.split("\n") if "mean_volume" in l]
        print(f" done ({mean[0].strip() if mean else '?'})")

    # 30초 샘플 조립: iro_ts30 → loop_ts30 → (gap)
    print("\n=== Assembling 30s samples ===")
    for ts in TIMESTEPS:
        work = OUT / f"sample_ts{ts}"
        work.mkdir(exist_ok=True)

        # Normalize
        for name, src in [("iro", OUT / f"iro_ts{ts}.wav"), ("loop", OUT / f"loop_ts{ts}.wav")]:
            subprocess.run([
                "ffmpeg", "-y", "-i", str(src), "-ar", "44100", "-ac", "1",
                "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
                str(work / f"{name}.wav")
            ], capture_output=True)

        # Silence
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi",
            "-i", "anullsrc=channel_layout=mono:sample_rate=44100",
            "-t", "0.4", str(work / "sil.wav")
        ], capture_output=True)

        # Concat
        concat = work / "concat.txt"
        concat.write_text(f"file '{work}/iro.wav'\nfile '{work}/sil.wav'\nfile '{work}/loop.wav'\n")

        subprocess.run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", str(concat), "-c", "copy",
            str(work / "raw.wav")
        ], capture_output=True)

        # loudnorm
        subprocess.run([
            "ffmpeg", "-y", "-i", str(work / "raw.wav"),
            "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
            "-b:a", "128k",
            str(OUT / f"sample_ts{ts}.mp3")
        ], capture_output=True)

        dur = subprocess.run(
            ["ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0",
             str(OUT / f"sample_ts{ts}.mp3")],
            capture_output=True, text=True
        ).stdout.strip()
        print(f"  ts{ts}: {dur}s")

    print("\n=== DONE ===")
    print(f"Samples in: {OUT}")


if __name__ == "__main__":
    main()
