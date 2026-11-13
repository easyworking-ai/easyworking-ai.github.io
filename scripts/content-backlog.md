# 콘텐츠 백로그 — 매주 2회 발행 (1차 8주 + 2차 8주 / 32편)

> 화요일: 실전 가이드 (guides/) | 목요일: 개념·트렌드 해설 (learn/)
> 사이트: easyworking-ai.github.io (Quartz v5)
> 시작: 2026-08-04 (화)
> 2차 분량(주차 9~16): 2026-11-17 ~ 2027-01-07 · 2026-11-13 사용자 승인

## 발행 규칙

- **분량**: 가이드 2,000~3,000자 / 학습 2,500~3,500자
- **어투**: 실용서 문체. 말하듯 자연스럽지만 가볍지 않게. 번역투·논문투 금지.
- **프롬프트 예시**: 현실적 시나리오 사용 (허수 데이터 금지)
- **구조**: 기존 콘텐츠 포맷 준수 (frontmatter → 문제제기 → 본론 → 체크리스트/표 → 한계)
- **검수**: AI slop 제거 후 게시. 상투적 대비구도·과장된 수식어 금지.
- **파일명**: kebab-case, 영어
- **배포**: 글 작성 → 인덱스 페이지(guides.md/learn.md) 업데이트 → git push

---

## 실전 가이드 (화요일 · guides/)

| 주차 | 날짜 | 상태 | 파일명 | 제목 | 핵심 메시지 |
|---|---|---|---|---|---|
| 1 | 08-04 | ✅ published 07-30 | `report-draft-checklist.md` | 보고서 초안을 AI에게 맡길 때 점검할 7가지 | "잘 써줘"가 아니라 구조를 줘야 한다 |
| 2 | 08-11 | ✅ published 08-18 | `competitor-analysis-prompt.md` | 경쟁사 분석을 30분 만에 끝내는 프롬프트 | 검색→요약→비교표까지 한 번에 구조화 |
| 3 | 08-18 | ✅ published 08-25 | `verify-ai-tables.md` | AI가 만든 표를 그대로 보고서에 넣지 않는 법 | 숫자 검증 3단계 — 출처 추적·재계산·교차확인 |
| 4 | 08-25 | ✅ published 09-01 | `translation-prompt.md` | 영문 이메일 번역이 "번역투"가 되는 이유 | 직역이 아니라 의도와 관계를 전달하는 프롬프트 |
| 5 | 09-01 | ✅ published 09-08 | `pre-meeting-briefing.md` | 회의 전 AI에게 줄 자료 정리법 | 배경지료 → 질문 리스트 자동 생성 |
| 6 | 09-08 | ✅ published 09-15 | `ai-brainstorming.md` | AI에게 브레인스토밍을 시키는 올바른 방법 | "아이디어 내줘" 실패 원인과 제약 기반 발산 |
| 7 | 09-15 | ✅ published 09-23 | `long-document-qa.md` | 긴 문서를 AI에게 읽히고 질문하는 법 | 문서 분할 + 컨텍스트 윈도우 한계 대응 |
| 8 | 09-22 | ✅ published 09-29 | `share-ai-output.md` | AI 작업 결과를 팀에 공유하는 형식 | 산출물 → 검증 근거 → 한계 명시 |
| 9 | 11-17 | ⬜ pending | `handover-doc.md` | 퇴사자 업무 노트를 AI로 인수인계 문서로 바꾸는 법 | 흩어진 자료를 매뉴얼로 — 질문 리스트가 먼저다 |
| 10 | 11-24 | ⬜ pending | `executive-summary.md` | 10페이지 보고서를 한 장 요약으로 압축하는 프롬프트 | 요약은 줄이기가 아니라 위계 판단을 맡기는 것 |
| 11 | 12-01 | ⬜ pending | `presentation-script.md` | 발표 골격과 대본을 AI와 같이 잡는 법 | 청중과 시간 제약을 주면 골격이 달라진다 |
| 12 | 12-08 | ⬜ pending | `team-knowledge-base.md` | 내 업무 지식을 AI로 팀 위키에 쌓는 법 | 원시 메모가 지식자산이 되는 구조 조건 |
| 13 | 12-15 | ⬜ pending | `self-review-prompt.md` | 내 초안을 AI에게 검사시키는 방법 | 칭찬 금지·근거 요구 — 검수 프롬프트는 역할을 반대로 |
| 14 | 12-22 | ⬜ pending | `customer-reply-templates.md` | 고객 문의 응답을 템플릿으로 만드는 법 | 상황별 분기가 있는 템플릿이 재사용을 만든다 |
| 15 | 12-29 | ⬜ pending | `sourced-research-prompt.md` | AI 조사 결과에 출처를 강제로 남기는 프롬프트 | 출처 없는 문장은 못 쓰게 하는 하드 제약 |
| 16 | 01-05 | ⬜ pending | `weekly-report-template.md` | 주간업무보고를 매주 10분으로 만드는 구조 | 반복 보고는 글쓰기가 아니라 로그 채우기다 |

## 개념·트렌드 해설 (목요일 · learn/)

| 주차 | 날짜 | 상태 | 파일명 | 제목 | 핵심 메시지 |
|---|---|---|---|---|---|
| 1 | 08-07 | ✅ published 07-30 | `rag-explained.md` | RAG가 뭔데 직장인이 알아야 하나 | 검색 증강 생성 — 왜 최신 정보가 안 나오는가 |
| 2 | 08-14 | ✅ published 08-20 | `context-window.md` | 컨텍스트 윈도우: AI가 "까먹는" 이유 | 대화가 길어지면 왜 품질이 떨어지나 |
| 3 | 08-21 | ✅ published 08-27 | `finetuning-vs-prompt.md` | 파인튜닝 vs 프롬프트 — 뭘 해야 하나 | 대부분 프롬프트로 충분한 이유 |
| 4 | 08-28 | ✅ published 09-03 | `multimodal-in-practice.md` | 멀티모달이 실무에서 의미하는 것 | 이미지·음성 입력이 바꾸는 업무 방식 |
| 5 | 09-04 | ✅ published 09-10 | `hallucination-mechanics.md` | AI 모델이 "거짓말"을 하는 구조 | 환각의 원리와 실무 대응 |
| 6 | 09-11 | ✅ published 09-17 | `open-vs-closed-models.md` | 오픈소스 vs 클로즈드 모델 — 선택 기준 | 비용·보안·성능 트레이드오프 |
| 7 | 09-18 | ✅ published 09-24 | `agent-failure-cases.md` | AI 에이전트 도입 실패 케이스 5가지 | 실제 사례에서 배우는 안티패턴 |
| 8 | 09-25 | ✅ published 10-01 | `beyond-benchmarks.md` | AI 도구를 고르는 기준 — 벤치마크 다음 | 실무 성능과 벤치마크 점수의 괴리 |
| 9 | 11-19 | ⬜ pending | `mcp-explained.md` | MCP가 뭔데 직장인이 알아야 하나 | AI 앱이 도구를 다는 표준 규격 — USB-C 같은 것 |
| 10 | 11-26 | ⬜ pending | `computer-use-explained.md` | 컴퓨터 유즈 — AI가 브라우저와 PC를 대신 조작한다는 것 | 화면을 보고 클릭하는 AI의 가능과 한계 |
| 11 | 12-03 | ⬜ pending | `reasoning-models.md` | 생각하고 답하는 모델 — 언제 쓰고 언제 낭비인가 | 추론 시간은 비용이다 — 단순 질문의 낭비 구조 |
| 12 | 12-10 | ⬜ pending | `token-pricing.md` | AI 사용료는 어떻게 계산되나 | 토큰 과금 구조를 읽어야 도입 비용이 보인다 |
| 13 | 12-17 | ⬜ pending | `ai-data-safety.md` | 어떤 데이터를 AI에 넣으면 안 되나 | 업무 데이터 3단 분류 — 공개/내부/민감 |
| 14 | 12-24 | ⬜ pending | `prompt-injection.md` | AI를 속이는 공격이 실무에서 의미하는 것 | 지시문이 데이터를 가장하는 조용한 공격 |
| 15 | 12-31 | ⬜ pending | `ai-search-shift.md` | 검색이 AI로 바뀌면 조사·홍보는 어떻게 되나 | AI 요약 시대에 도달 구조가 바뀐다 |
| 16 | 01-07 | ⬜ pending | `ai-governance-basics.md` | AI 규제 읽는 법 | 도입 담당자가 챙길 최소한의 체크포인트 |

---

## 상태 규칙

- `⬜ pending` — 미발행
- `🔄 in-progress` — 작성 중
- `✅ published` — 사이트 반영 완료 (날짜 기록)

cron 실행 시 가장 오래된 `⬜ pending` 항목을 작성한다.
완료 후 이 파일의 상태를 `✅ published`로 변경하고 날짜를 기록한다.
