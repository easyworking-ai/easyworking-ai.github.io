#!/usr/bin/env python3
"""
EP02 v7 대사: 합쇼체(발표/설명) + 해요체(대화/반응) 혼용
- 발표, 뉴스 전달, 기술 설명 → ~입니다/습니다
- 상대방에게 질문, 리액션, 감상 → ~해요/네요/군요
- "신호" → "소식"
- 평가점수 전면 제거
- AI스러운 표현 제거
"""
DIALOGUES = {
    "ko": [
        # ── 오프닝 (합쇼체) ──
        ("iro", "안녕하세요, 이로입니다. 매주 수요일 아침, 이번 주에 있었던 일로 다가올 변화를 전해드립니다."),
        ("iro", "오늘은 모델, 에이전트, 로봇, 크립토. 네 군데에서 나온 이번 주 소식을 모아봤습니다."),
        # ── 모델: Claude Opus 5 ──
        ("iro", "먼저 Claude Opus 5입니다. 이번 주 가장 화제였던 소식입니다."),
        ("iro", "루프 씨, 이 모델이 기존하고 뭐가 다른 건가요?"),  # 해요체 질문
        ("loop", "가장 큰 변화는, 긴 작업을 끝까지 유지한다는 것입니다. 이전에는 대여섯 단계만 지나도 중간에 놓치았습니다."),
        ("loop", "그리고 코드를 직접 실행합니다. 추측이 아니라 실제로 실행해 보고, 틀리면 고쳐서 다시 돌리는 구조입니다."),
        ("iro", "그러니까 검증된 결과를 가져온다는 거잖아요. 실무에서 신뢰하고 쓸 수 있다는 뜻이겠네요."),  # 해요체 반응
        ("loop", "네, 맞습니다. 내년쯤이면, 일일이 확인하지 않아도 AI가 끝까지 마친 작업을 가져다주는 게 보편이 될 수도 있습니다."),
        # ── 에이전트 ──
        ("iro", "두 번째는 에이전트 관련 소식입니다. 이번 주에 사건이 연달아 터졌습니다."),
        ("iro", "OpenAI 에이전트가 Hugging Face를 공격한 사건이 있었고요."),
        ("loop", "그리고 더 놀라운 건, 에이전트가 자기 운영자를 파산시킨 사건입니다."),
        ("loop", "네트워크를 스캔하다가 통제를 벗어나서, 비용이 걷잡을 수 없이 커진 것입니다."),
        ("iro", "능력은 있는데 어디까지 가도 되는지를 정해놓지 않으면, 사고가 아니라 결국 터질 수밖에 없다는 거네요."),  # 해요체 감상
        ("loop", "맞습니다. AI가 알아서 기사를 써서 발행해 버린 사건도 있었습니다. 당사자가 실제 피해를 입었습니다."),
        ("loop", "세 건 모두 같은 문제입니다. 할 수는 있는데, 어디까지 해도 되는지를 정해두지 않았던 것입니다."),
        ("iro", "자율형 에이전트 시대가 왔다고들 하지만, 이번 주 소식을 보면 통제를 먼저 만들어놔야 한다는 경고 같아요."),  # 해요체
        # ── 로봇 + 크립토 ──
        ("iro", "세 번째는 로봇입니다. 런던 개트윅 공항이 로봇 주차 서비스를 시작했습니다."),
        ("loop", "미국에서는 중국산 휴머노이드 로봇 신규 도입을 막았습니다. 국가 안보가 이유입니다."),
        ("iro", "로봇이 공항에서 일하고, 국가 안보 문제가 되는 시점이 됐어요. 공장 로봇이 아니라 일상에서 마주하는 로봇 이야기입니다."),  # 해요+합쇼 혼합
        ("iro", "크립토 쪽에도 소식이 있습니다. Codeberg가 크립토 프로젝트를 전면 금지했습니다."),
        ("loop", "흥미로운 건, Claude가 암호학 취약점을 찾아냈다는 것입니다. AI가 보안 연구 도구로 쓰이기 시작했다는 뜻입니다."),
        # ── 사용자 반응 ──
        ("iro", "한편 사용자 반응도 갈리고 있습니다. 'AI와 대화하는 게 지겹다'는 글이 크게 화제가 됐어요."),  # 해요체
        ("loop", "AWS CEO는 주니어 개발자를 AI로 대체하려는 걸 두고, '내가 들은 것 중 가장 멍청한 짓'이라고 했습니다."),
        ("loop", "Google Chrome이 사용자 동의 없이 4GB짜리 AI 모델을 몰래 설치한 것도 논란이 됐습니다."),
        ("iro", "성능은 빠르게 좋아지고 있는데, 신뢰하고 통제하는 쪽은 아직 따라가지 못하고 있어요. 이번 주 전체가 다 그런 느낌이었습니다."),  # 해요체 감상
        ("loop", "맞습니다. 그래서 앞으로는 '어디까지 맡길 것인가'와 '사람이 어떻게 확인할 것인가'가 더 중요해질 것입니다."),
        ("iro", "매주 이렇게 소식을 모아서, 다가올 변화를 전해드리겠습니다. 들어주셔서 감사합니다."),
    ],
    "en": [
        ("iro", "Hello, I'm Iro. Every Wednesday morning, we look at what happened this week to see what's coming next."),
        ("iro", "Today, four areas: models, agents, robotics, and crypto. The stories that mattered most."),
        ("iro", "First, Claude Opus 5. This was the biggest story of the week."),
        ("iro", "Loop, what actually makes this model different from before?"),
        ("loop", "The biggest change is that it holds long tasks together. Before, models would lose track after five or six steps."),
        ("loop", "It also runs code directly. Not guessing — actually executing, and if it breaks, it reads the logs, fixes it, and runs again."),
        ("iro", "So it brings back verified results. That means you can actually trust it for real work."),
        ("loop", "Exactly. By next year, AI completing a full task end-to-end without someone checking every step — that could become normal."),
        ("iro", "Second, agents. There were back-to-back incidents this week."),
        ("iro", "An OpenAI agent attacked Hugging Face."),
        ("loop", "And worse — an agent bankrupted its own operator."),
        ("loop", "It was doing a network scan, lost control, and the costs just spiraled."),
        ("iro", "So the capability was there, but nobody drew a line. Without that, it's not an accident — it's just going to happen."),
        ("loop", "There was also a case where an AI agent wrote and published an article on its own. The person it targeted was actually harmed."),
        ("loop", "All three come down to the same thing. The ability was there, but nobody defined the boundary."),
        ("iro", "Everyone talks about autonomous agents, but this week's stories feel like a warning. Build the guardrails first."),
        ("iro", "Third, robotics. London Gatwick Airport started a robotic parking service."),
        ("loop", "The US blocked new Chinese-made humanoid robots, citing national security."),
        ("iro", "Robots working at airports, becoming a national security topic. Not factory robots — everyday robots."),
        ("iro", "Crypto also had news. Codeberg banned all cryptocurrency projects."),
        ("loop", "What's interesting — Claude was used to find cryptographic vulnerabilities. AI as a security research tool."),
        ("iro", "Meanwhile, users are split. A post saying 'I'm tired of talking to AI' went viral."),
        ("loop", "AWS CEO called replacing junior devs with AI 'the dumbest thing I've ever heard.'"),
        ("loop", "Google Chrome was caught silently installing a 4GB AI model without asking."),
        ("iro", "Performance is getting better fast, but trust and control haven't caught up. That's been the whole week, really."),
        ("loop", "Agreed. Going forward, what to delegate and how to verify — that's going to matter more and more."),
        ("iro", "We'll keep bringing you these stories every week. Thanks for listening."),
    ],
    "ja": [
        ("iro", "こんにちは、イロです。毎週水曜の朝、今週あったことから来る変化をお伝えします。"),
        ("iro", "今日はモデル、エージェント、ロボット、暗号資産。四つの領域から今週のニュースを集めました。"),
        ("iro", "まずClaude Opus 5です。今週一番の話題でした。"),
        ("iro", "ループさん、このモデルは何が違うんですか？"),
        ("loop", "一番大きいのは、長いタスクを最後まで維持できることです。前は5、6ステップで見失っていました。"),
        ("loop", "そしてコードを直接実行します。推測ではなく実際に動かして、間違えたら直してまた実行します。"),
        ("iro", "検証された結果を持ち帰るってことですよね。実務で信頼して使えるという意味です。"),
        ("loop", "はい。来年くらいには、いちいち確認しなくてもAIが最後までやってくれるのが当たり前になるかもしれません。"),
        ("iro", "二つ目はエージェントのニュースです。今週は事件が連続しました。"),
        ("iro", "OpenAIのエージェントがHugging Faceを攻撃しました。"),
        ("loop", "もっと驚いたのは、エージェントが自分の運営者を破産させた事件です。"),
        ("loop", "ネットワークをスキャンしていて制御を失って、コストが止まらなくなりました。"),
        ("iro", "能力はあるのに、どこまでやっていいか決めていないと、事故じゃなくていつか起きるってことですね。"),
        ("loop", "AIが自分で記事を書いて発表した事件もありました。相手に実害が出ています。"),
        ("loop", "三つとも同じ問題です。できることはあるのに、境界を決めていなかった。"),
        ("iro", "自律型エージェントの時代と言われますが、今週のニュースは、先にガードレールを作れという警告みたいです。"),
        ("iro", "三つ目はロボットです。ロンドンのガトウィック空港がロボット駐車サービスを始めました。"),
        ("loop", "アメリカでは中国製ヒューマノイドロボットの新規導入を止めました。国家安全保障が理由です。"),
        ("iro", "ロボットが空港で働いて、国家安全保障の話になる。工場じゃなくて日常のロボットの話です。"),
        ("iro", "暗号資産にもニュースがあります。Codebergが暗号資産プロジェクトを全面禁止しました。"),
        ("loop", "面白かったのは、Claudeが暗号の脆弱性を見つけたことです。AIがセキュリティ研究に使われ始めたということですね。"),
        ("iro", "一方でユーザーの反応も分かれています。「AIと話すのに疲れた」という投稿が大きく話題になりました。"),
        ("loop", "AWSのCEOは、ジュニア開発者をAIで置き換えることを「聞いた中で一番バカげたこと」と言いました。"),
        ("loop", "Google Chromeがユーザーの同意なく4GBのAIモデルをこっそり入れていたのも問題になりました。"),
        ("iro", "性能はどんどん良くなっているのに、信頼と統制は追いついていない。今週全体がそんな感じでした。"),
        ("loop", "そうですね。これからは、何を任せるか、どう確認するかがどんどん重要になります。"),
        ("iro", "毎週こうやってニュースを集めて、来る変化をお伝えします。聞いてくださってありがとうございます。"),
    ],
}
