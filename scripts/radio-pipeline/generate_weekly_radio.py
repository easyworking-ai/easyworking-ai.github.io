#!/usr/bin/env python3
"""
easyworking-ai.github.io 주간 라디오 자동 생성 파이프라인

사용법:
  python3 generate_weekly_radio.py [episode_number]

동작 순서:
  1. Hacker News API에서 최근 7일 AI 뉴스 수집
  2. 상위 1~2개 토픽으로 IRO×LOOP 대화 대본 작성 (3개 언어)
  3. VoxCPM2 batch 모드로 각 언어별 음성 생성
  4. ffmpeg로 인터리빙 결합 + loudnorm 정규화
  5. 사이트에 MP3 반영 + git push

의존성:
  - VoxCPM2: /Users/macbook/.venvs/voxcpm2/bin/voxcpm
  - ffmpeg: 시스템 설치
"""
import json, os, subprocess, time, urllib.request, sys
from pathlib import Path

# ─── 설정 ──────────────────────────────────────────────────
SITE_DIR = Path("/Users/macbook/easyworking-ai.github.io")
RADIO_DIR = SITE_DIR / "quartz" / "static" / "radio"
SCRIPT_DIR = SITE_DIR / "scripts" / "radio-pipeline"
VOXCPM = "/Users/macbook/.venvs/voxcpm2/bin/voxcpm"

VOICE_CONTROLS = {
    "ko": {
        "iro": "A natural clear Korean female voice, late twenties, bright and clean tone, smooth conversational delivery like talking naturally to a friend, relaxed pace with organic pauses, crisp pronunciation, studio quality recording, no breathiness, no muffle, no noise",
        "loop": "A polished Korean male voice, calm and trustworthy, well-modulated radio host delivery, smooth and even, clean diction, moderate pace, professional broadcast quality, reassuring and competent",
    },
    "en": {
        "iro": "A natural clear English female voice, late twenties, bright and clean tone, smooth conversational delivery like talking naturally to a friend, relaxed pace with organic pauses, crisp pronunciation, studio quality recording, no breathiness, no muffle, no noise",
        "loop": "A polished English male voice, calm and trustworthy, well-modulated radio host delivery, smooth and even, clean diction, moderate pace, professional broadcast quality, reassuring and competent",
    },
    "ja": {
        "iro": "A natural clear Japanese female voice, late twenties, bright and clean tone, smooth conversational delivery like talking naturally to a friend, relaxed pace with organic pauses, crisp pronunciation, studio quality recording, no breathiness, no muffle, no noise",
        "loop": "A polished Japanese male voice, calm and trustworthy, well-modulated radio host delivery, smooth and even, clean diction, moderate pace, professional broadcast quality, reassuring and competent",
    },
}

def fetch_top_ai_news(limit=5):
    """Hacker News에서 최근 7일 AI 뉴스 수집"""
    ts_week_ago = int(time.time()) - 7 * 24 * 3600
    url = f"https://hn.algolia.com/api/v1/search?query=AI+LLM&tags=story&numericFilters=created_at_i>{ts_week_ago},points>30&hitsPerPage={limit}"
    req = urllib.request.Request(url, headers={"User-Agent": "ewa-radio/1.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read())
    
    hits = []
    for hit in data.get("hits", []):
        hits.append({
            "title": hit.get("title", ""),
            "points": hit.get("points", 0),
            "url": hit.get("url", ""),
        })
    hits.sort(key=lambda x: x["points"], reverse=True)
    return hits

def write_dialogue_files(news, ep_num, out_dir):
    """뉴스를 기반으로 3개 언어 대본 작성 (IRO/LOOP 각각 별도 파일)"""
    top1 = news[0] if len(news) > 0 else {"title": "AI 모델 개선 소식", "points": 0}
    top2 = news[1] if len(news) > 1 else None
    
    # 이 부분은 LLM이 대본을 작성해야 함 — cron에서는 agent가 처리
    # 여기서는 템플릿만 반환
    return top1, top2

def run_voxcpm_batch(input_file, output_dir, control, lang):
    """VoxCPM2 batch 모드 실행"""
    os.makedirs(output_dir, exist_ok=True)
    cmd = [
        VOXCPM, "batch",
        "--input", input_file,
        "--output-dir", output_dir,
        "--control", control,
        "--cfg-value", "2.0",
        "--inference-timesteps", "30",
        "--normalize",
        "--denoise",
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
    return r.returncode == 0

def concatenate_episode(iro_dir, loop_dir, output_path, silence_dur=0.35):
    """IRO와 LOOP 청크를 인터리빙 결합 + loudnorm"""
    work_dir = os.path.dirname(output_path)
    os.makedirs(work_dir, exist_ok=True)
    
    # silence 파일 생성
    silence = os.path.join(work_dir, "silence.wav")
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", f"anullsrc=channel_layout=mono:sample_rate=48000",
        "-t", str(silence_dur), silence
    ], capture_output=True)
    
    # concat list 생성
    iro_files = sorted(Path(iro_dir).glob("output_*.wav"))
    loop_files = sorted(Path(loop_dir).glob("output_*.wav"))
    
    concat_list = os.path.join(work_dir, "concat_list.txt")
    with open(concat_list, "w") as f:
        for i in range(min(len(iro_files), len(loop_files))):
            f.write(f"file '{iro_files[i]}'\n")
            f.write(f"file '{silence}'\n")
            f.write(f"file '{loop_files[i]}'\n")
            f.write(f"file '{silence}'\n")
    
    # concat → raw wav
    raw = os.path.join(work_dir, "raw.wav")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", concat_list, "-c", "copy", raw
    ], capture_output=True)
    
    # loudnorm → MP3
    subprocess.run([
        "ffmpeg", "-y", "-i", raw,
        "-af", "loudnorm=I=-18:TP=-1.5:LRA=8",
        "-ar", "48000", "-ac", "1", "-b:a", "192k",
        output_path
    ], capture_output=True)
    
    return os.path.exists(output_path)

if __name__ == "__main__":
    ep = sys.argv[1] if len(sys.argv) > 1 else "03"
    print(f"=== Weekly Radio Pipeline EP{ep} ===")
    
    # 1. 뉴스 수집
    news = fetch_top_ai_news()
    print(f"Top news: {news[0]['title']} ({news[0]['points']}pts)")
    
    # 2. 대본은 cron agent가 작성 (이 스크립트는 템플릿)
    print("대본 작성은 cron agent가 처리합니다")
    print(json.dumps(news[:3], ensure_ascii=False, indent=2))
