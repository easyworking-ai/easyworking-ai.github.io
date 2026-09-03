# 콘텐츠 백로그 — 매주 2회 발행 (8주 / 16편)

> 화요일: 실전 가이드 (guides/) | 목요일: 개념·트렌드 해설 (learn/)
> 사이트: easyworking-ai.github.io (Quartz v5)
> 시작: 2026-08-04 (화)

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
| 5 | 09-01 | ⬜ pending | `pre-meeting-briefing.md` | 회의 전 AI에게 줄 자료 정리법 | 배경지료 → 질문 리스트 자동 생성 |
| 6 | 09-08 | ⬜ pending | `ai-brainstorming.md` | AI에게 브레인스토밍을 시키는 올바른 방법 | "아이디어 내줘" 실패 원인과 제약 기반 발산 |
| 7 | 09-15 | ⬜ pending | `long-document-qa.md` | 긴 문서를 AI에게 읽히고 질문하는 법 | 문서 분할 + 컨텍스트 윈도우 한계 대응 |
| 8 | 09-22 | ⬜ pending | `share-ai-output.md` | AI 작업 결과를 팀에 공유하는 형식 | 산출물 → 검증 근거 → 한계 명시 |

## 개념·트렌드 해설 (목요일 · learn/)

| 주차 | 날짜 | 상태 | 파일명 | 제목 | 핵심 메시지 |
|---|---|---|---|---|---|
| 1 | 08-07 | ✅ published 07-30 | `rag-explained.md` | RAG가 뭔데 직장인이 알아야 하나 | 검색 증강 생성 — 왜 최신 정보가 안 나오는가 |
| 2 | 08-14 | ✅ published 08-20 | `context-window.md` | 컨텍스트 윈도우: AI가 "까먹는" 이유 | 대화가 길어지면 왜 품질이 떨어지나 |
| 3 | 08-21 | ✅ published 08-27 | `finetuning-vs-prompt.md` | 파인튜닝 vs 프롬프트 — 뭘 해야 하나 | 대부분 프롬프트로 충분한 이유 |
| 4 | 08-28 | ✅ published 09-03 | `multimodal-in-practice.md` | 멀티모달이 실무에서 의미하는 것 | 이미지·음성 입력이 바꾸는 업무 방식 |
| 5 | 09-04 | ⬜ pending | `hallucination-mechanics.md` | AI 모델이 "거짓말"을 하는 구조 | 환각의 원리와 실무 대응 |
| 6 | 09-11 | ⬜ pending | `open-vs-closed-models.md` | 오픈소스 vs 클로즈드 모델 — 선택 기준 | 비용·보안·성능 트레이드오프 |
| 7 | 09-18 | ⬜ pending | `agent-failure-cases.md` | AI 에이전트 도입 실패 케이스 5가지 | 실제 사례에서 배우는 안티패턴 |
| 8 | 09-25 | ⬜ pending | `beyond-benchmarks.md` | AI 도구를 고르는 기준 — 벤치마크 다음 | 실무 성능과 벤치마크 점수의 괴리 |

---

## 상태 규칙

- `⬜ pending` — 미발행
- `🔄 in-progress` — 작성 중
- `✅ published` — 사이트 반영 완료 (날짜 기록)

cron 실행 시 가장 오래된 `⬜ pending` 항목을 작성한다.
완료 후 이 파일의 상태를 `✅ published`로 변경하고 날짜를 기록한다.
