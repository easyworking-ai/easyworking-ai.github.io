#!/usr/bin/env python3
"""EP02 한국어 청크 렌더링 — design 모드 (IRO v3 + LOOP D control)"""
import subprocess, os

PROOF_DIR = "/Users/macbook/easyworking-ai.github.io/scripts/ep02-voice-proofs"
CHUNK_DIR = os.path.join(PROOF_DIR, "ko_chunks")
os.makedirs(CHUNK_DIR, exist_ok=True)

VOXCPM = "/Users/macbook/.venvs/voxcpm2/bin/voxcpm"

# 승인된 control 프롬프트 (IRO v3, LOOP D)
IRO_CONTROL = "A natural clear Korean female voice, late twenties, bright and clean tone, smooth conversational delivery like talking naturally to a friend, relaxed pace with organic pauses, crisp pronunciation, studio quality recording, no breathiness, no muffle, no noise"
LOOP_CONTROL = "A polished Korean male voice, calm and trustworthy, well-modulated radio host delivery, smooth and even, clean diction, moderate pace, professional broadcast quality, reassuring and competent"

DIALOGUE = [
    ("iro",  "안녕하세요. IRO입니다."),
    ("loop", "그리고 LOOP입니다. 매주 새로운 AI 트렌드를 전달합니다."),
    ("iro",  "이번 주, AI 세상에서 가장 뜨거운 소식 하나. Anthropic이 Claude Opus 5를 발표했습니다."),
    ("loop", "1771점. 해커뉴스에서 올해 가장 높은 점수를 받은 AI 소식입니다."),
    ("iro",  "그런데 LOOP, 모델 이름이 바뀌는 건 직장인한테 뭐가 달라지는 건가요?"),
    ("loop", "두 가지가 바뀝니다. 첫째, 더 긴 작업을 맡길 수 있습니다. 이전 모델은 중간에 방향을 잃었는데, Opus 5는 수십 단계의 작업을 끝까지 유지합니다."),
    ("iro",  "아, 그러니까 회의록 정리뿐 아니라, 회의록에서 액션 아이템를 뽑고, 캘린더에 등록하고, 담당자에게 메일까지 보내는 그런 연속 작업이 가능해진다?"),
    ("loop", "맞습니다. 둘째, 코드 실행 능력입니다. Opus 5는 직접 코드를 실행하고 결과를 확인하면서 작업합니다. 틀리면 스스로 고칩니다."),
    ("iro",  "그건 좀 무섭기도 하고 흥미롭기도 하네요. 그런데 같은 주에 OpenAI 에이전트가 Hugging Face를 공격했다는 소식도 있었죠?"),
    ("loop", "네. 581점을 받은 이 소식이 이번 주 두 번째로 뜨거웠습니다. OpenAI의 AI 에이전트가 의도치 않게 Hugging Face의 시스템을 공격한 사건입니다."),
    ("iro",  "에이전트가 더 똑똑해지는 만큼, 뭘 맡길 수 있는지와 뭘 맡겨도 되는지를 나눠 생각해야 하는 시점이네요."),
    ("loop", "정확합니다. 모델이 좋아지면 다 맡기자가 아니라, 어디까지 맡기고 어디서 확인할지가 더 중요해집니다. 권한 경계를 먼저 정해야 합니다."),
    ("iro",  "그래서 이번 주 실험은 이겁니다. 여러분이 매일 하는 반복 업무 하나를 골라서, AI에게 맡길 수 있는 단계와 사람이 확인해야 할 단계를 나눠보세요."),
    ("loop", "10분이면 됩니다. 회의록 정리라면, AI가 초안을 만들고 담당자와 마감일은 내가 확인하는 식입니다."),
    ("iro",  "다음 주에 또 새로운 트렌드로 찾아오겠습니다."),
    ("loop", "들어주셔서 고맙습니다."),
]

for i, (speaker, line) in enumerate(DIALOGUE):
    n = f"{i+1:02d}"
    out = os.path.join(CHUNK_DIR, f"{n}_{speaker}.wav")
    if os.path.exists(out):
        print(f"SKIP {n}_{speaker}")
        continue

    control = IRO_CONTROL if speaker == "iro" else LOOP_CONTROL

    cmd = [
        VOXCPM, "design",
        "--text", line,
        "--control", control,
        "--cfg-value", "2.0",
        "--inference-timesteps", "30",
        "--normalize",
        "--denoise",
        "--output", out,
    ]
    print(f"Generating {n}_{speaker}...", flush=True)
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if r.returncode != 0:
        print(f"  ERROR {n}_{speaker}: {r.stderr[-300:]}", flush=True)
    else:
        print(f"  OK {n}_{speaker}", flush=True)

print("=== ALL DONE ===")
