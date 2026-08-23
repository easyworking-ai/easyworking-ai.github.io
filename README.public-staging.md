# Public 스테이징 — 검수 대시보드

이 폴더는 `~/wiki` 원본에서 변환된 **독자 대상 공개 산출물**이다. Quartz 빌더가 이 폴더만 읽는다.

## 전환 규칙 요약

| wiki 원본에서 | 공개 산출물에서 |
|---|---|
| `[[wiki-link\|별칭]]` | 해소: 설명 문장 또는 하단 관련 글 링크 |
| `## 대표 원본 소스` (내부 출처) | 출처를 본문 흐름에 녹이거나 링크로 |
| `signals:`, `point_count:`, `keywords:` (내부 메타) | 제거 |
| `raw/articles/...` 내부 경로 | references로 이름 변경, 내부 경로 미노출 |
| 내부 운영 섹션 (OKF 요약, gap, cluster) | 제거 |
| 날카로운 내부 언어 | 독자 맥락으로 순화, 문제의식은 유지 |

## 검수 상태

| 파일 | 원본 | 상태 | 변환일 |
|---|---|---|---|
| `wiki/concepts/agent-runtime-reliability.md` | `concepts/agent-runtime-reliability.md` (293행) | 🟡 검수 대기 | 2026-07-25 |

## 워크플로

```
Hermes가 wiki 노트 → public/ 변환
  → git diff로 변경 사항 확인
  → 사용자 승인/수정/반려
  → Quartz build → push → GitHub Pages
```
