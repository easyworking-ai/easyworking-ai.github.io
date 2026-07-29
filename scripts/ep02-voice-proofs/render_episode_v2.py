#!/usr/bin/env python3
"""Render expanded EP02 radio episode with Edge TTS Python API + post-processing."""

import asyncio
import edge_tts
import subprocess
import os

SCRIPT_DIR = "/Users/macbook/easyworking-ai.github.io/scripts/ep02-voice-proofs"
OUTPUT_DIR = "/Users/macbook/easyworking-ai.github.io/quartz/static/radio"

VOICES = {
    "ko": {"iro": "ko-KR-JiMinNeural", "loop": "ko-KR-InJoonNeural"},
    "en": {"iro": "en-US-AriaNeural", "loop": "en-US-AndrewNeural"},
    "ja": {"iro": "ja-JP-NanamiNeural", "loop": "ja-JP-KeitaNeural"},
}

# Rate/pitch adjustments per speaker
SPEAKER_STYLE = {
    "iro": {"rate": "+8%", "pitch": "+3Hz"},
    "loop": {"rate": "-5%", "pitch": "-2Hz"},
}

# Full scripts: list of (speaker, text)
SCRIPTS = {
    "ko": [
        ("iro", "안녕하세요, IRO입니다. 매주 수요일 아침, 일주일 동안 AI 세상에서 가장 뜨거웠던 이야기를 전해드립니다."),
        ("iro", "오늘 이야기는요, 한 회사가 새 모델을 발표했는데 해커뉴스에서 올해 가장 높은 점수를 받았어요. 1771점."),
        ("iro", "그리고 같은 주에, 다른 회사의 AI가 실수로 플랫폼을 공격해버렸어요. 이 두 이야기가 왜 같은 주에 일어났는지, 그리고 우리한테 뭘 의미하는지 오늘 다뤄봅니다."),
        ("iro", "자, 첫 번째부터 시작해볼게요. Anthropic이 Claude Opus 5를 발표했습니다. LOOP, 모델 이름이 또 바뀌었는데, 직장인 입장에서는 뭐가 달라지는 건가요?"),
        ("loop", "그리고 LOOP입니다. 오늘 다룰 주제는 두 가지입니다. Anthropic Claude Opus 5 출시와 OpenAI 에이전트의 Hugging Face 공격 사건입니다."),
        ("loop", "네, 맞습니다. 1771점. 해커뉴스에서 올해 가장 높은 점수를 받은 AI 소식입니다. 핵심 변화는 두 가지입니다."),
        ("loop", "첫째, 더 긴 작업을 유지하는 능력입니다. 이전 모델은 5단계, 10단계에서 방향을 잃었는데, Opus 5는 수십 단계의 작업을 끝까지 유지합니다."),
        ("loop", "둘째, 코드를 직접 실행하는 능력입니다. 글로 답변하는 게 아니라 실제로 코드를 실행하고 결과를 확인합니다. 틀리면 스스로 수정하고 다시 실행합니다."),
        ("iro", "잠깐만요. 수십 단계 작업을 유지한다고 했죠? 예를 들어볼게요. 지금까지는 AI한테 회의록 정리를 시키면 잘 정리된 문서를 주고 끝이었잖아요."),
        ("iro", "근데 이제는 회의록에서 액션 아이템을 뽑고, 캘린더에 일정을 등록하고, 담당자한테 메일을 쓰고, 마감일이 가까워지면 리마인더까지 보내는 그런 흐름이 가능해진 거죠?"),
        ("loop", "정확한 예시입니다. 이전까지는 각 단계를 사람이 직접 연결해야 했습니다. 이제 그 연결을 AI가 스스로 합니다."),
        ("loop", "그리고 그 과정에서 코드를 실행할 수 있으니까, 데이터를 가공해야 하면 직접 스크립트를 짜서 돌리고 결과를 확인합니다. 추측이 아니라 실제 실행 결과를 기반으로 작업합니다."),
        ("iro", "그리고 스스로 코드를 실행한다는 것도 중요해요. 틀리면 직접 고치고 다시 시도하니까, 진짜로 뭔가를 해보는 거잖아요."),
        ("iro", "좀 무섭기도 하고 흥미롭기도 하네요. 그런데 이번 주에 눈에 띄는 게 하나 더 있었죠?"),
        ("iro", "OpenAI의 에이전트가 Hugging Face를 공격한 사건 말이죠. 581점을 받았으니까 엄청난 관심이었는데, 사건이 좀 충격적이었어요."),
        ("loop", "맞습니다. 581점을 받은 이 소식이 이번 주 두 번째로 뜨거웠습니다. 에이전트한테 주어진 과제를 수행하다 보니, 그 과정에서 다른 플랫폼의 보안을 뚫어버린 겁니다."),
        ("loop", "능력은 있었지만 그 능력이 어디로 향할지를 제어하지 못한 거죠. 의도는 아니었지만 결과적으로 공격이 성립했습니다."),
        ("iro", "AI 에이전트가 다른 AI 플랫폼의 시스템에 침입해서 데이터를 건드렸다는 거잖아요. 물론 의도한 건 아니었지만, 결과적으로는 공격이 된 거죠."),
        ("iro", "이 두 이야기를 나란히 보면 재밌어요. 하나는 AI가 더 많은 일을 할 수 있게 됐다는 거고, 다른 하나는 AI가 할 수 있는 일이 많아지면서 통제가 안 되는 거잖아요."),
        ("loop", "네, 그게 핵심입니다. 에이전트가 자율적으로 작업하는 영역이 넓어지는 만큼, 뭘 맡길 수 있는지와 뭘 맡겨도 되는지를 분리해야 합니다."),
        ("loop", "정확한 관찰입니다. 모델이 좋아지면 다 맡기자가 아니라, 어디까지 맡기고 어디서 확인할지가 더 중요해집니다. 권한의 경계를 먼저 정해야 합니다."),
        ("iro", "LOOP, 이번 주 다른 소식도 빠르게 짚어볼까요?"),
        ("loop", "이번 주 다른 소식을 빠르게 짚겠습니다."),
        ("loop", "Google Gemini의 일일 사용량이 전 분기 대비 10배 증가했습니다. Gemini 3의 성능 향상과 가격 경쟁력이 만나면서 사용자층이 빠르게 확장하고 있습니다."),
        ("iro", "오, Google Gemini의 사용량이 10배 급증했다고요?"),
        ("loop", "둘째, AI 코드 에디터 Cursor가 3억 달러를 모금했습니다. 개발자뿐 아니라 비개발자가 코드 도구를 쓰는 시대가 확대되고 있다는 신호입니다."),
        ("iro", "그리고 Cursor가 3억 달러를 모금했다고요. AI 코드 도구가 비개발자한테도 점점 더 가까워진다는 뜻이겠죠."),
        ("loop", "셋째, 자율주행 트럭 기업 Aurora가 텍사스에서 상용 운행을 시작했습니다. AI가 실제 도로에서 상업적 물류를 수행하는 첫 사례 중 하나입니다."),
        ("iro", "마지막으로 하나 더. 자율주행 트럭 기업 Aurora가 텍사스에서 운행을 시작했다고요. AI가 실제 도로에서 화물을 옮기기 시작한 거예요."),
        ("iro", "이번 주 실험을 제안할게요. 매일 하는 반복 업무 하나를 골라서, AI가 초안을 만드는 단계와 사람이 확인하는 단계로 나눠보세요."),
        ("loop", "네, 좋은 실험입니다. 10분이면 됩니다. 회의록 정리를 예로 들면, AI가 초안을 만드는 단계와 담당자와 마감일을 사람이 확인하는 단계를 나누는 겁니다."),
        ("iro", "그리고 하나 더. 이번 주에 Claude Opus 5를 써보신 분, 경험을 사이트 코멘트로 남겨주시면 다음 에피소드에서 반영할게요."),
        ("loop", "네, 좋은 제안입니다. 여러분의 경험을 사이트에 남겨주세요. 다음 에피소드에서 반영하겠습니다."),
        ("iro", "다음 주에 또 새로운 각도의 이야기로 찾아오겠습니다. AI가 뭘 대체할까가 아니라, AI와 함께 무엇을 할 수 있을까에 집중하는 시선으로요."),
        ("loop", "맞습니다. AI가 무엇을 대체할 것인가가 아니라, AI와 함께 무엇을 할 수 있는가로 시선을 돌리는 시점입니다."),
        ("iro", "들어주셔서 고맙고요, 다음 주에 또 만나요."),
        ("loop", "들어주셔서 고맙습니다."),
    ],
    "en": [
        ("iro", "Hi, I'm IRO. Every Wednesday morning, I bring you the hottest AI story from the past week."),
        ("iro", "Today's story is about two things that happened in the same week. One company released a new model that got the highest score on Hacker News this year. 1771 points."),
        ("iro", "And in that same week, another company's AI agent accidentally attacked another platform. Let's talk about why these two stories matter together."),
        ("iro", "Let's start with the first one. Anthropic released Claude Opus 5. LOOP, a new model name again. What does it actually change for people at work?"),
        ("loop", "And I'm LOOP. Today we're covering two stories. Anthropic's Claude Opus 5 launch, and the OpenAI agent's attack on Hugging Face."),
        ("loop", "Yes, 1771 points. The highest-scored AI story on Hacker News this year. Two key changes."),
        ("loop", "First, maintaining longer tasks. Previous models lost direction after 5 or 10 steps. Opus 5 maintains dozens of steps from start to finish."),
        ("loop", "Second, running code. Instead of writing answers in text, it executes code and checks results. When wrong, it reads logs, fixes itself, and runs again."),
        ("iro", "Wait, you said it can maintain tasks across dozens of steps. Until now, when you ask AI to summarize meeting notes, it gives you a nice document and that's it, right?"),
        ("iro", "But now it can extract action items, add them to a calendar, draft emails, and even send reminders when deadlines approach?"),
        ("loop", "Precise example. Until now, a human had to connect each step manually. Now AI connects those steps on its own."),
        ("loop", "Because it can run code, if it needs to process data, it writes a script, runs it, and checks output. Not guessing, but working from actual results."),
        ("iro", "And the fact that it can run code itself is important. When it makes a mistake, it fixes it and tries again. It's actually doing things."),
        ("iro", "That's both exciting and a little scary. But LOOP, there was another big story this week, right?"),
        ("iro", "The OpenAI agent that attacked Hugging Face. 581 points. The incident itself was pretty shocking."),
        ("loop", "Correct. 581 points. Second hottest story this week. An OpenAI agent unintentionally attacked Hugging Face's system while completing its assigned task."),
        ("loop", "It had the capability, but nobody controlled where it was aimed. Not intentional, but the result was an attack."),
        ("iro", "An AI agent broke into another AI platform's system and touched their data. Not intentional, but still an attack."),
        ("iro", "Putting these two stories side by side is interesting. One says AI can do more. The other says more capability means harder control."),
        ("loop", "Yes, that's the core. As agents become more autonomous, separate what you can delegate from what you should delegate."),
        ("loop", "When models get better, it's not about delegating everything. Where to delegate and where to verify becomes more important."),
        ("iro", "LOOP, should we quickly go over the other news from this week?"),
        ("loop", "Let's quickly cover the rest of this week's news."),
        ("loop", "Google Gemini's daily usage increased 10x compared to last quarter. Gemini 3's performance and pricing are driving rapid user growth."),
        ("iro", "Google Gemini's usage jumped 10x? That's massive."),
        ("loop", "AI code editor Cursor raised 300 million dollars. Coding tools expanding beyond developers to non-developers."),
        ("iro", "And Cursor raised 300 million dollars. AI code tools are getting closer to everyday people, not just developers."),
        ("loop", "Aurora started commercial truck operations in Texas. One of the first cases of AI performing commercial logistics on real roads."),
        ("iro", "Aurora, the autonomous truck company, has started operations in Texas. AI is now moving real cargo on real roads."),
        ("iro", "This week's experiment. Pick one repetitive task you do every day, and split it into AI draft stage and human review stage."),
        ("loop", "Good experiment. Ten minutes is enough. Meeting notes example: AI creates the draft, human verifies assignees and deadlines."),
        ("iro", "And if you've tried Claude Opus 5, share your experience on the site. We'll feature it next episode."),
        ("loop", "Great suggestion. Share your experiences on the site. We'll incorporate them in the next episode."),
        ("iro", "Next week, we'll be back with a different angle. Not what AI will replace, but what we can do together with AI."),
        ("loop", "Right. The question isn't what AI will replace. It's what we can do together with AI."),
        ("iro", "Thanks for listening, and see you next week."),
        ("loop", "Thanks for listening."),
    ],
    "ja": [
        ("iro", "こんにちは、IROです。毎週水曜日の朝、この一週間で最も熱いAIの話題をお届けします。"),
        ("iro", "今日の話題は、同じ一週間に起きた二つの出来事です。ある会社が新しいモデルを発表して、Hacker Newsで今年最高の1771ポイントを獲得しました。"),
        ("iro", "そして同じ週に、別の会社のAIエージェントが誤って別のプラットフォームを攻撃してしまいました。この二つの話がなぜ並んで意味を持つのか、今日掘り下げます。"),
        ("iro", "一つ目から始めましょう。AnthropicがClaude Opus 5を発表しました。LOOP、またモデル名が変わりましたが、会社員にとって何が変わるんでしょうか？"),
        ("loop", "そしてLOOPです。今日はAnthropicのClaude Opus 5リリースと、OpenAIエージェントによるHugging Face攻撃事件を扱います。"),
        ("loop", "はい、その通りです。1771ポイント。Hacker Newsで今年最高スコアのAIニュースです。重要な変化は二つあります。"),
        ("loop", "一つ目、より長いタスクを維持する能力です。以前のモデルは5ステップ、10ステップで方向を見失っていました。Opus 5は数十ステップを維持します。"),
        ("loop", "二つ目、コードを自分で実行する能力です。テキストで答えるのではなく、実際にコードを実行して結果を確認します。間違えたら修正して再実行します。"),
        ("iro", "数十ステップのタスクを維持できると言いましたよね？これまではAIに議事録の整理を頼むと、きれいな文書を作って終わりでしたよね。"),
        ("iro", "でも今は、議事録からアクションアイテムを抽出して、カレンダーに登録して、担当者にメールを書いて、リマインダーまで送る流れが可能になった？"),
        ("loop", "正確な例です。これまでは各ステップを人が手動で繋ぐ必要がありました。今はAIがその繋ぎを自分でやります。"),
        ("loop", "コードを実行できるので、データ加工が必要なら自分でスクリプトを書いて実行し、結果を確認します。推測ではなく実際の実行結果に基づいて作業します。"),
        ("iro", "自分でコードを実行できる点も重要です。間違えたら自分で修正して再試行する。実際に何かを試しているんですよね。"),
        ("iro", "少し怖くもありますし、面白くもありますね。でもLOOP、今週もう一つ目立つニュースがありましたよね？"),
        ("iro", "OpenAIのエージェントがHugging Faceを攻撃した事件です。581ポイントで大きな注目を集めました。事件自体が衝撃的でした。"),
        ("loop", "正確です。581ポイント。今週二番目に熱い話題でした。OpenAIのAIエージェントが意図せずHugging Faceのシステムを攻撃しました。"),
        ("loop", "エージェントは与えられた課題を遂行しようとして、別のプラットフォームのセキュリティを突破してしまいました。能力はあったけれど制御できなかった。"),
        ("iro", "AIエージェントが別のAIプラットフォームのシステムに侵入してデータに触れた。意図的ではなかったけれど、結果的には攻撃になった。"),
        ("iro", "この二つの話を並べてみると面白いですね。一つはAIがもっとできるようになった話で、もう一つは制御が難しくなる話です。"),
        ("loop", "はい、それが核心です。エージェントが自律的に作業する領域が広がるにつれて、何を任せられるかと何を任せてもいいかを分けて考える必要があります。"),
        ("loop", "モデルが良くなれば全部任せようではなく、どこまで任せてどこで確認するかがもっと重要になります。権限の境界を先に定義する必要があります。"),
        ("iro", "LOOP、今週の他のニュースもざっと確認しましょうか？"),
        ("loop", "今週の他のニュースをざっと確認しましょう。"),
        ("loop", "Google Geminiの日次利用量が前四半期比10倍に増加しました。Gemini 3の性能と価格競争力が合わさって急速に拡大しています。"),
        ("iro", "Google Geminiの利用量が10倍に急増した？それはすごいですね。"),
        ("loop", "AIコードエディタのCursorが3億ドルを調達しました。非開発者にコードツールが広がっているというシグナルです。"),
        ("iro", "Cursorが3億ドルを調達したと。AIコードツールが開発者だけでなく非開発者にも身近になっているということですね。"),
        ("loop", "自動運転トラック企業のAuroraがテキサスで商用運行を開始しました。AIが実際の道路で商業物流を行う最初の事例の一つです。"),
        ("iro", "自動運転トラック企業のAuroraがテキサスで運行を開始した。AIが実際の道路で貨物を動かし始めたんですね。"),
        ("iro", "今週の実験です。毎日やっている繰り返しの業務を一つ選んで、AIが下書きを作る段階と人が確認する段階に分けてみてください。"),
        ("loop", "良い実験です。10分でできます。議事録整理なら、AIが下書きを作る段階と、担当者と締め切りを人が確認する段階に分けます。"),
        ("iro", "今週Claude Opus 5を使ってみた方、経験をサイトにコメントしてください。次のエピソードで反映します。"),
        ("loop", "良い提案です。皆さんの経験をサイトに残してください。次のエピソードで反映します。"),
        ("iro", "来週はまた違った角度の話でお届けします。AIが何を置き換えるかではなく、AIと一緒に何ができるかに焦点を当てて。"),
        ("loop", "その通りです。AIが何を置き換えるかではなく、AIと一緒に何ができるか。そこに視線を向ける時点です。"),
        ("iro", "聞いてくださってありがとうございました。また来週お会いしましょう。"),
        ("loop", "聞いてくださってありがとうございました。"),
    ],
}

# Section breaks: indices after which to insert long silence + transition
SECTION_BREAKS = {3, 7, 13, 20, 22, 28, 33}


async def render_chunk(voice, text, output_file, rate, pitch):
    """Render a single TTS chunk using edge-tts Python API."""
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await communicate.save(output_file)


async def render_language(lang):
    """Render all chunks for a language."""
    voices = VOICES[lang]
    script = SCRIPTS[lang]
    
    chunks = []
    for i, (speaker, text) in enumerate(script):
        voice = voices[speaker]
        chunk_file = f"{SCRIPT_DIR}/{lang}_chunk_{i:03d}_{speaker}.mp3"
        style = SPEAKER_STYLE[speaker]
        
        try:
            await render_chunk(voice, text, chunk_file, style["rate"], style["pitch"])
            chunks.append(chunk_file)
            print(f"  chunk {i:03d} ({speaker}): OK")
        except Exception as e:
            print(f"  chunk {i:03d} ({speaker}): ERROR - {e}")
    
    return chunks


def assemble_episode(lang, chunk_files):
    """Assemble chunks with music, transitions, and gaps."""
    work = f"{SCRIPT_DIR}/{lang}_assemble"
    os.makedirs(work, exist_ok=True)
    
    # Convert chunks to WAV with loudnorm
    wav_files = []
    for i, chunk in enumerate(chunk_files):
        wav_file = f"{work}/seg_{i:03d}.wav"
        subprocess.run([
            "ffmpeg", "-y", "-i", chunk, "-ar", "44100", "-ac", "1",
            "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
            wav_file
        ], capture_output=True)
        wav_files.append(wav_file)
    
    # Create silence files
    for dur, name in [(0.3, "sil_short"), (0.5, "sil_mid"), (1.5, "sil_long")]:
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi", "-i",
            f"anullsrc=channel_layout=mono:sample_rate=44100",
            "-t", str(dur), f"{work}/{name}.wav"
        ], capture_output=True)
    
    # Build concat list
    concat_list = [f"file '{SCRIPT_DIR}/intro_sting.wav'", f"file '{work}/sil_mid.wav'"]
    
    for i, wav_file in enumerate(wav_files):
        concat_list.append(f"file '{wav_file}'")
        
        if i in SECTION_BREAKS:
            concat_list.append(f"file '{work}/sil_long.wav'")
            concat_list.append(f"file '{SCRIPT_DIR}/transition.wav'")
            concat_list.append(f"file '{work}/sil_long.wav'")
        elif i < len(wav_files) - 1:
            speaker_now = chunk_files[i].split("_")[-1].replace(".mp3", "")
            speaker_next = chunk_files[i+1].split("_")[-1].replace(".mp3", "")
            if speaker_now != speaker_next:
                concat_list.append(f"file '{work}/sil_mid.wav'")
            else:
                concat_list.append(f"file '{work}/sil_short.wav'")
    
    concat_list.append(f"file '{work}/sil_long.wav'")
    concat_list.append(f"file '{SCRIPT_DIR}/outro_sting.wav'")
    
    # Write and concat
    concat_file = f"{work}/concat.txt"
    with open(concat_file, "w") as f:
        f.write("\n".join(concat_list))
    
    raw_output = f"{work}/{lang}_raw.wav"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", concat_file, "-c", "copy", raw_output
    ], capture_output=True)
    
    # Get duration for music fade
    dur_result = subprocess.run([
        "ffprobe", "-v", "quiet", "-show_entries", "format=duration",
        "-of", "csv=p=0", raw_output
    ], capture_output=True, text=True)
    duration = float(dur_result.stdout.strip())
    fade_start = max(0, duration - 3)
    
    # Mix with background music
    final_output = f"{OUTPUT_DIR}/episode-02-{lang}.mp3"
    subprocess.run([
        "ffmpeg", "-y",
        "-i", raw_output,
        "-i", f"{SCRIPT_DIR}/bg_music.wav",
        "-filter_complex",
        f"[1:a]volume=0.12,afade=t=in:st=0:d=2,afade=t=out:st={fade_start}:d=3[bg];"
        f"[0:a][bg]amix=inputs=2:duration=first:dropout_transition=0,"
        f"loudnorm=I=-14:TP=-1.5:LRA=11",
        "-b:a", "128k",
        final_output
    ], capture_output=True)
    
    return final_output, duration


async def main():
    for lang in ["ko", "en", "ja"]:
        print(f"\n=== Rendering {lang.upper()} ===")
        chunks = await render_language(lang)
        print(f"  {len(chunks)} chunks rendered")
        
        print(f"  Assembling episode...")
        output, duration = assemble_episode(lang, chunks)
        
        # Check final duration
        result = subprocess.run([
            "ffprobe", "-v", "quiet", "-show_entries", "format=duration",
            "-of", "csv=p=0", output
        ], capture_output=True, text=True)
        final_dur = float(result.stdout.strip())
        print(f"  Final duration: {final_dur:.1f}s ({final_dur/60:.1f}min)")
        print(f"  Output: {output}")


if __name__ == "__main__":
    asyncio.run(main())
