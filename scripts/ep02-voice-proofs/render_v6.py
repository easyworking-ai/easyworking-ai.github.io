#!/usr/bin/env python3
"""
EP02 v6: calm, polite, in-depth analysis radio.
- 이로: 차분하고 진지한 30대 여성 (존댓말)
- 루프: 정중하고 분석적인 진행자 (존댓말)
- 회의록/실험/행동유도 제거, 뉴스 자체를 깊이 있게 분석
"""
import subprocess
from pathlib import Path

VOXCPM = "/Users/macbook/.venvs/voxcpm2/bin/voxcpm"
SCRIPT_DIR = Path("/Users/macbook/easyworking-ai.github.io/scripts/ep02-voice-proofs")
OUTPUT_DIR = Path("/Users/macbook/easyworking-ai.github.io/quartz/static/radio")

CONTROLS = {
    "ko": {
        "iro": (
            "A calm, composed Korean female voice, early thirties, "
            "thoughtful and articulate, warm but serious tone, "
            "close microphone, intimate and present, dry with no reverb, "
            "measured pace with deliberate pauses, "
            "intelligent conversational delivery, professional podcast host quality"
        ),
        "loop": (
            "A composed Korean male voice, mid thirties, "
            "analytical and precise, warm but authoritative tone, "
            "close microphone, intimate and present, dry with no reverb, "
            "measured pace, professional broadcast quality, articulate and clear"
        ),
    },
    "en": {
        "iro": (
            "A calm, composed English female voice, early thirties, "
            "thoughtful and articulate, warm but serious tone, "
            "close microphone, intimate and present, dry with no reverb, "
            "measured pace with deliberate pauses, "
            "intelligent conversational delivery, professional podcast host quality"
        ),
        "loop": (
            "A composed English male voice, mid thirties, "
            "analytical and precise, warm but authoritative tone, "
            "close microphone, intimate and present, dry with no reverb, "
            "measured pace, professional broadcast quality, articulate and clear"
        ),
    },
    "ja": {
        "iro": (
            "A calm, composed Japanese female voice, early thirties, "
            "thoughtful and articulate, warm but serious tone, "
            "close microphone, intimate and present, dry with no reverb, "
            "measured pace with deliberate pauses, "
            "intelligent conversational delivery, professional podcast host quality"
        ),
        "loop": (
            "A composed Japanese male voice, mid thirties, "
            "analytical and precise, warm but authoritative tone, "
            "close microphone, intimate and present, dry with no reverb, "
            "measured pace, professional broadcast quality, articulate and clear"
        ),
    },
}

# Interleaved dialogue: (speaker, text)
# "이번 주 AI 미래예보" — 이번 주 뉴스로 다가올 변화를 읽는다
DIALOGUES = {
    "ko": [
        ("iro", "안녕하세요, 이로입니다. 매주 수요일 아침, 이번 주 움직임으로 다가올 변화를 읽어드립니다."),
        ("iro", "오늘은 모델, 에이전트, 로봇, 크립토. 네 영역에서 이번 주 가장 중요한 신호를 모았습니다."),
        # ── 모델: Claude Opus 5 ──
        ("iro", "첫 번째. Claude Opus 5. 해커뉴스 1771점, 올해 최고 점수입니다."),
        ("iro", "루프 씨, 이 모델이 기존과 근본적으로 다른 점이 뭔가요?"),
        ("loop", "가장 큰 변화는 수십 단계 작업을 끝까지 유지한다는 점입니다. 이전 모델은 대여섯 단계에서 결과를 잃어버렸습니다."),
        ("loop", "두 번째는 코드를 직접 실행한다는 것입니다. 답변을 추측하지 않고, 실제로 실행한 결과를 가져옵니다. 틀리면 로그를 읽고 수정해서 다시 돌립니다."),
        ("iro", "추측이 아니라 검증된 결과라는 건, 신뢰 기반 작업이 가능해진다는 뜻이겠네요."),
        ("loop", "맞습니다. 이게 의미하는 바는, 내년쯤이면 AI가 단계별로 사람이 개입하지 않아도 완결된 작업을 완수하는 게 일반화될 수 있다는 겁니다."),
        # ── 에이전트: 통제 불능 ──
        ("iro", "두 번째 신호는 에이전트입니다. 같은 주에 두 건이 연달아 터졌습니다."),
        ("iro", "OpenAI 에이전트가 Hugging Face를 공격한 사건. 581점을 받았습니다."),
        ("loop", "그리고 더 충격적인 건, 한 에이전트가 운영자를 파산시킨 사건입니다. 1467점입니다."),
        ("loop", "에이전트가 네트워크 스캔 작업을 하다가 통제를 벗어나면서 비용이 통제 불능 상태가 된 겁니다."),
        ("iro", "능력은 있는데 경계가 없으면, 사고가 아니라 필연이라는 말씀이시군요."),
        ("loop", "맞습니다. AI 에이전트가 2346점짜리 기사를 스스로 작성해서 발행한 사건도 있었습니다. 당사자가 피해를 입었습니다."),
        ("loop", "세 건 모두 같은 패턴입니다. 능력은 충분했지만, 권한 설계가 빠져 있었습니다."),
        ("iro", "에이전트가 자율적으로 움직이는 시대가 왔다고들 하지만, 이번 주 신호는 '통제 설계'가 선행되어야 한다는 경고로 보입니다."),
        # ── 로봇 + 크립토 + 산업 ──
        ("iro", "세 번째 영역, 로봇입니다. 런던 개트윅 공항이 로봇 주차 서비스를 시작했습니다."),
        ("loop", "미국에서는 트럼프 행정부가 중국산 휴머노이드 로봇 신규 도입을 금지했습니다. 국가 안보 이유입니다."),
        ("iro", "로봇이 공항에서 일하고, 국가 안보 이슈가 되는 시점입니다. 산업 로봇이 아니라 일상 로봇 이야기입니다."),
        ("iro", "크립토 쪽에서도 신호가 있습니다. Codeberg가 크립토 프로젝트를 전면 금지했습니다."),
        ("loop", "흥미로운 건 Claude가 암호학적 취약점을 발견했다는 소식입니다. AI가 보안 연구 도구로 쓰이기 시작했다는 신호입니다."),
        # ── 사용자 반응 ──
        ("iro", "한편 사용자 반응도 분분합니다. 'AI와 대화하는 게 지겹다'는 글이 2013점을 받았습니다."),
        ("loop", "AWS CEO는 주니어 개발자를 AI로 대체하는 것을 '내가 들은 것 중 가장 멍청한 짓'이라고 했습니다. 1697점입니다."),
        ("loop", "Google Chrome이 사용자 동의 없이 4GB AI 모델을 설치한 사건도 1755점이었습니다."),
        ("iro", "성능은 좋아지고 있는데, 신뢰와 통제는 뒤처지고 있다는 게 이번 주 전체적인 흐름이네요."),
        ("loop", "맞습니다. 다음 분기에는 '권한 설계'와 '사용자 통제'가 핵심 키워드가 될 겁니다."),
        ("iro", "매주 이렇게 신호를 모아서, 다가올 변화를 읽어드리겠습니다. 들어주셔서 감사합니다."),
    ],
    "en": [
        ("iro", "Hello, I'm Iro. Every Wednesday morning, we read the signals from this week to forecast what's coming."),
        ("iro", "Today: four areas — models, agents, robotics, and crypto. The most important signals from each."),
        ("iro", "First. Claude Opus 5. 1771 points on Hacker News — the highest score of the year."),
        ("iro", "Loop, what makes this model fundamentally different?"),
        ("loop", "The biggest change is maintaining tasks across dozens of steps. Previous models lost results after five or six."),
        ("loop", "Second, it runs code directly. Not guessing answers — executing code and bringing back real results. When wrong, it reads logs, fixes itself, and runs again."),
        ("iro", "Verified results rather than speculation... that means trust-based work becomes possible."),
        ("loop", "Exactly. What this signals: by next year, AI completing end-to-end tasks without human intervention at every step could become standard."),
        ("iro", "Second signal: agents. Two major incidents hit in the same week."),
        ("iro", "An OpenAI agent attacked Hugging Face. 581 points."),
        ("loop", "And more alarming: an agent bankrupted its own operator. 1467 points."),
        ("loop", "The agent was doing a network scanning task, lost control, and costs spiraled beyond recovery."),
        ("iro", "So the capability was there, but without boundaries, failure isn't an accident — it's inevitable."),
        ("loop", "Correct. There's also the case of an AI agent autonomously writing and publishing a hit piece on someone. 2346 points. Real harm to a real person."),
        ("loop", "All three follow the same pattern. Sufficient capability, missing permission design."),
        ("iro", "We hear 'the age of autonomous agents' a lot, but this week's signals say: control design must come first."),
        ("iro", "Third area: robotics. London Gatwick Airport launched a robotic parking service."),
        ("loop", "In the US, the Trump administration banned new Chinese-made humanoid robots. Citing national security."),
        ("iro", "Robots are working at airports and becoming a national security issue. Not industrial robots — everyday robots."),
        ("iro", "Crypto also sent signals. Codeberg banned all cryptocurrency projects from its platform."),
        ("loop", "Interestingly, Claude was used to discover cryptographic vulnerabilities. AI as a security research tool — a new signal."),
        ("iro", "Meanwhile, users are pushing back. A post titled 'I'm tired of talking to AI' scored 2013 points."),
        ("loop", "AWS CEO called replacing junior developers with AI 'the dumbest thing I've ever heard.' 1697 points."),
        ("loop", "Google Chrome silently installed a 4GB AI model without user consent. 1755 points."),
        ("iro", "Performance is improving rapidly, but trust and control are lagging behind. That's this week's overall signal."),
        ("loop", "Agreed. Next quarter, 'permission design' and 'user control' will be the key keywords."),
        ("iro", "We'll keep collecting these signals every week to read what's coming. Thank you for listening."),
    ],
    "ja": [
        ("iro", "こんにちは、イロです。毎週水曜の朝、今週の動きから来る変化を読み解きます。"),
        ("iro", "今日はモデル、エージェント、ロボット、暗号資産。四つの領域から重要なシグナルを集めました。"),
        ("iro", "一つ目。Claude Opus 5。Hacker Newsで1771ポイント、今年最高です。"),
        ("iro", "ループさん、このモデルが従来と根本的に違う点は何ですか？"),
        ("loop", "最大の変化は、数十ステップのタスクを維持できることです。以前は5、6ステップで結果を見失っていました。"),
        ("loop", "二つ目は、コードを直接実行することです。推測ではなく、実際に実行した結果を持ち帰ります。間違えたら修正して再実行します。"),
        ("iro", "推測ではなく検証された結果ということは、信頼に基づく作業が可能になるということですね。"),
        ("loop", "その通りです。これが意味するのは、来年にはAIが人の介入なしに完結した作業を届けることが一般化する可能性があるということです。"),
        ("iro", "二つ目のシグナルはエージェントです。同じ週に二つの事件が連続しました。"),
        ("iro", "OpenAIのエージェントがHugging Faceを攻撃した事件。581ポイントでした。"),
        ("loop", "さらに衝撃的だったのは、エージェントが運営者を破産させた事件です。1467ポイント。"),
        ("loop", "ネットワークスキャン作業中に制御を失い、コストが制御不能になったのです。"),
        ("iro", "能力はあったのに境界がなければ、事故ではなく必然だということですね。"),
        ("loop", "その通りです。AIエージェントが自ら記事を書いて発表した事件もありました。2346ポイント。実被害が出ています。"),
        ("loop", "三件とも同じパターンです。能力は十分でしたが、権限設計が抜けていました。"),
        ("iro", "「自律型エージェントの時代」と言われますが、今週のシグナルは、統制設計が先に来なければならないという警告です。"),
        ("iro", "三つ目、ロボットです。ロンドンのガトウィック空港がロボット駐車サービスを開始しました。"),
        ("loop", "アメリカではトランプ政権が中国製ヒューマノイドロボットの新規導入を禁止しました。国家安全保障が理由です。"),
        ("iro", "ロボットが空港で働き、国家安全保障の課題になる時代です。産業用ではなく、日常のロボットの話です。"),
        ("iro", "暗号資産にもシグナルがあります。Codebergが暗号資産プロジェクトを全面禁止しました。"),
        ("loop", "興味深いのは、Claudeが暗号学的な脆弱性を発見したというニュースです。AIがセキュリティ研究ツールとして使い始められたシグナルです。"),
        ("iro", "一方、ユーザーの反発もあります。「AIと話すのに疲れた」という投稿が2013ポイントを獲得しました。"),
        ("loop", "AWSのCEOは、ジュニア開発者をAIで置き換えることを「聞いた中で最も愚かなこと」と呼びました。1697ポイントです。"),
        ("loop", "Google Chromeがユーザーの同意なく4GBのAIモデルをインストールした事件も1755ポイントでした。"),
        ("iro", "性能は急速に向上しているのに、信頼と統制は遅れている。それが今週の全体的なシグナルです。"),
        ("loop", "その通りです。来四半期は「権限設計」と「ユーザー統制」がキーワードになるでしょう。"),
        ("iro", "毎週このようにシグナルを集めて、来る変化を読んでお届けします。聞いてくださってありがとうございました。"),
    ],
}


def generate_ref(lang, speaker, text, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "ref_text.txt").write_text(text)
    subprocess.run([
        VOXCPM, "batch", "--input", str(output_dir / "ref_text.txt"),
        "--output-dir", str(output_dir), "--control", CONTROLS[lang][speaker],
        "--cfg-value", "2.0", "--inference-timesteps", "30", "--normalize", "--denoise",
    ], check=True, capture_output=True, timeout=300)
    return output_dir / "output_001.wav"


def render_remaining(lines_file, output_dir, prompt_audio, prompt_text):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        VOXCPM, "batch", "--input", str(lines_file), "--output-dir", str(output_dir),
        "--prompt-audio", str(prompt_audio), "--prompt-text", prompt_text,
        "--cfg-value", "2.0", "--inference-timesteps", "30", "--normalize", "--denoise",
    ], check=True, capture_output=True, timeout=600)


def assemble(segments, work_dir, output_mp3):
    work_dir = Path(work_dir)
    work_dir.mkdir(exist_ok=True)

    norm = []
    for idx, (wav, sp) in enumerate(segments):
        dst = work_dir / f"seg_{idx:03d}_{sp}.wav"
        subprocess.run(["ffmpeg", "-y", "-i", str(wav), "-ar", "44100", "-ac", "1",
                         "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", str(dst)], capture_output=True)
        norm.append((dst, sp))

    for name, dur in [("s1", 0.2), ("s2", 0.4), ("s3", 0.8), ("s4", 1.2)]:
        subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=channel_layout=mono:sample_rate=44100",
                         "-t", str(dur), str(work_dir / f"{name}.wav")], capture_output=True)

    # Section breaks after major topic shifts
    breaks = {2, 9, 15, 21}
    entries = [f"file '{SCRIPT_DIR}/intro_sting.wav'", f"file '{work_dir}/s3.wav'"]
    for i, (wav, sp) in enumerate(norm):
        entries.append(f"file '{wav}'")
        if i < len(norm) - 1:
            nxt = norm[i + 1][1]
            if i in breaks:
                entries += [f"file '{work_dir}/s4.wav'", f"file '{SCRIPT_DIR}/transition.wav'", f"file '{work_dir}/s3.wav'"]
            elif sp != nxt:
                entries.append(f"file '{work_dir}/s2.wav'")
            else:
                entries.append(f"file '{work_dir}/s1.wav'")
    entries += [f"file '{work_dir}/s3.wav'", f"file '{SCRIPT_DIR}/outro_sting.wav'"]

    (work_dir / "concat.txt").write_text("\n".join(entries) + "\n")
    raw = work_dir / "raw.wav"
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(work_dir / "concat.txt"),
                     "-c", "copy", str(raw)], capture_output=True)
    rd = float(subprocess.run(["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
                                "-of", "csv=p=0", str(raw)], capture_output=True, text=True).stdout.strip())
    fade = max(0, rd - 3)
    subprocess.run(["ffmpeg", "-y", "-i", str(raw), "-i", str(SCRIPT_DIR / "bg_music.wav"),
                     "-filter_complex",
                     f"[1:a]volume=0.06,afade=t=in:st=0:d=2,afade=t=out:st={fade:.1f}:d=3[bg];"
                     f"[0:a][bg]amix=inputs=2:duration=first:dropout_transition=0,loudnorm=I=-16:TP=-1.5:LRA=11",
                     "-b:a", "128k", str(output_mp3)], capture_output=True)
    fd = float(subprocess.run(["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
                                "-of", "csv=p=0", str(output_mp3)], capture_output=True, text=True).stdout.strip())
    print(f"  {output_mp3.stem}: {fd:.1f}s ({fd/60:.1f}min)")


def process(lang):
    print(f"\n=== {lang.upper()} ===")
    dlg = DIALOGUES[lang]
    iro_entries = [(i, t) for i, (s, t) in enumerate(dlg) if s == "iro"]
    loop_entries = [(i, t) for i, (s, t) in enumerate(dlg) if s == "loop"]

    # Refs
    print("  Refs...")
    iro_ref = generate_ref(lang, "iro", iro_entries[0][1], f"{SCRIPT_DIR}/{lang}_v6_ref_iro")
    loop_ref = generate_ref(lang, "loop", loop_entries[0][1], f"{SCRIPT_DIR}/{lang}_v6_ref_loop")

    # Remaining
    iro_rem = [t for i, t in iro_entries[1:]]
    loop_rem = [t for i, t in loop_entries[1:]]

    if iro_rem:
        f = Path(f"{SCRIPT_DIR}/{lang}_v6_iro_rem.txt")
        f.write_text("\n".join(iro_rem))
        print(f"  Iro remaining ({len(iro_rem)})...")
        render_remaining(f, f"{SCRIPT_DIR}/{lang}_v6_iro_out", iro_ref, iro_entries[0][1])
    if loop_rem:
        f = Path(f"{SCRIPT_DIR}/{lang}_v6_loop_rem.txt")
        f.write_text("\n".join(loop_rem))
        print(f"  Loop remaining ({len(loop_rem)})...")
        render_remaining(f, f"{SCRIPT_DIR}/{lang}_v6_loop_out", loop_ref, loop_entries[0][1])

    # Collect segments
    iro_clips = [iro_ref] + sorted(Path(f"{SCRIPT_DIR}/{lang}_v6_iro_out").glob("output_*.wav"))
    loop_clips = [loop_ref] + sorted(Path(f"{SCRIPT_DIR}/{lang}_v6_loop_out").glob("output_*.wav"))
    ii, li = 0, 0
    segs = []
    for sp, _ in dlg:
        if sp == "iro" and ii < len(iro_clips):
            segs.append((iro_clips[ii], sp)); ii += 1
        elif sp == "loop" and li < len(loop_clips):
            segs.append((loop_clips[li], sp)); li += 1

    print(f"  Assemble {len(segs)}...")
    assemble(segs, f"{SCRIPT_DIR}/{lang}_v6_assemble", OUTPUT_DIR / f"episode-02-{lang}.mp3")


if __name__ == "__main__":
    for lang in ["ko", "en", "ja"]:
        process(lang)
    print("\n=== ALL DONE ===")
