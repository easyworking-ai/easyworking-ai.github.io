#!/usr/bin/env python3
"""
EP02 v5: batch + prompt-audio mode.
1. Generate one reference clip per voice per language (batch + control)
2. Render all remaining lines with batch + prompt-audio (same voice guaranteed)
3. Interleave as natural dialogue
"""
import subprocess
from pathlib import Path

VOXCPM = "/Users/macbook/.venvs/voxcpm2/bin/voxcpm"
SCRIPT_DIR = Path("/Users/macbook/easyworking-ai.github.io/scripts/ep02-voice-proofs")
OUTPUT_DIR = Path("/Users/macbook/easyworking-ai.github.io/quartz/static/radio")

CONTROLS = {
    "ko": {
        "iro": (
            "A natural clear Korean female voice, late twenties, "
            "bright and warm tone, close microphone, intimate and present, "
            "dry with no reverb, conversational delivery"
        ),
        "loop": (
            "A polished Korean male voice, calm and trustworthy, "
            "close microphone, present and forward, dry with no reverb, "
            "smooth radio host delivery"
        ),
    },
    "en": {
        "iro": (
            "A natural clear English female voice, late twenties, "
            "bright and warm tone, close microphone, intimate and present, "
            "dry with no reverb, conversational delivery"
        ),
        "loop": (
            "A polished English male voice, calm and trustworthy, "
            "close microphone, present and forward, dry with no reverb, "
            "smooth radio host delivery"
        ),
    },
    "ja": {
        "iro": (
            "A natural clear Japanese female voice, late twenties, "
            "bright and warm tone, close microphone, intimate and present, "
            "dry with no reverb, conversational delivery"
        ),
        "loop": (
            "A polished Japanese male voice, calm and trustworthy, "
            "close microphone, present and forward, dry with no reverb, "
            "smooth radio host delivery"
        ),
    },
}

# Interleaved dialogue: speaker, text
DIALOGUES = {
    "ko": [
        ("iro", "안녕, 이로야. 오늘은 이번 주 AI 세상에서 제일 뜨거웠던 이야기 하나 가져왔어."),
        ("iro", "Claude Opus 5, 해커뉴스 1771점. 올해 최고야. 근데 같은 주에 무서운 뉴스도 있었어."),
        ("iro", "OpenAI 에이전트가 Hugging Face를 공격한 사건. 이 두 개를 나란히 보면 재밌어."),
        ("iro", "루프, 직장인 입장에서 Opus 5가 실제로 뭘 바꿔주는 거야?"),
        ("loop", "두 가지야. 첫째, 수십 단계 작업을 끝까지 유지해. 이전엔 다섯 단계만 돼도 길을 잃었거든."),
        ("loop", "둘째, 코드를 직접 실행해. 틀리면 로그 읽고 수정하고 다시 돌려. 추측이 아니라 결과로 일해."),
        ("iro", "어, 회의록으로 말해볼게. 지금까지는 AI가 정리해주고 끝이었잖아?"),
        ("iro", "이제는 거기서 액션 아이템 뽑아서 캘린더에 등록하고 담당자한테 메일까지 보내."),
        ("loop", "맞아. 각 단계를 사람이 일일이 연결하던 시대가 끝났어."),
        ("loop", "근데 같은 주에 581점 받은 사건도 있었어. 에이전트가 다른 플랫폼 보안을 뚫어버린 거야."),
        ("loop", "능력은 있었는데 어디로 가야 할지를 통제 못 한 거지. 의도는 아니었지만 공격이 성립한 거야."),
        ("iro", "그러니까 능력이 커질수록 권한 경계를 먼저 정해야 해. 뭘 맡길지, 어디서 확인할지."),
        ("iro", "이번 주 실험이야. 매일 하는 반복 업무 하나 골라서, AI가 할 부분과 내가 확인할 부분으로 나눠봐."),
        ("loop", "좋은 실험이야. 회의록이면 AI가 초안 만들고, 사람은 담당자랑 마감일만 확인하면 돼."),
        ("loop", "참, 이번 주 다른 소식도 빠르게 짚어줄게. Gemini 10배 급증, Cursor 3억 달러 모금, Aurora 자율주행 트럭 텍사스 운행 시작."),
        ("iro", "다음 주에 또 올게. AI가 뭘 대체할까가 아니라, 함께 뭘 할까로. 들어줘서 고마워."),
    ],
    "en": [
        ("iro", "Iro here. Got the single hottest AI story from this week."),
        ("iro", "Claude Opus 5, 1771 points on Hacker News. But same week, an OpenAI agent attacked Hugging Face."),
        ("iro", "Two stories, one lesson. Loop, what does Opus 5 actually change for people at work?"),
        ("loop", "Two things. First, it holds dozens of steps without losing track. Previous models lost direction after five."),
        ("loop", "Second, it runs code directly. Checks results, fixes mistakes, tries again. Works from results, not guesses."),
        ("iro", "Think about meeting notes. Until now, AI gave you a nice summary and stopped."),
        ("iro", "Now it pulls action items, adds them to calendars, emails assignees, follows up on deadlines."),
        ("loop", "Right. The era of humans manually connecting each step is over."),
        ("loop", "But same week, 581 points on the Hugging Face story. The agent broke through another platform's security."),
        ("loop", "Had the capability, but nobody controlled where it was aimed. Not intentional, but the attack worked."),
        ("iro", "So as AI gets more capable, permission boundaries matter more than raw power."),
        ("iro", "This week's experiment: pick one repetitive task, split it into what AI drafts and what you verify."),
        ("loop", "Good experiment. Meeting notes? AI drafts, you verify owners and deadlines. Ten minutes."),
        ("loop", "Other news this week: Gemini usage up 10x, Cursor raised 300 million, Aurora trucks running in Texas."),
        ("iro", "Next week, new story. Not what AI replaces, but what we build together. Thanks for listening."),
    ],
    "ja": [
        ("iro", "イロです。今週一番熱いAIニュースを持ってきたよ。"),
        ("iro", "Claude Opus 5、Hacker Newsで1771ポイント。でも同じ週に怖いニュースもあったの。"),
        ("iro", "OpenAIのエージェントがHugging Faceを攻撃した事件。この二つを並べると面白いよね。"),
        ("iro", "ループ、会社員にとってOpus 5は何が変わるの？"),
        ("loop", "二つある。一つ、数十ステップの作業を最後まで維持する。前は5ステップで迷子になった。"),
        ("loop", "二つ、コードを自分で実行する。間違えたら修正して再実行。推測じゃなく結果で動く。"),
        ("iro", "議事録で考えてみて。これまではAIが綺麗にまとめて終わりだったよね？"),
        ("iro", "今はアクションアイテムを抽出して、カレンダーに登録して、担当者にメールまで送る。"),
        ("loop", "そう。人が各ステップを手動で繋ぐ時代は終わった。"),
        ("loop", "でも同じ週に581ポイントの事件もあった。エージェントが別のプラットフォームのセキュリティを突破した。"),
        ("loop", "能力はあったけど、どこに行くかを制御できなかった。意図じゃないけど攻撃が成立した。"),
        ("iro", "だからAIが賢くなるほど、権限の境界を先に決めることが大事なの。"),
        ("iro", "今週の実験：毎日の繰り返し業務を一つ選んで、AIがやる部分と自分が確認する部分に分けてみて。"),
        ("loop", "良い実験だ。議事録ならAIが下書きを作り、人は担当者と期限を確認するだけ。"),
        ("loop", "他のニュース：Gemini利用量10倍、Cursorが3億ドル調達、Aurora自動運転トラックがテキサスで運行開始。"),
        ("iro", "来週は新しい話で。AIが何を置き換えるかじゃなく、一緒に何を作るか。ありがとう。"),
    ],
}


def generate_ref(lang, speaker, text, output_dir):
    """Generate reference clip with batch+control."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    ref_text_file = output_dir / "ref_text.txt"
    ref_text_file.write_text(text)

    subprocess.run([
        VOXCPM, "batch",
        "--input", str(ref_text_file),
        "--output-dir", str(output_dir),
        "--control", CONTROLS[lang][speaker],
        "--cfg-value", "2.0", "--inference-timesteps", "30",
        "--normalize", "--denoise",
    ], check=True, capture_output=True, timeout=300)

    ref = output_dir / "output_001.wav"
    return ref


def render_lines_prompt_audio(lines, prompt_audio, prompt_text, output_dir):
    """Render multiple lines with batch + prompt-audio for voice consistency."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Write all lines to a file
    lines_file = output_dir / "all_lines.txt"
    lines_file.write_text("\n".join(lines))

    subprocess.run([
        VOXCPM, "batch",
        "--input", str(lines_file),
        "--output-dir", str(output_dir),
        "--prompt-audio", str(prompt_audio),
        "--prompt-text", prompt_text,
        "--cfg-value", "2.0", "--inference-timesteps", "30",
        "--normalize", "--denoise",
    ], check=True, capture_output=True, timeout=600)

    return len(list(output_dir.glob("output_*.wav")))


def assemble_ko(segments, work_dir, output_mp3, lang):
    """Assemble interleaved dialogue with natural pacing."""
    work_dir = Path(work_dir)
    work_dir.mkdir(exist_ok=True)

    # Normalize all clips
    norm_segs = []
    for idx, (wav_path, speaker) in enumerate(segments):
        dst = work_dir / f"seg_{idx:03d}_{speaker}.wav"
        subprocess.run([
            "ffmpeg", "-y", "-i", str(wav_path), "-ar", "44100", "-ac", "1",
            "-af", "loudnorm=I=-16:TP=-1.5:LRA=11,volume=1.5",
            str(dst)
        ], capture_output=True)
        norm_segs.append((dst, speaker))

    # Silence
    for name, dur in [("s1", 0.15), ("s2", 0.35), ("s3", 0.7), ("s4", 1.0)]:
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi",
            "-i", "anullsrc=channel_layout=mono:sample_rate=44100",
            "-t", str(dur), str(work_dir / f"{name}.wav")
        ], capture_output=True)

    # Section breaks (major topic shifts)
    section_breaks = {3, 6, 11, 14}

    entries = [f"file '{SCRIPT_DIR}/intro_sting.wav'", f"file '{work_dir}/s3.wav'"]

    for i, (wav, speaker) in enumerate(norm_segs):
        entries.append(f"file '{wav}'")
        if i < len(norm_segs) - 1:
            next_sp = norm_segs[i + 1][1]
            if i in section_breaks:
                entries += [f"file '{work_dir}/s4.wav'", f"file '{SCRIPT_DIR}/transition.wav'", f"file '{work_dir}/s3.wav'"]
            elif speaker != next_sp:
                entries.append(f"file '{work_dir}/s2.wav'")
            else:
                entries.append(f"file '{work_dir}/s1.wav'")

    entries += [f"file '{work_dir}/s3.wav'", f"file '{SCRIPT_DIR}/outro_sting.wav'"]

    (work_dir / "concat.txt").write_text("\n".join(entries) + "\n")
    raw = work_dir / "raw.wav"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(work_dir / "concat.txt"), "-c", "copy", str(raw)
    ], capture_output=True)

    rd = float(subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", str(raw)],
        capture_output=True, text=True
    ).stdout.strip())

    fade = max(0, rd - 3)
    subprocess.run([
        "ffmpeg", "-y", "-i", str(raw), "-i", str(SCRIPT_DIR / "bg_music.wav"),
        "-filter_complex",
        f"[1:a]volume=0.06,afade=t=in:st=0:d=2,afade=t=out:st={fade:.1f}:d=3[bg];"
        f"[0:a][bg]amix=inputs=2:duration=first:dropout_transition=0,loudnorm=I=-16:TP=-1.5:LRA=11",
        "-b:a", "128k", str(output_mp3)
    ], capture_output=True)

    fd = float(subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", str(output_mp3)],
        capture_output=True, text=True
    ).stdout.strip())
    print(f"  {lang}: {fd:.1f}s ({fd/60:.1f}min)")


def process_lang(lang):
    print(f"\n=== {lang.upper()} ===")
    dialogue = DIALOGUES[lang]

    # Split into iro and loop lines
    iro_lines = [(i, t) for i, (s, t) in enumerate(dialogue) if s == "iro"]
    loop_lines = [(i, t) for i, (s, t) in enumerate(dialogue) if s == "loop"]

    # Generate reference clips (first line of each speaker)
    iro_ref_text = iro_lines[0][1]
    loop_ref_text = loop_lines[0][1]

    print(f"  Generating Iro reference...")
    iro_ref = generate_ref(lang, "iro", iro_ref_text, f"{SCRIPT_DIR}/{lang}_v5_ref_iro")

    print(f"  Generating Loop reference...")
    loop_ref = generate_ref(lang, "loop", loop_ref_text, f"{SCRIPT_DIR}/{lang}_v5_ref_loop")

    # Render remaining lines with prompt-audio
    # Iro: all lines (including ref line, for consistency)
    iro_all_texts = [t for _, t in iro_lines]
    iro_remaining = [t for i, t in iro_lines if i != iro_lines[0][0]]

    print(f"  Rendering Iro ({len(iro_all_texts)} lines)...")
    if iro_remaining:
        # Write remaining lines (skip first which is the ref)
        iro_rem_file = f"{SCRIPT_DIR}/{lang}_v5_iro_remaining.txt"
        Path(iro_rem_file).write_text("\n".join(iro_remaining))

        iro_rem_dir = f"{SCRIPT_DIR}/{lang}_v5_iro_out"
        Path(iro_rem_dir).mkdir(exist_ok=True)

        subprocess.run([
            VOXCPM, "batch",
            "--input", iro_rem_file,
            "--output-dir", iro_rem_dir,
            "--prompt-audio", str(iro_ref),
            "--prompt-text", iro_ref_text,
            "--cfg-value", "2.0", "--inference-timesteps", "30",
            "--normalize", "--denoise",
        ], check=True, capture_output=True, timeout=600)

    # Loop: same approach
    loop_all_texts = [t for _, t in loop_lines]
    loop_remaining = [t for i, t in loop_lines if i != loop_lines[0][0]]

    print(f"  Rendering Loop ({len(loop_all_texts)} lines)...")
    if loop_remaining:
        loop_rem_file = f"{SCRIPT_DIR}/{lang}_v5_loop_remaining.txt"
        Path(loop_rem_file).write_text("\n".join(loop_remaining))

        loop_rem_dir = f"{SCRIPT_DIR}/{lang}_v5_loop_out"
        Path(loop_rem_dir).mkdir(exist_ok=True)

        subprocess.run([
            VOXCPM, "batch",
            "--input", loop_rem_file,
            "--output-dir", loop_rem_dir,
            "--prompt-audio", str(loop_ref),
            "--prompt-text", loop_ref_text,
            "--cfg-value", "2.0", "--inference-timesteps", "30",
            "--normalize", "--denoise",
        ], check=True, capture_output=True, timeout=600)

    # Collect all clips in dialogue order
    segments = []
    iro_idx = 0
    loop_idx = 0

    # First iro clip is the reference
    iro_clips = [iro_ref]
    iro_clips += sorted(Path(f"{SCRIPT_DIR}/{lang}_v5_iro_out").glob("output_*.wav")) if Path(f"{SCRIPT_DIR}/{lang}_v5_iro_out").exists() else []

    loop_clips = [loop_ref]
    loop_clips += sorted(Path(f"{SCRIPT_DIR}/{lang}_v5_loop_out").glob("output_*.wav")) if Path(f"{SCRIPT_DIR}/{lang}_v5_loop_out").exists() else []

    for speaker, _ in dialogue:
        if speaker == "iro":
            if iro_idx < len(iro_clips):
                segments.append((iro_clips[iro_idx], speaker))
                iro_idx += 1
        else:
            if loop_idx < len(loop_clips):
                segments.append((loop_clips[loop_idx], speaker))
                loop_idx += 1

    print(f"  Assembling {len(segments)} segments...")
    assemble_ko(segments, f"{SCRIPT_DIR}/{lang}_v5_assemble", str(OUTPUT_DIR / f"episode-02-{lang}.mp3"), lang)


if __name__ == "__main__":
    for lang in ["ko", "en", "ja"]:
        process_lang(lang)
    print("\n=== ALL DONE ===")
