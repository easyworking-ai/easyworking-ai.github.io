---
title: "헤르메스 데스크톱과 Bot Mode 설치·실습노트"
description: "Hermes Desktop 설치부터 Bot Mode의 Profile, 그룹 채팅과 Routines까지, 실제 실행 여부와 안전한 운영 경계를 구분해 기록한 실습노트입니다."
created: 2026-08-22
updated: 2026-08-22
cssclass: blog-post
publish: true
lang: ko
section: YOUTUBE
source_checked: 2026-08-22
official_site_version_observed: v0.20.5
runtime_status: "미실행"
tags:
  - hermes
  - hermes-desktop
  - bot-mode
  - agent
  - youtube
  - 실습노트
sources:
  - https://hermes-agent.nousresearch.com/docs/getting-started/quickstart
  - https://hermes-agent.nousresearch.com/docs/getting-started/installation
  - https://hermes-agent.nousresearch.com/docs/user-guide/desktop
  - https://hermes-agent.nousresearch.com/docs/user-guide/profiles
  - https://hermes-agent.nousresearch.com/docs/user-guide/features/cron
  - https://hermes-agent.nousresearch.com/docs/user-guide/security
---

<img class="ewa-article-art" src="/static/img/art-youtube-hermes-installation.jpg" alt="데스크톱 에이전트와 프로필 카드를 연결해 실습하는 삽화" width="1200" height="800" loading="eager">

# 헤르메스 데스크톱과 Bot Mode 설치·실습노트

## 0. 정리

| 구분             | 한마디로                                                     | 설치·실행의 핵심                                                                             |
| -------------- | -------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Hermes Desktop | 터미널용 Hermes와 같은 에이전트를 창에서 쓰는 네이티브 앱                      | 공식 사이트의 Desktop 설치 파일을 실행하거나, CLI 설치 뒤 `hermes desktop`                               |
| Bot Mode       | Hermes **프로필(Profile)** 하나를 이름 있는 봇 하나로 보여 주는 Desktop 기능 | 현재 Desktop에 기본 포함된 기능. `Settings → Plugins`에서 켜고 끌 수 있으며, 최신 빌드에는 별도 플러그인 클론이 필요하지 않다 |
| Profile        | 설정·API 인증·기억·세션·스킬·예약 작업을 분리한 Hermes 인스턴스                | Bot Mode에서 `New Agent`로 만들거나 `hermes profile create <name>`으로 만든다                     |
| Routines       | 봇에 연결된 반복 작업. 내부적으로 Hermes Cron을 사용한다                    | 기본 실습이 통과한 뒤, 외부 전송 없이 로컬 테스트로만 확인한다                                                  |
| 주의할 오해         | 프로필을 만들었다고 파일 접근이 자동으로 격리되는 것은 아니다                       | 기본 `local` 터미널은 현재 OS 사용자 권한으로 실행된다. Profile은 상태 분리이지 보안 샌드박스가 아니다                    |

### Bot Mode는 따로 설치하지 않는다

현재 Bot Mode는 Desktop에 기본 포함되어 있다. 예전 [Hermes-Bot-Mode 저장소](https://github.com/NousResearch/Hermes-Bot-Mode)를 따로 클론하지 말고, Desktop을 설치한 뒤 `Settings → Plugins`에서 보이는지만 확인한다.

## 1. 실습 전 한 줄 주의

처음에는 현재 보유한 유튜브 콘텐츠 패키지의 문서와 필요한 발췌만 읽기 자료로 사용한다. 실제 채널 계정·업로드·비공개 자료에는 접근하지 않으며, 외부 메시지 전송·파일 생성·삭제는 하지 않는다. API 키는 노트나 캡처에 남기지 않는다.

## 2. 설치 전 준비

### 2.1 지원 범위

공식 홈페이지 기준 Desktop 다운로드 항목은 다음과 같다.

- macOS 12+
- Windows 10/11
- Linux: 공식 터미널 설치 후 `hermes desktop` 실행

공식 설치 문서는 macOS와 Windows에서 Desktop 설치 파일을 실행하는 경로를 권장한다. Linux·macOS·WSL2는 설치 스크립트, native Windows는 PowerShell 스크립트 경로를 제공한다.

### 2.2 설치 경로 선택

| 운영체제 | 권장 경로 | 실행할 일 |
| --- | --- | --- |
| macOS | 공식 Desktop 설치 파일 | [공식 홈페이지](https://hermes-agent.nousresearch.com/)에서 Download desktop app을 받아 실행 |
| Windows | 공식 Desktop 설치 파일 | 공식 홈페이지에서 Windows 설치 파일을 받아 실행 |
| Linux | CLI 설치 후 Desktop 실행 | `curl ... | bash` → 셸 재시작 → `hermes desktop` |
| 이미 CLI가 설치됨 | 기존 설치 재사용 | `hermes desktop` |

설치 프로그램은 공식 문서상 Python 3.11, Node.js 22, `ripgrep`, `ffmpeg`, 가상환경, `hermes` 명령 설정 등을 자동으로 처리한다. Python·Node.js·ripgrep·ffmpeg를 먼저 수동 설치하는 것이 기본 요구사항은 아니다.

### 2.3 Linux 또는 터미널 설치 전 점검

```bash
git --version
curl --version
```

Linux에서 명령이 없다면 배포판의 패키지 관리자로 `curl`, `xz-utils`를 준비한다. Desktop 빌드에 native 모듈 컴파일이 필요하면 `build-essential`도 준비한다. Debian/Ubuntu 예시는 다음과 같다.

```bash
sudo apt install curl xz-utils build-essential
```

Windows Desktop 설치 파일을 쓰는 경우에는 이 단계를 생략한다.

## 3. Hermes 설치

### 3.1 macOS·Windows: Desktop 설치 파일

1. [Hermes Agent 공식 홈페이지](https://hermes-agent.nousresearch.com/)를 연다.
2. 운영체제에 맞는 **Download desktop app**을 선택한다.
3. 설치 파일을 실행한다.
4. 첫 실행 화면에서 로컬 Hermes 설치 또는 이미 실행 중인 Hermes 연결을 선택한다.
5. 설치가 끝난 뒤 새 터미널을 열고 아래 검증을 진행한다.

> Windows는 설치 후 기존 PowerShell이 이전 PATH를 들고 있을 수 있다. 기존 창을 닫고 새 PowerShell을 열어 `Get-Command hermes`를 다시 확인한다.

### 3.2 Linux·macOS·WSL2: 터미널 설치 후 Desktop 실행

공식 설치 스크립트 경로:

조직 보안 정책상 원격 스크립트 직접 실행이 금지되어 있다면 공식 URL의 스크립트를 먼저 저장·검토한 뒤 실행한다. 비공식 미러나 임의의 설치 파일은 사용하지 않는다.

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

설치 후 셸을 다시 읽는다.

```bash
source ~/.bashrc   # bash를 쓰는 경우
# 또는
source ~/.zshrc    # zsh를 쓰는 경우
```

그 다음 Desktop을 실행한다.

```bash
hermes desktop
```

`hermes desktop`은 현재 Hermes 설치의 설정·키·세션·스킬을 재사용한다. 첫 실행에서 Desktop 앱이 로컬 Hermes 런타임을 준비할 수 있다. 기본적으로는 현재 OS에 맞는 Desktop 빌드 과정을 거친 뒤 앱을 연다.

### 3.3 native Windows의 CLI-only 설치 경로

Desktop 설치 파일이 아니라 CLI만 먼저 설치하려는 경우 PowerShell에서 실행한다.

```powershell
iex (irm https://hermes-agent.nousresearch.com/install.ps1)
```

그 뒤 Desktop까지 사용하려면 새 PowerShell을 열고 다음을 실행한다.

```powershell
hermes desktop
```

### 3.4 설치 직후 정적 검증

아직 모델을 연결하지 않았더라도 아래 명령으로 설치 상태를 확인한다.

```bash
hermes --version
hermes doctor
hermes status
```

Windows PowerShell도 명령 이름은 동일하다.

```powershell
hermes --version
hermes doctor
hermes status
```

#### 실행 기록

| 항목 | 실제 기록 |
| --- | --- |
| 운영체제·버전 | `[실행 기록]` |
| 설치 경로 | `Desktop 설치 파일 / install.sh / install.ps1 / 기존 CLI` |
| `hermes --version` | `[실행 기록]` |
| `hermes doctor` 요약 | `[실행 기록]` |
| `hermes status` 요약 | `[실행 기록]` |
| 오류 또는 경고 | `[없음 / 내용]` |

## 4. Provider·모델 설정

Desktop 첫 실행의 onboarding 또는 `Settings → Providers`에서 Provider와 모델을 설정한다. Hermes가 설치되어도 Provider 인증이 끝나지 않으면 실제 대화가 완료되지 않는다.

### 선택 A: Nous Portal을 사용하는 경우

공식 문서가 안내하는 가장 짧은 경로는 다음이다.

```bash
hermes setup --portal
```

이 명령은 OAuth 로그인을 진행하고 Nous를 inference Provider로 설정하며 Tool Gateway 사용 설정을 한 번에 처리한다. Portal을 사용하지 않는다면 이 명령을 억지로 실행하지 말고 선택 B를 사용한다.

### 선택 B: 다른 Provider 또는 직접 API 키를 사용하는 경우

```bash
hermes model
```

또는 전체 설정 마법사를 실행한다.

```bash
hermes setup
```

Desktop에서는 같은 작업을 `Settings → Providers`, `Settings → Model`에서 할 수 있다. API 키는 화면이나 노트에 직접 복사하지 않는다.

### Provider 설정 확인

다음 테스트는 도구 사용이나 외부 자료가 필요 없는 한 문장 응답으로 한다.

```text
다음 문장을 정확히 한 줄로 답해줘: 설치 확인 완료
```

확인할 것:

- [ ] Provider 인증 오류 없이 응답이 왔다.
- [ ] 응답 시간 초과나 모델 이름 오류가 없었다.
- [ ] 응답 전문 또는 화면 캡처를 `실습 기록 카드`에 남겼다.
- [ ] 이 시점까지는 Bot Mode·Cron·Messaging을 추가하지 않았다.

공식 Quickstart도 일반 채팅 하나가 먼저 완료된 뒤 gateway, cron, skills, voice, routing을 추가하라고 안내한다. 기본 대화가 실패한 상태에서 Bot Mode를 먼저 디버깅하지 않는다.

## 5. Desktop 기본 사용 확인

### 입력 → 행동 → 결과

| 단계 | 할 일 | 남길 결과 |
| --- | --- | --- |
| 입력 | `설치 확인 완료`라고 한 줄 응답을 요청 | 내가 보낸 테스트 문장 |
| 행동 | Desktop 채팅창에 전송하고 응답이 끝날 때까지 기다림 | 응답 완료 시각 또는 캡처 |
| 결과 | 응답이 한 번 완료되었는지 확인 | `기본 채팅 통과 / 실패 원인` |
| 복구 | 실패하면 Provider·모델을 먼저 확인하고 `hermes doctor`를 재실행 | 복구 전후 기록 |

Desktop은 CLI와 별도 에이전트가 아니다. 공식 문서에 따르면 Desktop, `hermes` CLI/TUI, Web Dashboard가 같은 Agent의 설정·키·세션·스킬·memory를 공유하므로, 여기서 시작한 세션을 CLI에서 이어 볼 수 있다.

실행 명령으로 열려면:

```bash
hermes desktop
```

이미 열린 앱을 계속 사용할 때는 다시 실행하지 않아도 된다.

## 6. Bot Mode 실습: 프로필 두 개를 봇으로 만들기

### 6.1 봇과 프로필의 관계

이번 실습에서 `content-planner`와 `script-editor`는 서로 다른 이름의 봇처럼 보이지만 실제 기반은 각각의 Hermes Profile이다. 각 Profile은 자체 `config.yaml`, `.env`, `SOUL.md`, memory, sessions, skills, cron, gateway 상태를 가진다.

따라서 다음 원칙을 지킨다.

- 같은 Profile 홈을 두 프로세스가 동시에 쓰지 않는다.
- 같은 Provider를 쓰더라도 Profile의 상태와 세션은 섞이지 않는다.
- Profile 이름을 바꿀 때는 기존 세션·예약 작업과의 연결을 함께 확인한다.
- Profile 분리는 보안 샌드박스가 아니므로, 실제 파일을 다루는 업무에는 별도의 sandbox 또는 제한된 작업 폴더를 설계한다.

### 6.2 Bot Mode 켜기

1. Hermes Desktop을 연다.
2. 왼쪽 사이드바에서 `Sessions | Bots` 탭을 찾는다.
3. `Bots`가 보이지 않으면 `Settings → Plugins`로 이동한다.
4. Bot Mode를 켠 뒤 Desktop을 재시작하거나 플러그인을 reload한다.
5. 봇 목록에 기본 Profile이 하나 보이는지 확인한다.

현재 Desktop 문서의 Bot Mode는 다음을 제공한다.

- 봇별 avatar와 하나의 canonical Bot Chat
- `New Agent`를 통한 새 Profile 생성
- 봇별 model, SOUL, skills, toolsets, MCP 설정을 여는 Advanced 영역
- 그룹 분류와 그룹 채팅
- 봇별 Routines 타일
- `@봇이름`을 통한 봇 간 전달과 `@user`를 통한 사람의 판단 요청

### 6.3 첫 번째 봇 만들기

#### 입력

다음 값을 사용한다.

| 필드 | 값 |
| --- | --- |
| Name | `content-planner` |
| Title | `콘텐츠 기획자` |
| Description | `현재 보유한 일하는 ai 유튜브 자료에서 타깃·핵심 약속·데모·근거·금지사항을 추출해 제작용 brief로 정리한다.` |

#### 행동

1. `Bots` 탭에서 `New Agent`를 선택한다.
2. 위의 Name, Title, Description을 입력한다.
3. 첫 실습에서는 Advanced를 기본값으로 둔다.
4. 저장한 뒤 봇 목록에 `content-planner`가 나타나는지 확인한다.
5. 봇을 클릭해 독립된 Bot Chat이 열리는지 확인한다.

#### 결과·확인

- [ ] `content-planner` 행이 봇 목록에 보인다.
- [ ] 봇의 제목과 설명이 입력값과 일치한다.
- [ ] 봇을 클릭하면 기존 기본 Profile과 구분되는 Bot Chat이 열린다.
- [ ] 봇의 프로필 설정을 바꿨다면 새 채팅에서 확인한다.

### 6.4 두 번째 봇 만들기

| 필드 | 값 |
| --- | --- |
| Name | `script-editor` |
| Title | `대본 편집자` |
| Description | `content-planner가 확인한 내용만 사용해 일하는 ai 톤의 훅·장면 구성·CTA 초안을 만들고 미확인 내용은 표시한다.` |

동일하게 `New Agent → 저장 → 봇 목록 확인 → Bot Chat 열기` 순서로 진행한다.

### 6.5 UI가 작동하지 않을 때 CLI 대체 경로

Bot Mode UI 대신 공식 Profiles CLI로 Profile을 만들 수 있다.

```bash
hermes profile create content-planner \
  --description "현재 보유한 일하는 ai 유튜브 자료에서 타깃·핵심 약속·데모·근거·금지사항을 추출해 제작용 brief로 정리한다."

hermes profile create script-editor \
  --description "content-planner가 확인한 내용만 사용해 일하는 ai 톤의 훅·장면 구성·CTA 초안을 만들고 미확인 내용은 표시한다."

hermes profile list
```

Profile을 만든 뒤 Desktop을 새로고침하고 `Bots` 탭을 다시 확인한다. 새 Profile에서 실제 대화를 시작하려면 Profile별 Provider·모델 설정이 필요할 수 있다.

## 7. Bot Mode 실습: 유튜브 콘텐츠 제작 협업

### 7.1 실습 사례

이번 실습은 새 공지문을 요약하는 대신, 현재 보유한 `일하는 ai` 콘텐츠 패키지를 다음 제작 산출물로 발전시키는 흐름을 사용한다. 기준 자료는 AI 격차 유튜브 콘텐츠 패키지다.

```text
[현재 보유 콘텐츠]
채널: 일하는 ai
시리즈: AI 격차의 시대
대상 편: EP1 「AI한테 시켰더니 퇴근이 빨라졌습니다」
타깃: 현업 IT 기획자·PM과 AI 도입에 관심 있는 실무자
핵심 약속: 회사는 AI를 도입했지만 쓰는 방법을 모르는 사람에게,
           에이전트 3명(dev·reviewer·orchestrator)이 brief → 실행 → 검수하는 흐름을 실제 화면으로 보여준다.
현재 문서 산출물: 리서치·시리즈 설계·EP1 대본·촬영 큐시트·편집 가이드·마케팅 플랜·소스 체크리스트

[읽기·제작 규칙]
1. 아래에 지정한 현재 보유 콘텐츠 문서만 source of truth로 사용한다.
2. 문서에 적힌 확정 내용, 제작 계획, 런타임 미확인을 서로 구분한다.
3. 통계·출처·실행 결과는 원문 상태를 보존하고, 확인되지 않은 내용은 [확인 필요] 또는 [런타임 미확인]으로 표시한다.
4. 실제 채널 업로드, 커뮤니티 게시, 외부 전송, 파일 생성·수정·삭제, 웹 검색은 하지 않는다.
5. 대본 초안이 만들어져도 촬영·편집·업로드가 완료된 것으로 간주하지 않는다.
```

### 7.2 그룹 만들기

1. `content-planner` 행에서 마우스 오른쪽 버튼을 누른다.
2. `Move to group`을 선택한다.
3. 새 그룹 이름으로 `유튜브 콘텐츠 제작`을 입력한다.
4. `script-editor`도 같은 그룹으로 이동한다.
5. 그룹 헤더에서 `Open chat`을 선택한다.

아카이브된 공식 Bot Mode README는 그룹 채팅을 2~6개 봇이 함께 쓰는 방으로 설명한다. 현재 Desktop 문서도 그룹 채팅을 여러 봇이 함께 쓰는 기능으로 안내한다. 그룹 채팅은 일반 개인 세션과 구분된 행으로 표시되며, 여러 봇이 순서대로 응답할 수 있다.

### 7.3 그룹에 보낼 입력

다음 프롬프트를 그룹 채팅에 붙여 넣는다. 읽기 전용 참고자료만 사용하고, 외부 검색이나 파일 작업은 하지 않는다.

```text
현재 보유한 `일하는 ai` 유튜브 콘텐츠 패키지만 사용해 EP1 제작 협업을 해줘.
외부 검색, 채널 업로드, 파일 작업, 메시지 발송은 하지 마.

[읽을 자료]
- 패키지 README
- 채널·시장 리서치
- 시리즈·앵글
- EP1 대본
- 소스 체크리스트

@content-planner 먼저 위 문서에서 다음을 추출해.
1. 채널·시리즈·EP1의 타깃과 시청자 약속
2. 핵심 메시지와 데모 흐름
3. 화면으로 증명할 수 있는 근거와 아직 준비·확인이 필요한 항목
4. 촬영 가능한 1페이지 콘텐츠 brief
확정 내용, 계획, [런타임 미확인]을 분리해서 적어.

@script-editor content-planner의 brief와 위 문서만 사용해 다음 제작 초안을 작성해.
1. 일하는 ai 톤의 30~45초 훅
2. EP1의 6장면 구성: 훅 → 문제 정의 → 에이전트 소개 → brief 투입 → 실행·검수 → 한계·CTA
3. 각 장면의 화면 증거와 내레이션 요지
4. 마지막에 [확인 필요]·[런타임 미확인]·사람이 최종 승인할 항목
새로운 통계·성과·실행 결과를 만들지 마.
```

### 7.4 기대하는 결과 형식

정확한 문장이나 표현은 모델마다 달라질 수 있으므로, 다음 **구조와 상태 구분**을 확인한다.

```text
[콘텐츠 brief]
- 채널·시리즈·EP: ...
- 타깃·시청자 약속: ...
- 핵심 메시지: ...
- 데모 흐름: ...
- 화면 증거·출처: ...
- 상태: 확정 / 제작 계획 / [런타임 미확인]

[촬영 초안]
- 훅: ...
- 장면 1~6: ...
- CTA: ...

[확인 필요·사람 승인]
- 없음 또는 항목 목록
```

실제 실행 후 아래를 확인한다.

- [ ] `content-planner`가 현재 패키지의 타깃·메시지·데모·근거를 분리해 정리했다.
- [ ] `script-editor`가 planner의 결과와 지정 문서만 사용했다.
- [ ] 확정 내용·제작 계획·[런타임 미확인]이 섞이지 않았다.
- [ ] 두 봇의 응답과 `유튜브 콘텐츠 제작` 그룹 채팅의 최신 미리보기가 보인다.
- [ ] 외부 웹 검색, 파일 쓰기, 채널 업로드, 메시지 발송이 일어나지 않았다.
- [ ] 사람이 최종 확인해야 하는 출처·화면·성과는 [확인 필요]로 남았다.

### 7.5 Bot Mode 결과 기록

| 확인 항목 | 실제 결과 |
| --- | --- |
| `content-planner` Bot Chat | `[실행 기록]` |
| `script-editor` Bot Chat | `[실행 기록]` |
| `유튜브 콘텐츠 제작` 그룹 행 | `[보임 / 안 보임]` |
| brief → 대본 초안 응답 순서 | `[실행 기록]` |
| `@user` 최종 판단 요청 여부 | `[있음 / 없음]` |
| 런타임 미확인 항목 표시 | `[있음 / 없음]` |
| 외부 부작용 | `[없음 / 내용]` |
| 캡처·전사 위치 | `[기록]` |

## 8. 선택 과제: Routines로 로컬 예약 테스트

선택 과제다. 수동 그룹 채팅을 확인한 뒤 진행한다.

### 8.1 Routines의 의미

Bot Mode의 Routines는 단순한 메모가 아니라 Hermes Cron으로 등록되는 예약 작업이다. 공식 Cron 문서에 따르면 예약 실행은 새 Agent 세션에서 수행되고, Gateway scheduler가 주기적으로 due job을 실행한다. 따라서 예약 작업은 현재 채팅의 맥락을 그대로 이어받는다고 가정하지 않는다.

첫 테스트에서는 다음을 지킨다.

- `local` 결과만 사용한다.
- Telegram, Discord, Slack, Email, `all` 전송을 선택하지 않는다.
- 실행 빈도는 짧게 잡더라도 테스트 직후 pause 또는 remove한다.
- 예약 작업은 Provider 호출과 비용을 만들 수 있으므로 실행 횟수를 확인한다.

### 8.2 Desktop에서 만들기

1. `Bots` 탭에서 `content-planner`를 선택한다.
2. 봇 옆 또는 대화 옆의 `Routines` 타일을 연다.
3. 작업 이름을 `bot-mode-local-smoke`로 입력한다.
4. 프롬프트를 다음처럼 입력한다.

```text
현재 시각과 "유튜브 콘텐츠 제작 예약 테스트"라는 문구만 로컬 결과로 기록해.
외부 메시지 전송, 파일 삭제, 파일 생성, 웹 검색을 하지 마.
```

5. 가장 짧은 일회성 또는 짧은 반복 시간을 선택한다.
6. Delivery가 있다면 `local`을 선택한다.
7. 저장 후 `hermes cron list` 또는 Routines 목록에서 작업을 확인한다.

### 8.3 CLI 확인·정리 경로

Desktop에서 Routines가 보이지 않을 때의 공식 CLI 확인 예시다. 아래 명령은 문서화용이며, 실제로 실행할 때는 예약 시간을 먼저 검토한다.

```bash
# 로컬 테스트용 예약 작업 예시
hermes cron create "10m" \
  "현재 시각과 '유튜브 콘텐츠 제작 예약 테스트'만 로컬 결과로 기록하고 외부 전송은 하지 마." \
  --name "bot-mode-local-smoke"

hermes cron list
hermes cron status
```

실행 후 ID를 확인했다면 최근 실행 기록을 본다.

```bash
hermes cron runs <job_id> --limit 5
```

테스트를 끝내면 반드시 중지하거나 삭제한다.

```bash
hermes cron pause <job_id>
hermes cron remove <job_id>
```

예약 작업이 실행되지 않으면 `hermes gateway status`, `hermes cron status`, `hermes cron list`를 순서대로 확인한다. Gateway scheduler가 실행 중인지 확인하기 전에는 작업을 여러 개 만들지 않는다.

## 9. 로컬·원격 실행 경계

기본 Desktop은 로컬 backend를 관리한다. 다른 머신의 `hermes serve`에 연결하는 Remote gateway도 지원하지만, 첫 실습에서는 사용하지 않는다.

Remote로 전환할 때는 다음 의미를 기억한다.

- Desktop 화면을 보는 컴퓨터와 Agent가 도구를 실행하는 컴퓨터가 달라질 수 있다.
- Remote 모드에서는 터미널 명령, 파일 작업, Agent 도구가 원격 Hermes 호스트에서 실행된다.
- `Settings → Gateways`에서 Remote URL과 인증을 설정한다.
- 공개 인터넷에 Basic Auth backend를 그대로 노출하지 않는다. 공식 문서는 신뢰 네트워크/VPN에는 Basic Auth를, 공개 접근에는 OAuth를 권장한다.

이번 실습에서 Remote gateway를 사용했다면 기록 카드에 `화면 컴퓨터`, `Agent 실행 호스트`, `인증 방식`을 따로 적는다.

## 10. 문제 해결표

| 증상 | 먼저 할 일 | 멈춤·복구 기준 |
| --- | --- | --- |
| `hermes: command not found` | macOS/Linux는 새 셸을 열거나 `source ~/.zshrc`/`source ~/.bashrc`; Windows는 새 PowerShell에서 `Get-Command hermes` | PATH를 임의로 여러 번 수정하지 말고 설치 위치와 `hermes doctor`를 기록 |
| Desktop은 열리지만 응답이 없음 | `Settings → Providers` 또는 `hermes model`에서 Provider·모델 확인 | API 키를 노트에 붙이지 말고 인증 오류 문구만 기록 |
| `hermes doctor`에 의존성 오류 | doctor가 제시한 현재 설치 경로와 오류를 저장하고 `hermes update` 여부를 검토 | 수동으로 여러 Python/Node 버전을 섞지 않는다 |
| Bots 탭이 없음 | Desktop 업데이트 → `Settings → Plugins`에서 Bot Mode 확인 | 현재 빌드에 내장되어야 하므로 예전 Bot Mode 저장소를 먼저 클론하지 않는다 |
| 봇 생성 후 목록에 안 보임 | Desktop reload/restart → `hermes profile list`로 Profile 존재 확인 | Profile 이름 중복·Provider 미설정 여부를 기록 |
| 그룹 채팅이 조용함 | 두 Profile이 그룹에 들어갔는지, 정확한 `@봇이름`을 썼는지, Provider가 각 Profile에 있는지 확인 | 같은 프롬프트를 반복 전송하지 말고 한 번 멈춘 뒤 상태를 기록 |
| 봇이 파일을 만들거나 외부 행동을 제안함 | 즉시 실행을 중지하고 승인하지 않음. `--yolo`를 끄고 지정 문서의 읽기 전용 발췌만으로 재시도 | 프로필 분리만으로 안전하다고 판정하지 않는다 |
| Routine이 실행되지 않음 | `hermes gateway status` → `hermes cron status` → `hermes cron list` → `hermes cron runs <job_id>` | 예약 작업을 추가로 만들지 말고 pause/remove 후 원인 기록 |
| Remote 연결에서 파일 위치가 다름 | 현재 연결된 Gateway와 실행 호스트를 확인 | 비공개 파일을 업로드하지 말고 로컬 실습으로 되돌린다 |

### 구형 Bot Mode 수동 플러그인에 대한 주의

예전 README에는 다음과 같은 수동 설치가 있었지만, 현재 Desktop의 권장 설치 절차가 아니다.

```text
git clone https://github.com/NousResearch/Hermes-Bot-Mode ~/.hermes/desktop-plugins/hermes-bots
```

이 명령은 **현재 빌드에 내장된 Bot Mode를 설치하기 위한 명령으로 사용하지 않는다.** 구형 빌드나 개발 환경을 재현해야 하는 별도 상황이 아니라면, 공식 Desktop 설치와 `Settings → Plugins` 확인만 사용한다. 예전 플러그인을 꼭 점검해야 한다면 플러그인은 Gateway가 아니라 Desktop 앱이 실행되는 컴퓨터에 설치된다는 점도 기록한다.

## 11. 실행 기록 카드

실습이 끝난 뒤 빈칸을 채운다. 키·토큰·비공개 자료는 기록하지 않는다.

```yaml
실행일: "YYYY-MM-DD HH:MM KST"
운영체제: ""
설치경로: "Desktop installer | install.sh | install.ps1 | 기존 CLI"
hermes_version: ""
doctor_result: ""
provider: "이름만 기록"
model: "모델 이름만 기록"
desktop_smoke_test: "통과 | 실패 | 미실행"
bot_mode: "내장 확인 | 미확인"
profiles:
  - name: content-planner
    result: ""
  - name: script-editor
    result: ""
group_chat: "통과 | 실패 | 미실행"
routine: "사용 안 함 | local 테스트 후 제거 | 확인 필요"
evidence: "캡처 또는 전사 위치"
external_side_effect: "없음 | 내용"
known_gap: ""
next_safe_action: ""
```

### 산출물 경로 제안

실제 수업 패키지에 넣을 때는 입력·출력·증거를 분리한다.

- 입력: 현재 보유한 `AI 격차 유튜브 콘텐츠 패키지` 콘텐츠 패키지와 프롬프트
- 출력: 콘텐츠 brief·촬영 초안의 그룹 채팅 전사 또는 결과 캡처
- 증거: `hermes --version`, `hermes doctor`, Bot Mode 목록, 그룹 채팅 화면
- 미실행: 아직 Provider·Desktop·Bot Mode를 열어 보지 못한 항목과 실제 촬영·업로드

## 12. 중지 기준과 다음 세션 인계

### 여기서 멈춘다

- 기본 채팅이 성공했고 Bot Mode의 두 Profile이 보이면 1차 실습은 충분하다.
- 그룹 채팅이 성공하면 Routines·Messaging·Remote를 한 번에 추가하지 않는다.
- 외부 전송·채널 업로드·실제 비공개 자료가 필요해지는 순간 이 노트의 안전 범위를 벗어난다.

### 다음 세션 인계 문장

```text
Hermes Desktop 설치·기본 채팅은 [통과/실패/미실행]이다.
확인한 버전은 [버전]이고, Provider·모델은 [이름]이다.
Bot Mode는 [내장 확인/미확인]이며 content-planner와 script-editor는 [상태]다.
유튜브 콘텐츠 제작 그룹 채팅은 [통과/실패/미실행]이고, 외부 부작용은 [없음/내용]이다.
다음 안전한 작업은 [그룹 결과 검토/출처·화면 확인/로컬 Routine 확인/문제 해결]이다.
```

## 사례 참고문서

이번 실습 사례의 기준 문서는 다음과 같다. 실제 촬영·업로드·런타임 완료를 의미하지 않는다.

1. AI 격차 유튜브 콘텐츠 패키지 — 패키지 범위·상태·소스 자산
2. 채널·시장 리서치 — 채널 실측과 콘텐츠 포지셔닝
3. 시리즈·앵글 — 타깃·EP1 구조·데모 설계
4. EP1 대본 — 훅·장면·CTA 원고
5. 소스 체크리스트 — 촬영 전 확인·보안·업로드 준비

## 참고문서

아래는 2026-08-22에 확인한 Nous Research 공식 문서와 공식 저장소다.

1. [Hermes Agent 공식 홈페이지](https://hermes-agent.nousresearch.com/) — Desktop 다운로드, OS 지원, 현재 사이트 표시 버전
2. [Quickstart](https://hermes-agent.nousresearch.com/docs/getting-started/quickstart) — 설치 후 Provider 선택, 첫 대화 검증, 기능을 단계적으로 추가하는 순서
3. [Installation](https://hermes-agent.nousresearch.com/docs/getting-started/installation) — macOS·Windows·Linux·WSL2 설치 명령, 의존성, 설치 위치
4. [Desktop App](https://hermes-agent.nousresearch.com/docs/user-guide/desktop) — Desktop과 CLI의 상태 공유, Bot Mode 내장 기능, Routines, 원격 Gateway
5. [Profiles](https://hermes-agent.nousresearch.com/docs/user-guide/profiles) — Profile별 설정·memory·session·skills 분리, Profile 생성과 Profile의 보안 한계
6. [Scheduled Tasks (Cron)](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron) — 예약 작업 생성·실행·검증·중지·삭제, Gateway scheduler와 새 세션 동작
7. [Security](https://hermes-agent.nousresearch.com/docs/user-guide/security) — 위험 명령 승인, YOLO 경고, Gateway 인증, Profile과 샌드박스의 차이
8. [Hermes Agent 공식 저장소](https://github.com/NousResearch/hermes-agent) — 현재 소스와 공식 문서 원문
9. [Hermes Bot Mode 공식 저장소(아카이브)](https://github.com/NousResearch/Hermes-Bot-Mode) — 구형 플러그인 기록과 현재 Desktop 내장 전환 안내
