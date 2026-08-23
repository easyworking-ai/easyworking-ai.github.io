---
title: "Hermes Desktop and Bot Mode: installation and practice note"
description: "A practical note covering Hermes Desktop installation, Bot Mode Profiles, group chats, and Routines while separating verified execution from planned practice."
created: 2026-08-22
updated: 2026-08-22
cssclass: blog-post
publish: true
lang: en
section: YOUTUBE
source_checked: 2026-08-22
official_site_version_observed: v0.20.5
runtime_status: "Not run"
tags:
  - hermes
  - hermes-desktop
  - bot-mode
  - agent
  - youtube
  - practice note
sources:
  - https://hermes-agent.nousresearch.com/docs/getting-started/quickstart
  - https://hermes-agent.nousresearch.com/docs/getting-started/installation
  - https://hermes-agent.nousresearch.com/docs/user-guide/desktop
  - https://hermes-agent.nousresearch.com/docs/user-guide/profiles
  - https://hermes-agent.nousresearch.com/docs/user-guide/features/cron
  - https://hermes-agent.nousresearch.com/docs/user-guide/security
---

<img class="ewa-article-art" src="/static/img/art-youtube-hermes-installation.jpg" alt="Illustration of connecting a desktop agent with profile cards for practice" width="1200" height="800" loading="eager">

# Hermes Desktop and Bot Mode: installation and practice note

## 0. Overview

| Item | In one line | Installation or practice point |
| --- | --- | --- |
| Hermes Desktop | The native app for using the same agent as Hermes in a window | Install the Desktop app from the official site, or run `hermes desktop` after installing the CLI |
| Bot Mode | A Desktop feature that presents one Hermes Profile as a named bot | It is included in current Desktop builds; check it in `Settings → Plugins` rather than cloning an old plugin repository |
| Profile | A separated Hermes instance with its own settings, authentication, memory, sessions, skills, and scheduled tasks | Create one with `New Agent` in Bot Mode or `hermes profile create <name>` |
| Routines | Repeating work attached to a bot; internally it uses Hermes Cron | Test it locally only, after the basic practice has passed |
| Common misunderstanding | Creating a Profile does not automatically isolate file access | The default local terminal runs with the current OS user's permissions. A Profile separates state; it is not a security sandbox |

### Bot Mode is not installed separately

Bot Mode is currently included in Desktop. Do not clone the old [Hermes-Bot-Mode repository](https://github.com/NousResearch/Hermes-Bot-Mode) as the default installation path. Install Desktop first, then check `Settings → Plugins`.

## 1. One safety note before practice

Use only the current YouTube content package and the excerpts needed for the exercise. Do not access a channel account or private material, and do not upload, message, create, or delete files. Never put an API key in a note or screenshot.

## 2. Preparation

### 2.1 Supported systems

The official site lists Desktop downloads for:

- macOS 12+
- Windows 10/11
- Linux: install the official terminal package and run `hermes desktop`

The official installation guide recommends a Desktop installer on macOS and Windows. Linux, macOS, and WSL2 also have an installation-script path, while native Windows has a PowerShell script.

### 2.2 Choose an installation path

| System | Recommended path | What to do |
| --- | --- | --- |
| macOS | Official Desktop installer | Download **Download desktop app** from the [official site](https://hermes-agent.nousresearch.com/) and run it |
| Windows | Official Desktop installer | Download the Windows installer from the official site and run it |
| Linux | Terminal installation, then Desktop | Run the official install script, reload the shell, and run `hermes desktop` |
| CLI already installed | Reuse the existing installation | Run `hermes desktop` |

According to the official installation material, the installer can handle Python 3.11, Node.js 22, `ripgrep`, `ffmpeg`, a virtual environment, and the `hermes` command. Installing all of these manually first is not the default requirement.

### 2.3 Check before a Linux or terminal installation

```bash
git --version
curl --version
```

If a Linux system is missing a command, prepare `curl` and `xz-utils` with the distribution's package manager. If native modules need to be compiled, prepare `build-essential` as well. For Debian or Ubuntu:

```bash
sudo apt install curl xz-utils build-essential
```

Skip this step when using the Windows Desktop installer.

## 3. Install Hermes

### 3.1 macOS and Windows: Desktop installer

1. Open the [Hermes Agent official site](https://hermes-agent.nousresearch.com/).
2. Select **Download desktop app** for the operating system.
3. Run the installer.
4. On first launch, choose a local Hermes installation or connect to an already running Hermes.
5. Open a new terminal and run the checks below.

Windows PowerShell may still hold the old PATH after installation. Close the old window, open a new PowerShell, and run `Get-Command hermes` again.

### 3.2 Linux, macOS, and WSL2: install from the terminal, then launch Desktop

If the organization's security policy forbids piping a remote script directly into a shell, save and review the script from the official URL first. Do not use an unofficial mirror or installer.

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

Reload the shell:

```bash
source ~/.bashrc   # bash
# or
source ~/.zshrc    # zsh
```

Then launch Desktop:

```bash
hermes desktop
```

`hermes desktop` reuses the current Hermes installation's settings, keys, sessions, and skills. On first launch, the Desktop app may prepare the local Hermes runtime.

### 3.3 Native Windows CLI-only path

To install the CLI first with PowerShell:

```powershell
iex (irm https://hermes-agent.nousresearch.com/install.ps1)
```

Open a new PowerShell and launch Desktop:

```powershell
hermes desktop
```

### 3.4 Static checks immediately after installation

Even before connecting a model, check the installation:

```bash
hermes --version
hermes doctor
hermes status
```

PowerShell uses the same command names.

| Item | Actual record |
| --- | --- |
| Operating system and version | `[record after execution]` |
| Installation path | `Desktop installer / install.sh / install.ps1 / existing CLI` |
| `hermes --version` | `[record after execution]` |
| `hermes doctor` summary | `[record after execution]` |
| `hermes status` summary | `[record after execution]` |
| Error or warning | `[none / details]` |

## 4. Provider and model setup

Configure the Provider and model during Desktop onboarding or under `Settings → Providers` and `Settings → Model`. Installing Hermes is not enough: actual conversations require Provider authentication.

### Option A: Nous Portal

The shortest path described in the official documentation is:

```bash
hermes setup --portal
```

This starts OAuth login, configures Nous as the inference Provider, and enables the Tool Gateway. If you do not use the Portal, do not force this command; use Option B.

### Option B: another Provider or a direct API key

```bash
hermes model
```

Or run the full setup wizard:

```bash
hermes setup
```

Desktop exposes the same work under `Settings → Providers` and `Settings → Model`. Do not copy an API key into a screen capture or note.

### Check the Provider

Use one sentence that needs neither tools nor external material:

```text
Answer this sentence in exactly one line: Installation check complete
```

- [ ] The response arrived without a Provider authentication error.
- [ ] There was no timeout or model-name error.
- [ ] The full response or a screen capture was saved to the practice record.
- [ ] Bot Mode, Cron, and Messaging were not added before this basic test passed.

The official Quickstart also puts one normal chat before gateway, cron, skills, voice, and routing. Do not debug Bot Mode first when the basic conversation is failing.

## 5. Verify basic Desktop use

### Input → action → result

| Stage | Action | Evidence to keep |
| --- | --- | --- |
| Input | Ask for a one-line response: `Installation check complete` | The test sentence sent |
| Action | Send it in Desktop and wait until the response finishes | Completion time or capture |
| Result | Check that one response completed | `Basic chat passed / failure reason` |
| Recovery | Check Provider and model first, then rerun `hermes doctor` if needed | Before-and-after record |

Desktop is not a separate agent. The official documentation says Desktop, the `hermes` CLI/TUI, and the Web Dashboard share the same Agent settings, keys, sessions, skills, and memory. A session started here can be continued from the CLI.

```bash
hermes desktop
```

If the app is already open, launching it again is unnecessary.

## 6. Bot Mode practice: create two Profiles as bots

### 6.1 The relationship between bots and Profiles

In this practice, `content-planner` and `script-editor` look like two named bots. Underneath, each is a separate Hermes Profile. A Profile has its own `config.yaml`, `.env`, `SOUL.md`, memory, sessions, skills, cron, and gateway state.

Follow these rules:

- Do not let two processes use the same Profile home at the same time.
- Profiles can use the same Provider without sharing their state or sessions.
- When renaming a Profile, check its existing sessions and scheduled tasks as well.
- Profile separation is not a security sandbox. For real file work, design a separate sandbox or restricted work folder.

### 6.2 Turn on Bot Mode

1. Open Hermes Desktop.
2. Find the `Sessions | Bots` tabs in the left sidebar.
3. If `Bots` is missing, open `Settings → Plugins`.
4. Turn on Bot Mode, then restart Desktop or reload the plugin.
5. Confirm that one default Profile appears in the bot list.

Current Desktop documentation describes these Bot Mode features:

- An avatar and one canonical Bot Chat per bot
- A new Profile through `New Agent`
- An Advanced area for the bot's model, SOUL, skills, toolsets, and MCP settings
- Groups and group chats
- A Routines tile for each bot
- Handoffs with `@bot-name` and requests for human judgment with `@user`

### 6.3 Create the first bot

Use these values:

| Field | Value |
| --- | --- |
| Name | `content-planner` |
| Title | `Content planner` |
| Description | `Extract the target, promise, demo, evidence, and prohibitions from the current Working AI YouTube materials and organize them into a production brief.` |

Select `New Agent` in the Bots tab, enter the values, leave Advanced at its default for the first practice, save, and open the new Bot Chat.

- [ ] The `content-planner` row is visible.
- [ ] The title and description match the entered values.
- [ ] The Bot Chat is distinct from the default Profile chat.
- [ ] A changed Profile setting is checked in a new chat.

### 6.4 Create the second bot

| Field | Value |
| --- | --- |
| Name | `script-editor` |
| Title | `Script editor` |
| Description | `Using only the content-planner's verified findings, draft a Working AI hook, scene structure, and CTA. Mark anything unverified.` |

Follow the same `New Agent → save → check the list → open Bot Chat` sequence.

### 6.5 CLI fallback when the UI does not work

```bash
hermes profile create content-planner \
  --description "Extract the target, promise, demo, evidence, and prohibitions from the current Working AI YouTube materials and organize them into a production brief."

hermes profile create script-editor \
  --description "Using only content-planner's verified findings, draft a Working AI hook, scene structure, and CTA, and mark anything unverified."

hermes profile list
```

Refresh Desktop and check the Bots tab again. Each new Profile may need its own Provider and model configuration before it can start a conversation.

## 7. Bot Mode practice: collaborate on YouTube content

### 7.1 Practice case

Instead of summarizing a new announcement, use the current **AI Gap YouTube content package** to develop production outputs. The package contains research, series design, an EP1 script, a shooting cue sheet, an editing guide, a marketing plan, and a source checklist.

```text
[Current content]
Channel: Working AI
Series: The age of the AI gap
Episode: EP1, “I asked AI to do the work, and left work earlier”
Audience: Working IT planners, PMs, and people interested in practical AI adoption
Promise: Show the brief → execution → review flow of three agents (dev, reviewer,
         orchestrator) on screen for people who have adopted AI but do not yet know
         how to use it.

[Reading and production rules]
1. Use only the specified current content package as the source of truth.
2. Keep confirmed facts, production plans, and runtime-unverified items separate.
3. Preserve the status of statistics, sources, and execution results. Mark unknowns as
   [needs confirmation] or [runtime not run].
4. Do not search the web, upload to a channel, send external messages, or create,
   modify, or delete files.
5. A script draft is not a completed shoot, edit, or upload.
```

### 7.2 Create a group

Move both `content-planner` and `script-editor` to a group named `YouTube content production`, then open the group's chat. A group chat is distinct from an ordinary personal session and can let several bots respond in sequence.

### 7.3 Prompt for the group

```text
Use only the current Working AI YouTube content package to collaborate on EP1.
Do not search externally, upload to a channel, modify files, or send messages.

[Materials to read]
- Package README
- Channel and market research
- Series and angle
- EP1 script
- Source checklist

@content-planner first extract:
1. The channel, series, and EP1 target and viewer promise
2. The core message and demo flow
3. Evidence that can be shown on screen and items still needing preparation or confirmation
4. A one-page brief that can be filmed
Keep confirmed facts, plans, and [runtime not run] separate.

@script-editor use only the brief and the listed materials to draft:
1. A 30–45 second Working AI hook
2. A six-scene structure: hook → problem → agent introduction → brief input → execution and review → limits and CTA
3. Screen evidence and narration points for each scene
4. A final list of [needs confirmation], [runtime not run], and human approval items
Do not invent statistics, results, or execution records.
```

### 7.4 Expected result shape

The wording may differ by model. Check the structure and state separation:

```text
[Content brief]
- Channel, series, episode: ...
- Target and viewer promise: ...
- Core message: ...
- Demo flow: ...
- Screen evidence and sources: ...
- Status: confirmed / production plan / [runtime not run]

[Shooting draft]
- Hook: ...
- Scenes 1–6: ...
- CTA: ...

[Needs confirmation and human approval]
- None or a list of items
```

Check that the planner separates target, message, demo, and evidence; the editor uses only the brief and specified documents; runtime-unverified items remain marked; both Bot Chats and the group row are visible; no web search, file write, channel upload, or message send occurred.

### 7.5 Record the Bot Mode result

| Check | Actual result |
| --- | --- |
| `content-planner` Bot Chat | `[record after execution]` |
| `script-editor` Bot Chat | `[record after execution]` |
| `YouTube content production` group | `[visible / not visible]` |
| Brief → script response order | `[record after execution]` |
| `@user` request for judgment | `[yes / no]` |
| Runtime-unverified items marked | `[yes / no]` |
| External side effect | `[none / details]` |
| Capture or transcript location | `[record]` |

## 8. Optional exercise: a local scheduled test with Routines

Do this only after the manual group chat has passed.

### 8.1 What Routines mean

Bot Mode Routines are scheduled tasks registered through Hermes Cron, not simple reminders. Cron jobs run in a new Agent session, so do not assume that they inherit the current chat. For the first test:

- Use local results only.
- Do not select Telegram, Discord, Slack, email, or `all` delivery.
- Pause or remove the task immediately after the test.
- Check the number of runs because the task can consume Provider calls and cost.

### 8.2 Create it in Desktop

1. Select `content-planner` in the Bots tab.
2. Open its `Routines` tile.
3. Name the task `bot-mode-local-smoke`.
4. Enter:

```text
Record only the current time and “YouTube content production scheduled test” as a local result.
Do not send external messages, delete files, create files, or search the web.
```

5. Choose a one-time or short test schedule.
6. Select `local` if a Delivery field is shown.
7. Save and check the task in `hermes cron list` or the Routines list.

### 8.3 CLI check and cleanup

```bash
hermes cron create "10m" \
  "Record only the current time and 'YouTube content production scheduled test' locally; do not send anything externally." \
  --name "bot-mode-local-smoke"

hermes cron list
hermes cron status
```

After confirming the ID:

```bash
hermes cron runs <job_id> --limit 5
```

Remove the test when finished:

```bash
hermes cron pause <job_id>
hermes cron remove <job_id>
```

If it does not run, check `hermes gateway status`, `hermes cron status`, and `hermes cron list` in that order. Do not create more tasks until the Gateway scheduler is understood.

## 9. Local and remote execution boundaries

The default Desktop manages a local backend. A Remote gateway can connect to another machine, but it is outside the first practice.

When switching to Remote:

- The computer displaying Desktop and the computer executing tools may differ.
- Terminal commands, file work, and Agent tools run on the remote Hermes host.
- Configure the Remote URL and authentication under `Settings → Gateways`.
- Do not expose a Basic Auth backend to the public internet. The official security guidance recommends a trusted network or VPN for Basic Auth and OAuth for public access.

Record the display computer, Agent execution host, and authentication method separately when Remote is used.

## 10. Troubleshooting

| Symptom | First action | Stop and recover when |
| --- | --- | --- |
| `hermes: command not found` | Open a new shell or reload `.zshrc`/`.bashrc`; on Windows open a new PowerShell | Do not repeatedly rewrite PATH; record the install location and `hermes doctor` |
| Desktop opens but does not respond | Check Provider and model in `Settings → Providers` or `hermes model` | Do not record an API key; record only the authentication error text |
| `hermes doctor` reports dependency errors | Save the installation path and error, then consider `hermes update` | Do not mix several Python or Node installations manually |
| No Bots tab | Update Desktop and check `Settings → Plugins` | Do not clone the old Bot Mode repository first |
| New bot is not listed | Reload or restart Desktop, then run `hermes profile list` | Record duplicate names and Provider settings |
| Group chat is quiet | Check that both Profiles are in the group, the exact `@bot-name` was used, and each Profile has a Provider | Stop after one prompt; do not resend it repeatedly |
| Bot proposes file or external actions | Stop and do not approve; turn off `--yolo` and retry with read-only excerpts | Never treat Profile separation as a sandbox |
| Routine does not run | Check `hermes gateway status` → `hermes cron status` → `hermes cron list` → `hermes cron runs <job_id>` | Pause or remove the task before creating another |
| Remote shows a different file location | Check the active Gateway and execution host | Do not upload private files; return to local practice |

### About the old manual Bot Mode plugin

An archived README once showed this manual installation:

```text
git clone https://github.com/NousResearch/Hermes-Bot-Mode ~/.hermes/desktop-plugins/hermes-bots
```

Do not use that command as the current Desktop installation procedure. It is relevant only when reproducing an old build or a development environment. If it must be inspected, remember that the plugin belongs on the computer running the Desktop app, not on the Gateway.

## 11. Execution record card

Fill this in after the practice. Never record keys, tokens, or private material.

```yaml
execution_date: "YYYY-MM-DD HH:MM KST"
os: ""
installation_path: "Desktop installer | install.sh | install.ps1 | existing CLI"
hermes_version: ""
doctor_result: ""
provider: "name only"
model: "model name only"
desktop_smoke_test: "passed | failed | not run"
bot_mode: "built-in confirmed | not confirmed"
profiles:
  - name: content-planner
    result: ""
  - name: script-editor
    result: ""
group_chat: "passed | failed | not run"
routine: "not used | local test then removed | needs confirmation"
evidence: "capture or transcript location"
external_side_effect: "none | details"
known_gap: ""
next_safe_action: ""
```

### Suggested artifact boundary

Keep inputs, outputs, and evidence separate:

- Input: the current AI Gap YouTube package and the prompt
- Output: the content brief and shooting draft from the group chat
- Evidence: `hermes --version`, `hermes doctor`, the Bot Mode list, and the group chat screen
- Not run: any Provider, Desktop, Bot Mode, real filming, or upload step that has not actually been checked

## 12. Stop conditions and hand-off

Stop after the basic chat succeeds and the two Bot Mode Profiles are visible. If the group chat succeeds, do not add Routines, Messaging, and Remote all at once. Stop when external delivery, channel upload, or private material is required.

Use this hand-off sentence for the next session:

```text
Hermes Desktop and the basic chat are [passed/failed/not run].
The confirmed version is [version], and the Provider/model are [names].
Bot Mode is [built-in confirmed/not confirmed], and content-planner and script-editor are [status].
The YouTube production group chat is [passed/failed/not run], and external side effects are [none/details].
The next safe action is [review group result/check sources and screens/check a local Routine/troubleshoot].
```

## Case reference

This practice uses the current AI Gap YouTube content package: its scope, research, series angle, EP1 script, and source checklist. It does not mean filming, upload, or runtime execution has been completed.

## References

These are the Nous Research official materials checked on 2026-08-22:

1. [Hermes Agent official site](https://hermes-agent.nousresearch.com/) — Desktop download, OS support, and the version shown on the site
2. [Quickstart](https://hermes-agent.nousresearch.com/docs/getting-started/quickstart) — Provider selection, first-chat verification, and the recommended order for adding features
3. [Installation](https://hermes-agent.nousresearch.com/docs/getting-started/installation) — macOS, Windows, Linux, and WSL2 installation paths and dependencies
4. [Desktop App](https://hermes-agent.nousresearch.com/docs/user-guide/desktop) — shared state with CLI, built-in Bot Mode, Routines, and Remote Gateway
5. [Profiles](https://hermes-agent.nousresearch.com/docs/user-guide/profiles) — Profile state separation, creation, and security limits
6. [Scheduled Tasks (Cron)](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron) — scheduling, execution, verification, pausing, and removal
7. [Security](https://hermes-agent.nousresearch.com/docs/user-guide/security) — approvals, YOLO warnings, Gateway authentication, and the difference between Profiles and sandboxes
8. [Hermes Agent official repository](https://github.com/NousResearch/hermes-agent) — current source and documentation
9. [Hermes Bot Mode archived repository](https://github.com/NousResearch/Hermes-Bot-Mode) — historical plugin record and the move into Desktop
