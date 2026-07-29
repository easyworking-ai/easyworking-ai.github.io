#!/usr/bin/env python3
"""
Assemble EP02 KO v3 from consistent-voice clips.
iro_v3.txt and loop_v3.txt have different line counts because
some lines belong to IRO(이로) and some to LOOP(루프).

We map each output clip to its position in the dialogue flow.
"""
import subprocess
import os
from pathlib import Path

SCRIPT_DIR = Path("/Users/macbook/easyworking-ai.github.io/scripts/ep02-voice-proofs")
OUTPUT_DIR = Path("/Users/macbook/easyworking-ai.github.io/quartz/static/radio")
WORK_DIR = SCRIPT_DIR / "ko_v3_assemble"
WORK_DIR.mkdir(exist_ok=True)

# Dialogue order: (speaker, clip_index)
# Based on iro_v3.txt (14 lines) and loop_v3.txt (11 lines)
# Reading the scripts to determine the conversation flow:
#
# IRO:  안녕, 이로입니다... (1)
# IRO:  이번 주 최고 화제... (2)
# IRO:  루프, 직장인에게... (3) ← 이로가 루프에게 질문
# LOOP: 두 가지입니다... (1)
# IRO:  이전까지는 AI가... (4) ← 이로가 반응
# LOOP: 맞습니다. 각 단계를... (2)
# IRO:  근데 같은 주에... (5) ← 이로가 전환
# LOOP: 581점을 받은... (3)
# LOOP: 능력은 있었지만... (4) ← 루프가 계속
# IRO:  능력이 커질수록... (6) ← 이로가 관점
# LOOP: 모델이 좋아지면... (5) ← 루프가 정리 (loop_v3 line 8)
# IRO:  그래서 이번 주 실험... (7)
# LOOP: 이번 주 다른 소식... (6) ← 루프가 뉴스 라운드업 (loop_v3 line 9)
# IRO:  회의록이면... (8) ← 이로가 보충... wait

# Let me re-read carefully:

# iro_v3.txt:
# 1: 안녕, 이로입니다. 오늘은 AI 세상에서...
# 2: 이번 주 최고 화제, Claude Opus 5...
# 3: 루프, 직장인에게 실제로 뭘 바꿔주는 거야?
# 4: 이전까지는 AI가 회의록 정리하고 끝이었잖아? 이제는 액션 아이템을...
# 5: 근데 같은 주에 무서운 뉴스도 있었어. OpenAI 에이전트가...
# 6: 능력이 커질수록 권한 경계를 먼저 정해야 해...
# 7: 그래서 이번 주 실험입니다. 매일 하는 반복 업무를...
# 8: 회의록이면 AI가 초안을 만들고, 담당자와 마감일은 사람이 확인합니다. 10분이면 됩니다.
# 9: 다음 주에 또 새로운 트렌드로 찾아오겠습니다...
# 10: 들어주셔서 고맙습니다.

# Wait, iro_v3.txt has 14 lines not 10. Let me re-check.

DIALOGUE = [
    # (speaker, clip_number_1indexed)
    ("iro", 1),    # 안녕, 이로입니다
    ("iro", 2),    # 이번 주 최고 화제, Claude Opus 5
    ("iro", 3),    # 루프, 직장인에게 실제로 뭘 바꿔주는 거야?
    ("loop", 1),   # 두 가지입니다. 첫째, 긴 작업을 끝까지 유지합니다.
    ("iro", 4),    # 이전까지는 AI가 회의록 정리하고 끝이었잖아?
    ("loop", 2),   # 맞습니다. 각 단계를 사람이 연결하던 시대가 끝났습니다.
    ("iro", 5),    # 근데 같은 주에 무서운 뉴스도 있었어.
    ("loop", 3),   # 581점을 받은 이 소식이 두 번째로 뜨거웠습니다.
    ("loop", 4),   # 능력은 있었지만 어디로 향할지를 통제하지 못한 거죠.
    ("iro", 6),    # 능력이 커질수록 권한 경계를 먼저 정해야 해.
    ("loop", 5),   # 맞습니다. 에이전트가 자율적으로 움직이는 영역이 넓어질수록...
    ("iro", 7),    # 그래서 이번 주 실험입니다.
    ("loop", 6),   # 581점을 받은 두 번째 핫 이슈... wait, no.
]

# Actually, let me just re-read both files and map properly
IRO_LINES = [
    "안녕, 이로입니다",
    "이번 주 최고 화제",
    "루프, 직장인에게",
    "이전까지는 AI가 회의록",
    "근데 같은 주에 무서운",
    "능력이 커질수록 권한",
    "그래서 이번 주 실험",
    "회의록이면 AI가 초안",
    "다음 주에 또 새로운",
    "들어주셔서 고맙습니다",
]

LOOP_LINES = [
    "그리고 루프입니다",
    "핵심 변화는 두 가지",
    "이전 모델은 다섯 단계",
    "정확한 지적입니다",
    "맞습니다. 에이전트가 자율적으로",
    "581점을 받은 두 번째",
    "능력은 있었지만 방향을",
    "모델이 좋아지면 전부",
    "이번 주 다른 소식을 빠르게",
    "좋은 실험입니다",
    "들어주셔서 고맙습니다",
]

# Actually the iro_v3.txt has 14 lines and loop_v3.txt has 11 lines.
# But my IRO_LINES list above only has 10 entries because I was summarizing.
# Let me just use the actual clip files - they're numbered 001-014 and 001-011.
# The conversation flow based on the actual script content is:

# Read actual scripts
iro_text = (SCRIPT_DIR / "iro_v3.txt").read_text().strip().split("\n")
loop_text = (SCRIPT_DIR / "loop_v3.txt").read_text().strip().split("\n")

# Map conversation flow by matching content to the correct speaker
# The dialogue alternates but not strictly. Based on script content:
FLOW = [
    ("iro", 1),    # 안녕, 이로입니다
    ("iro", 2),    # 이번 주 최고 화제, Claude Opus 5
    ("iro", 3),    # 루프, 직장인에게 실제로 뭘 바꿔주는 거야?
    ("loop", 1),   # 그리고 루프입니다... → No wait, loop 1 is "그리고 루프입니다"
    # Actually loop line 1 is the intro. But in the flow, loop's first response to iro's question should be...
    # Let me re-examine: iro_v3.txt line 3 asks 루프 a question.
    # loop_v3.txt line 1 = "그리고 루프입니다. 오늘 다룰 주제는..."
    # This doesn't answer the question. It's an intro line.
    # So the actual flow is:
]

# Let me just read both scripts properly and interleave based on content
print("=== IRO lines ===")
for i, line in enumerate(iro_text):
    if line.strip():
        print(f"  {i+1}: {line.strip()[:50]}...")

print("\n=== LOOP lines ===")
for i, line in enumerate(loop_text):
    if line.strip():
        print(f"  {i+1}: {line.strip()[:50]}...")

# Based on actual content, the conversation flow is:
# IRO 1: 안녕, 이로입니다. (intro)
# IRO 2: 이번 주 최고 화제, Claude Opus 5... (topic intro)
# IRO 3: 루프, 직장인에게 실제로 뭘 바꿔주는 거야? (question to loop)
# LOOP 1: 그리고 루프입니다... → No, this is loop's self-intro
# Actually LOOP 1 = "그리고 루프입니다. 오늘 다룰 주제는 Claude Opus 5 출시와..."
# This seems like a co-host intro, not a response to the question.
# 
# Real flow based on content analysis:
# IRO 1: 안녕, 이로입니다 (greeting)
# LOOP 1: 그리고 루프입니다 (co-host greeting)  
# IRO 2: 이번 주 최고 화제, Claude Opus 5... (topic)
# IRO 3: 루프, 직장인에게 실제로 뭘 바꿔주는 거야? (question)
# LOOP 2: 핵심 변화는 두 가지입니다... (answer)
# LOOP 3: 이전 모델은 다섯 단계만 지나도... (elaboration)
# IRO 4: 이전까지는 AI가 회의록 정리하고 끝이었잖아? (reaction)
# LOOP 4: 정확한 지적입니다. 회의록 하나도... (agreement)
# IRO 5: 근데 같은 주에 무서운 뉴스도 있었어. (transition)
# LOOP 5: 맞습니다. 에이전트가 자율적으로... → No, loop 5 is about boundaries
# Actually loop 5 = "맞습니다. 에이전트가 자율적으로 움직이는 영역이 넓어질수록..."
# But iro 5 = "근데 같은 주에 무서운 뉴스도 있었어. OpenAI 에이전트가 Hugging Face를..."
# These don't flow. Let me look at loop 6 = "581점을 받은 두 번째 핫 이슈입니다..."
# That flows after iro 5.

# CORRECT FLOW:
CORRECT_FLOW = [
    ("iro", 1),    # 안녕, 이로입니다
    ("loop", 1),   # 그리고 루프입니다
    ("iro", 2),    # 이번 주 최고 화제, Claude Opus 5
    ("iro", 3),    # 루프, 직장인에게 실제로 뭘 바꿔주는 거야?
    ("loop", 2),   # 핵심 변화는 두 가지입니다
    ("loop", 3),   # 이전 모델은 다섯 단계만 지나도
    ("iro", 4),    # 이전까지는 AI가 회의록 정리하고 끝이었잖아?
    ("loop", 4),   # 정확한 지적입니다
    ("iro", 5),    # 근데 같은 주에 무서운 뉴스도 있었어
    ("loop", 5),   # 맞습니다. 에이전트가 자율적으로 → wait, this is about boundaries
    # loop 5 = "맞습니다. 에이전트가 자율적으로 움직이는 영역이 넓어질수록..."
    # But after iro's HF attack mention, loop 6 = "581점을 받은 두 번째 핫 이슈입니다" makes more sense
    # Let me re-read:
    # iro 5 = "근데 같은 주에 무서운 뉴스도 있었어. OpenAI 에이전트가 Hugging Face를 공격한 사건."
    # loop 6 = "581점을 받은 두 번째 핫 이슈입니다. OpenAI 에이전트가 다른 플랫폼 보안을 뚫었습니다."
    # These are redundant. Loop is adding detail.
    # So after iro 5, loop 6 follows, then:
    # loop 7 = "능력은 있었지만 방향을 통제하지 못했습니다."
    # iro 6 = "능력이 커질수록 권한 경계를 먼저 정해야 해."
    # loop 8 = "모델이 좋아지면 전부 맡기는 게 아니라 권한 경계를 먼저 정해야 합니다."
    # These two say the same thing... so maybe:
    # iro 6 = "능력이 커질수록 권한 경계를 먼저 정해야 해."
    # Then move to experiment:
    # iro 7 = "그래서 이번 주 실험입니다."
    # loop 9 = "이번 주 다른 소식을 빠르게 짚겠습니다."
    # iro 8 = "회의록이면 AI가 초안을 만들고..."
    # loop 10 = "좋은 실험입니다."
    # iro 9 = "다음 주에 또 새로운 트렌드로..."
    # iro 10... wait iro has 14 lines
]

# The iro_v3.txt has 14 lines but some are continuation. Let me just count properly.
print(f"\nIRO total lines: {len([l for l in iro_text if l.strip()])}")
print(f"LOOP total lines: {len([l for l in loop_text if l.strip()])}")
