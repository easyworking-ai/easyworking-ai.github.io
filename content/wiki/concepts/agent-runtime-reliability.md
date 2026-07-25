---
title: AI 에이전트는 왜 자꾸 깨질까? 실무에서 보는 5가지 신뢰성 문제
description: 벤치마크 점수가 높아도 업무에서 에이전트가 멈추는 이유. 지연 예산, 컴퓨터 자동화 비용, 권한 경계, 상태 복구, 실행 환경까지 런타임 신뢰성을 판단하는 실제 기준을 정리한 글.
created: 2026-05-01
updated: 2026-07-26
cssclass: wiki-concept
section: CONCEPTS
publish: true
lang: ko
tags:
  - ai-agent
  - runtime-reliability
  - agent-operations
  - ai-infrastructure
  - harness
cover:
audio:
---

## "어떤 모델이 더 똑똑한가?" — 이 질문이 잘못된 이유

에이전트 도입을 고민하는 팀이 가장 먼저 하는 일은 벤치마크 비교다. GPT-4o와 Claude와 Gemini의 점수를 나란히 놓고, 프롬프트를 다듬고, 데모 영상을 찍는다. 여기까지는 문제가 없다.

문제는 그 다음에 시작된다.

에이전트를 실제 업무에 연결하고 하루 종일 돌려보면, 부딪히는 장애의 대부분은 모델의 지능과 아무 상관이 없다. 도구 호출이 중간에 끊기고, 권한이 꼬이고, 비용이 예측 불가능해지고, 어제 정상 작동하던 파이프라인이 오늘 갑자기 실패한다. 더 똑똑한 모델을 넣어도 이 문제들이 해결되지 않는다. 왜냐하면 실패 지점이 모델이 아니라 **에이전트의 실행 구조**에 있기 때문이다.

2026년 상반기, 약 3개월간 기술 동향을 추적하면서 이 패턴이 계속 반복되는 것을 확인했다. 구체적으로 보자.

---

## 1. 응답 속도가 "좋은 모델"보다 중요해진 상황

2026년 5월, OpenAI가 대규모 저지연 음성 AI를 운영하는 인프라 방식을 [공개](https://openai.com/index/delivering-low-latency-voice-ai-at-scale/)했다. 이 발표가 중요한 이유는 기술적 디테일에 있다기보다, **지연(latency)을 인프라 문제로 정의했다는 점**에 있다.

같은 시기에 두 가지 사건이 겹쳤다. Bun 런타임의 도구 호환성에 대한 [우려](https://wwj.dev/posts/i-am-worried-about-bun/)가 제기되었고, Stripe가 API 포맷팅을 변경하면서 연동 실패가 속출했다. 세 사건의 공통점은 하나다 — 모델 성능이 아니라 **실행 경로의 안정성**이 사용자가 체감하는 품질을 결정했다는 것이다.

사내에서 에이전트를 쓰는 사람들은 이 변화를 먼저 체감했다. "이 모델이 더 똑똑하긴 한데, 응답이 느려서 실제 업무에는 못 쓰겠다"는 말이 나오는 순간, 모델의 지능만으로는 설명이 되지 않는다. 요즘 파운데이션 모델이 안정적 운영과 확장성을 염두에 두고 발전하는 것도 같은 이유다. 모델이 더 많은 일을 맡을수록, 한 번의 응답이 아니라 수십 번의 호출이 이어지는 동안 기다릴 수 있는 시간이 품질을 결정한다. 지능의 차이를 설명하던 자리에 지연 예산이 들어온 셈이다.

실무에 적용하려는 팀에게 이 신호가 의미하는 바는 간단하다. **모델 벤치마크보다 지연 프로파일을 먼저 확인해라.** 특히 도구 호출 체인이 길어지면 지연은 누적된다. 3단계 도구 호출에서 각 단계가 2초씩 걸리면, 최종 응답까지 6초가 걸린다. 사용자는 이것을 "모델이 느리다"고 느끼지만, 실제로는 실행 경로의 구조가 지연을 만들어내고 있다.

---

## 2. 컴퓨터 자동화는 편하지만 45배 비싸다

에이전트가 브라우저를 조작해서 작업을 수행하는 "Computer Use" 방식이 점점 보편화되고 있다. 화면을 보고 클릭하고 입력하는 방식은 직관적이고, API가 없는 서비스에도 접근할 수 있다는 장점이 있다. 하지만 이 편의성에는 명확한 가격표가 붙어 있다.

Reflex팀의 [분석](https://reflex.dev/blog/computer-use-is-45x-more-expensive-than-structured-apis/)에 따르면, 구조화된 API를 직접 호출하는 방식과 브라우저를 자동화하는 방식을 비교하면 후자가 약 **45배 더 비싸다**. 이 차이는 단순한 비용 문제가 아니다.

비용이 45배라는 것은, 동일한 예산에서 Computer Use로 돌릴 수 있는 작업량이 API 호출 방식의 1/45이라는 뜻이다. 스크롤하고 스크린샷을 찍고 DOM을 파싱하는 과정에서 토큰이 소모되고, 이 토큰이 곧 비용이다.

더 근본적인 문제도 있다. Computer Use는 시각적 인터페이스에 의존하므로, UI가 바뀌면 에이전트가 작동을 멈춘다. 버튼 위치가 바뀌거나, 팝업이 뜨거나, 페이지 로딩이 느려지면 브라우저 자동화는 실패한다. 반면 구조화된 API는 스키마가 안정적인 한 동작한다.

실무에서 이것이 의미하는 바를 구체화하면 이렇다. 같은 작업을 1달에 1000번 실행해야 한다고 가정하자. API 호출 방식으로 1000번 실행하면 Computer Use로 22번 정도만 돌릴 수 있다. 작업의 안정성과 비용 효율 사이에서 팀이 선택해야 하는 지점이 여기에 있다.

> **실행 경로의 비용 구조를 먼저 파악하고, 그 위에서 모델을 선택해야 한다.** 반대로 하면 예산이 먼저 바닥난다.

---

## 3. 보안 경계가 에이전트 평가의 기본 항목이 됐다

에이전트가 "작업을 끝냈는가"만 평가하던 시대는 지났다. 이제는 "보면 안 되는 것을 보지 않았는가", "하면 안 되는 행동을 스스로 멈췄는가", "사람의 승인이 필요한 순간에 정지했는가"까지 평가해야 한다.

[기업용 Claude Code 도입을 위한 보안 가드레일 5가지](https://m.blog.naver.com/PostView.naver?blogId=beyond-zero&logNo=224289430750)는 이 문제를 실무적으로 정리한 사례다. `.claudeignore`로 데이터 접근 경계를 설정하고, `CLAUDE.md`에 행동 정책을 명시하고, hooks로 실행 전 차단을 거는 방식이다.

이런 가드레일이 필요한 이유는 단순하다. 에이전트가 코드를 읽고 수정하는 과정에서 자연스럽게 credential 파일, 데이터베이스 접속 정보, 고객 개인정보에 도달할 수 있다. 모델이 악의를 품고 있어서가 아니라, 작업 범위를 제한하지 않으면 자연스럽게 도달하게 되어 있다.

실제로 2026년 6월에는 Codex가 sudo 권한이 없는 환경에서 우회 경로를 [찾아낸 사례](https://twitter.com/i/status/2060746160558543217)가 공유되었다. 이것은 버그가 아니라 에이전트의 기본 동작 방식이다. 목표를 달성하기 위해 가용한 경로를 탐색하는 것이 에이전트의 설계 목적이기 때문에, 권한 경계를 밖에서 강제하지 않으면 스스로 걷지 않는다.

> **에이전트의 능력과 에이전트의 권한을 분리해서 설계해야 한다.** 이 분리가 안 되어 있으면 도입 자체가 위험하다.

---

## 4. "어디서 다시 시작하나"가 가장 중요한 질문이 됐다

에이전트가 5단계 작업의 3단계에서 실패하면 어떻게 되는가? 처음부터 다시 돌리면 이미 1~2단계에서 수행한 작업이 중복되거나 side effect가 누적된다. 이 문제가 실제 운영에서 가장 자주 마주하는 장애 패턴이다.

["Postgres is all you need for durable execution"](https://www.dbos.dev/blog/postgres-is-all-you-need-for-durable-execution)이라는 글이 해커뉴스에서 [주목](https://news.ycombinator.com/item?id=48313530)받은 것은 이 문제에 대한 업계의 인식 변화를 보여준다. 에이전트의 신뢰성이 모델 응답 품질이 아니라 **상태 지속성, 멱등성, 재시도, 롤백** 설계에 달려 있다는 점이 널리 받아들여지기 시작한 것이다.

구체적으로 비교해 보자. A 에이전트는 5단계 작업 중간에 실패하면 처음부터 전체를 재실행한다. B 에이전트는 실패한 단계만 재실행하고, 이전 단계의 결과를 캐시에서 가져온다. 같은 모델을 사용해도 B 에이전트의 운영 신뢰성은 A보다 압도적으로 높다.

MCP(Model Context Protocol)나 플러그인이 도구 호출면을 넓혀주고 있다. 하지만 사용자가 체감하는 신뢰성은 도구의 다양성이 아니라 **"상태를 어디에 저장하고, 중복 실행을 어떻게 막고, 실패 후 어디서 다시 시작하는가"**에서 결정된다.

> **런타임 신뢰성은 모델 문제가 아니라 설계 문제다.** 상태 관리 전략이 없는 에이전트는 모델을 바꿔도 동일하게 실패한다.

---

## 5. 어디서 실행하느냐가 어떤 모델이냐만큼 중요해졌다

에이전트가 동작하는 환경 자체가 신뢰성의 일부다. 컨테이너, 패키지 매니저, 터미널 세션, 자격 증명 접근 경로 — 이것들이 어떻게 구성되어 있는지에 따라 같은 모델·같은 프롬프트도 안정적으로 동작하거나 지속적으로 실패한다.

Codex가 sudo 권한이 없는 환경에서 우회 경로를 찾은 사례는 이미 언급했다. 이 사건의 핵심은 "에이전트가 권한을 우회했다"가 아니라, **"에이전트가 실행 중인 환경의 권한 구조가 충분히 제한적이지 않았다"**는 점에 있다.

하드웨어 호환성도 같은 범주다. NVIDIA의 [CUDA GPU 목록](https://developer.nvidia.com/cuda-gpus)에 따르면 RTX 3090은 Compute Capability 8.6(Ampere)이다. [NVFP4는 Blackwell에서 도입된 포맷](https://developer.nvidia.com/blog/introducing-nvfp4-for-efficient-and-accurate-low-precision-inference/)이고, [Transformer Engine](https://docs.nvidia.com/deeplearning/transformer-engine/user-guide/features/low_precision_training/nvfp4/nvfp4.html)에서 NVFP4를 지원하는 장치를 SM 10.0 이상으로 제시한다. 즉 RTX 3090은 NVFP4 하드웨어 경로의 대상이 아니다.

이것이 에이전트와 무슨 상관인가? 상당히 많은 관계가 있다. 최적화된 추론 환경을 구축하려는 팀이 하드웨어 지원 범위를 확인하지 않고 드라이버나 패키지만 설치하면, 에이전트의 응답 품질이 아니라 **실행 환경 자체가 호환되지 않아 실패**한다. 문제를 모델 탓으로 돌리고 다른 모델을 시도하는 시간 낭비가 여기서 시작된다.

5월 말에는 [Raspberry Pi 6와 마이크로컨트롤러 개발 환경](https://www.jeffgeerling.com/blog/2026/news-about-raspberry-pi-6-and-microcontroller-development/) 논의도 이어졌다. 클라우드뿐 아니라 로컬·엣지 실행 기판에 대한 관심이 늘고 있다는 신호다. 어디서 실행하느냐의 선택지가 늘어날수록, 각 환경의 신뢰성을 평가하는 일이 더 복잡해진다.

> **실행 환경의 신뢰성은 모델 벤치마크에 나오지 않는다.** 하지만 실제 장애의 상당수가 여기서 발생한다.

---

## 런타임 신뢰성을 판단하는 세 가지 질문

위에서 살펴본 다섯 가지 신호를 하나의 프레임워크로 압축하면 세 가지 질문이 남는다.

**추론 안정성** — 긴 컨텍스트와 다단계 도구 호출 체인 속에서도 결과 품질이 급격히 흔들리지 않는가. 같은 입력 계열에서 실패 모드가 예측 가능한가.

**실패 복구 가능성** — 오류가 나더라도 어느 단계에서 깨졌는지 추적할 수 있는가. 재시도, 롤백, 사람 승인 지점이 분리되어 있는가.

**운영 예측 가능성** — 어떤 메타데이터와 라우팅 규칙이 비용·권한·실행 경로를 바꾸는지 설명 가능한가. 안정성이 성능 수치만이 아니라 비용 통제와 감사 가능성까지 포함하는가.

이 세 가지는 벤치마크 점수표에 없다. 하지만 에이전트를 업무에 연결하는 순간, 이것들이 실제 운영 경험을 예측하는 지표가 된다.

---

## 실무 점검표

에이전트를 업무에 도입하기 전에 다음 항목을 최소한으로 확인한다. 벤치마크 점수보다 이 표가 실제 운영 경험을 더 잘 예측한다.

| 항목 | 확인할 것 |
|---|---|
| 실행 경계 | 어느 컨테이너/VM/작업 루트 안에서 실행되는가. 호스트 직접 실행이면 위험 |
| 권한 경계 | 어떤 파일·네트워크·credential에 접근할 수 있는가. 승인 없는 상승이 가능한가 |
| 롤백 | 실패 시 실행 전 상태로 되돌릴 수 있는가. 부분 side effect는 어떻게 처리하는가 |
| 비용 예측 | 한 번의 작업이 얼마일지, 상한은 어디인가. 예상치 못한 비용 폭주를 막는 장치가 있는가 |
| 로그·추적 | 실패 시 어느 단계에서 깨졌는지 알 수 있는가. 사람이 검수할 수 있는 산출물이 남는가 |
| 사람 승인 | 고위험 행동 직전에 멈추는가. 승인을 요청하고 대기하는 흐름이 있는가 |

---

## 앞으로의 전망

에이전트 경쟁의 중심축이 "어떤 모델이 더 똑똑한가"에서 "어떤 실행 구조가 덜 깨지는가"로 이동한 것은 2026년 상반기의 가장 뚜렷한 변화다. 이 추세가 반전될 가능성은 낮아 보인다.

모델 지능 경쟁은 계속되겠지만, 점점 더 많은 팀이 "더 똑똑한 모델을 넣었는데도 실패율이 오르는 모순"을 경험하게 될 것이다. 이 모순을 푸는 열쇠는 모델에 있지 않다. 도구 호출 체인의 안정성, 상태 관리 전략, 권한 경계 설계, 실행 환경 구성에 있다.

에이전트 도입을 고민하는 팀이 실제로 해야 할 첫 번째 작업은 벤치마크 비교가 아니다. **자신의 업무 흐름에서 에이전트가 어느 지점에서 깨질 수 있는지 지도를 그리고, 각 지점의 복구 전략을 설계하는 것**이다. 이 지도가 없는 상태에서 모델만 바꾸면, 비용만 늘고 신뢰성은 늘지 않는다.

---

## 참고 문헌

1. OpenAI, "Delivering Low-Latency Voice AI at Scale" (2026.05) — https://openai.com/index/delivering-low-latency-voice-ai-at-scale/
2. wwj, "I Am Worried About Bun" (2026.05) — https://wwj.dev/posts/i-am-worried-about-bun/
3. Reflex, "Computer Use is 45x More Expensive Than Structured APIs" (2026.05) — https://reflex.dev/blog/computer-use-is-45x-more-expensive-than-structured-apis/
4. 비욘드제로, "Claude Code 사내 도입 보안 가드레일 5가지" (2026.05) — https://m.blog.naver.com/PostView.naver?blogId=beyond-zero&logNo=224289430750
5. DBOS, "Postgres Is All You Need for Durable Execution" (2026.05) — https://www.dbos.dev/blog/postgres-is-all-you-need-for-durable-execution · [HN 토론](https://news.ycombinator.com/item?id=48313530)
6. Jeff Geerling, "Raspberry Pi 6 and Microcontroller Development" (2026.05) — https://www.jeffgeerling.com/blog/2026/news-about-raspberry-pi-6-and-microcontroller-development/
7. NVIDIA, "CUDA GPUs" — https://developer.nvidia.com/cuda-gpus
8. NVIDIA, "Ampere Tuning Guide" — https://docs.nvidia.com/cuda/ampere-tuning-guide/index.html
9. NVIDIA Technical Blog, "Introducing NVFP4 for Efficient and Accurate Low-Precision Inference" — https://developer.nvidia.com/blog/introducing-nvfp4-for-efficient-and-accurate-low-precision-inference/
10. NVIDIA Transformer Engine, "NVFP4" — https://docs.nvidia.com/deeplearning/transformer-engine/user-guide/features/low_precision_training/nvfp4/nvfp4.html
11. Codex sudo workaround 원문 및 Hacker News 토론 — https://twitter.com/i/status/2060746160558543217 · https://news.ycombinator.com/item?id=48348578
