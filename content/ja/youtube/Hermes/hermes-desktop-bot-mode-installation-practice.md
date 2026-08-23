---
title: "Hermes DesktopとBot Modeのインストール・実習ノート"
description: "Hermes DesktopのインストールからBot ModeのProfile、グループチャット、Routinesまで、実行済みの内容と計画を分けて記録する実習ノートです。"
created: 2026-08-22
updated: 2026-08-22
cssclass: blog-post
publish: true
lang: ja
section: YOUTUBE
source_checked: 2026-08-22
official_site_version_observed: v0.20.5
runtime_status: "未実行"
tags:
  - hermes
  - hermes-desktop
  - bot-mode
  - agent
  - youtube
  - 実習ノート
sources:
  - https://hermes-agent.nousresearch.com/docs/getting-started/quickstart
  - https://hermes-agent.nousresearch.com/docs/getting-started/installation
  - https://hermes-agent.nousresearch.com/docs/user-guide/desktop
  - https://hermes-agent.nousresearch.com/docs/user-guide/profiles
  - https://hermes-agent.nousresearch.com/docs/user-guide/features/cron
  - https://hermes-agent.nousresearch.com/docs/user-guide/security
---

# Hermes DesktopとBot Modeのインストール・実習ノート

## 0. まとめ

| 項目 | 一言でいうと | インストール・実行のポイント |
| --- | --- | --- |
| Hermes Desktop | ターミナル版と同じHermesエージェントをウィンドウで使うネイティブアプリ | 公式サイトのDesktopインストーラーを実行するか、CLIのインストール後に `hermes desktop` を実行します |
| Bot Mode | 一つのHermes Profileを名前付きのボットとして表示するDesktop機能 | 現在のDesktopに含まれています。古いプラグインを別途クローンせず、`Settings → Plugins`で確認します |
| Profile | 設定、認証、memory、session、skills、予約タスクを分けたHermesのインスタンス | Bot Modeの`New Agent`、または `hermes profile create <name>` で作成します |
| Routines | ボットに紐づく繰り返し作業。内部ではHermes Cronを使います | 基本実習が通った後、外部送信なしのローカルテストだけで確認します |
| よくある誤解 | Profileを作っただけでファイルアクセスが隔離されるわけではありません | 標準の`local`ターミナルは現在のOSユーザー権限で動きます。Profileは状態を分けますが、セキュリティサンドボックスではありません |

### Bot Modeは別にインストールしません

現在のBot ModeはDesktopに含まれています。古い[Hermes-Bot-Modeリポジトリ](https://github.com/NousResearch/Hermes-Bot-Mode)を通常のインストール手順としてクローンしないでください。Desktopをインストールした後、`Settings → Plugins`を確認します。

## 1. 実習前の注意

現在のYouTubeコンテンツパッケージと、実習に必要な抜粋だけを読みます。チャンネルアカウントや非公開資料にはアクセスせず、アップロード、メッセージ送信、ファイルの作成・変更・削除も行いません。APIキーをノートやキャプチャに残さないでください。

## 2. インストール前の準備

### 2.1 対応範囲

公式サイトのDesktopダウンロードは次の環境に対応しています。

- macOS 12+
- Windows 10/11
- Linux：公式のターミナルインストール後に `hermes desktop` を実行

公式のインストール文書では、macOSとWindowsはDesktopインストーラーを使う方法が案内されています。Linux、macOS、WSL2にはインストールスクリプトの経路があり、ネイティブWindowsにはPowerShellスクリプトの経路があります。

### 2.2 インストール経路を選ぶ

| OS | 推奨経路 | 実行すること |
| --- | --- | --- |
| macOS | 公式Desktopインストーラー | [公式サイト](https://hermes-agent.nousresearch.com/)から**Download desktop app**を取得して実行します |
| Windows | 公式Desktopインストーラー | 公式サイトからWindows用インストーラーを取得して実行します |
| Linux | ターミナルインストール後にDesktopを起動 | 公式スクリプトを実行し、シェルを再読み込みして `hermes desktop` を実行します |
| CLIがすでにある場合 | 既存のインストールを再利用 | `hermes desktop` を実行します |

公式のインストール資料によれば、インストーラーはPython 3.11、Node.js 22、`ripgrep`、`ffmpeg`、仮想環境、`hermes`コマンドの設定を処理できます。最初にすべてを手動で入れることが標準要件ではありません。

### 2.3 Linuxまたはターミナルインストール前の確認

```bash
git --version
curl --version
```

Linuxでコマンドが不足している場合は、ディストリビューションのパッケージマネージャーで`curl`と`xz-utils`を準備します。ネイティブモジュールのコンパイルが必要なら`build-essential`も準備します。Debian/Ubuntuの例です。

```bash
sudo apt install curl xz-utils build-essential
```

WindowsのDesktopインストーラーを使う場合は、この手順を省略します。

## 3. Hermesをインストールする

### 3.1 macOS・Windows：Desktopインストーラー

1. [Hermes Agent公式サイト](https://hermes-agent.nousresearch.com/)を開きます。
2. OSに合う**Download desktop app**を選びます。
3. インストーラーを実行します。
4. 初回起動でローカルHermesをインストールするか、起動中のHermesに接続します。
5. 新しいターミナルを開き、下記の確認を行います。

Windowsでは、インストール前のPowerShellが古いPATHを保持している場合があります。古いウィンドウを閉じ、新しいPowerShellで`Get-Command hermes`を再実行します。

### 3.2 Linux・macOS・WSL2：ターミナルからインストールしてDesktopを起動

組織のセキュリティポリシーでリモートスクリプトの直接実行が禁止されている場合は、公式URLからスクリプトを保存して確認してから実行します。非公式ミラーや任意のインストーラーは使いません。

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

シェルを再読み込みます。

```bash
source ~/.bashrc   # bash
# または
source ~/.zshrc    # zsh
```

その後、Desktopを起動します。

```bash
hermes desktop
```

`hermes desktop`は、現在のHermesインストールの設定、キー、session、skillsを再利用します。初回起動時にDesktopアプリがローカルのHermesランタイムを準備する場合があります。

### 3.3 ネイティブWindowsのCLI専用経路

PowerShellでCLIだけを先にインストールする場合は、次を実行します。

```powershell
iex (irm https://hermes-agent.nousresearch.com/install.ps1)
```

新しいPowerShellを開き、Desktopを起動します。

```powershell
hermes desktop
```

### 3.4 インストール直後の静的確認

まだモデルを接続していなくても、次のコマンドでインストール状態を確認できます。

```bash
hermes --version
hermes doctor
hermes status
```

PowerShellでもコマンド名は同じです。

| 確認項目 | 実際の記録 |
| --- | --- |
| OS・バージョン | `[実行後に記録]` |
| インストール経路 | `Desktop installer / install.sh / install.ps1 / 既存CLI` |
| `hermes --version` | `[実行後に記録]` |
| `hermes doctor`の概要 | `[実行後に記録]` |
| `hermes status`の概要 | `[実行後に記録]` |
| エラーまたは警告 | `[なし / 内容]` |

## 4. Providerとモデルの設定

Desktop初回起動のオンボーディング、または`Settings → Providers`と`Settings → Model`でProviderとモデルを設定します。Hermesをインストールしただけでは、Provider認証が終わるまで実際の会話は完了しません。

### 選択肢A：Nous Portalを使う

公式文書が案内する短い経路は次のとおりです。

```bash
hermes setup --portal
```

このコマンドはOAuthログインを開始し、Nousを推論Providerとして設定し、Tool Gatewayを有効にします。Portalを使わない場合は無理に実行せず、選択肢Bを使います。

### 選択肢B：別のProviderまたは直接APIキーを使う

```bash
hermes model
```

または、設定ウィザード全体を実行します。

```bash
hermes setup
```

Desktopでは`Settings → Providers`と`Settings → Model`から同じ設定を行えます。APIキーを画面やノートにコピーしないでください。

### Providerを確認する

ツールも外部資料も必要ない、一文だけのテストを行います。

```text
次の文を正確に一行で答えてください：インストール確認完了
```

- [ ] Providerの認証エラーなしに応答が返った。
- [ ] タイムアウトやモデル名のエラーがなかった。
- [ ] 応答全文または画面キャプチャを実習記録に残した。
- [ ] この基本テストが終わる前にBot Mode、Cron、Messagingを追加していない。

公式Quickstartも、最初に通常のチャットを完了してからgateway、cron、skills、voice、routingを追加する順序を案内しています。基本会話が失敗している状態で、先にBot Modeを調べないでください。

## 5. Desktopの基本利用を確認する

### 入力 → 操作 → 結果

| 段階 | やること | 残す結果 |
| --- | --- | --- |
| 入力 | `インストール確認完了`を一行で返すよう依頼 | 送信したテスト文 |
| 操作 | Desktopのチャット欄から送り、応答が終わるまで待つ | 完了時刻またはキャプチャ |
| 結果 | 一回の応答が完了したことを確認 | `基本チャット通過 / 失敗原因` |
| 復旧 | Providerとモデルを先に確認し、必要なら`hermes doctor`を再実行 | 復旧前後の記録 |

DesktopはCLIとは別のエージェントではありません。公式文書によれば、Desktop、`hermes` CLI/TUI、Web Dashboardは同じAgentの設定、キー、session、skills、memoryを共有します。ここで始めたsessionをCLIから続けて確認できます。

```bash
hermes desktop
```

すでにアプリが開いている場合は、もう一度起動する必要はありません。

## 6. Bot Mode実習：二つのProfileをボットにする

### 6.1 ボットとProfileの関係

この実習では`content-planner`と`script-editor`を別々の名前付きボットとして扱います。実体は、それぞれ独立したHermes Profileです。各Profileは独自の`config.yaml`、`.env`、`SOUL.md`、memory、session、skills、cron、gateway状態を持ちます。

次の原則を守ります。

- 同じProfileのホームを二つのプロセスが同時に使わない。
- 同じProviderを使っても、Profileの状態とsessionは混ざらない。
- Profile名を変更するときは、既存のsessionと予約タスクとの関係も確認する。
- Profileの分離はセキュリティサンドボックスではない。実際のファイルを扱う仕事には、別のsandboxまたは制限した作業フォルダーを設計する。

### 6.2 Bot Modeを有効にする

1. Hermes Desktopを開きます。
2. 左サイドバーの`Sessions | Bots`タブを探します。
3. `Bots`が見えない場合は`Settings → Plugins`を開きます。
4. Bot Modeを有効にし、Desktopを再起動するかプラグインをreloadします。
5. ボット一覧に標準Profileが一つ表示されることを確認します。

現在のDesktop文書では、Bot Modeに次の機能があります。

- ボットごとのavatarと一つのcanonical Bot Chat
- `New Agent`による新しいProfileの作成
- ボットごとのmodel、SOUL、skills、toolsets、MCP設定を開くAdvanced領域
- グループ分類とグループチャット
- ボットごとのRoutinesタイル
- `@ボット名`による引き継ぎと、`@user`による人への判断依頼

### 6.3 一つ目のボットを作る

次の値を使います。

| フィールド | 値 |
| --- | --- |
| Name | `content-planner` |
| Title | `コンテンツ企画担当` |
| Description | `現在のWorking AI YouTube資料から、対象、約束、デモ、根拠、禁止事項を抽出し、制作briefに整理する。` |

Botsタブで`New Agent`を選び、値を入力します。最初の実習ではAdvancedを初期値のままにし、保存後にボット一覧とBot Chatを確認します。

- [ ] `content-planner`の行が見える。
- [ ] タイトルと説明が入力値と一致する。
- [ ] ボットをクリックすると標準Profileと区別されたBot Chatが開く。
- [ ] Profileの設定を変更した場合、新しいチャットで確認できる。

### 6.4 二つ目のボットを作る

| フィールド | 値 |
| --- | --- |
| Name | `script-editor` |
| Title | `台本編集担当` |
| Description | `content-plannerが確認した内容だけを使い、Working AIのフック、シーン構成、CTA案を作り、未確認の内容を表示する。` |

同じく`New Agent → 保存 → 一覧確認 → Bot Chatを開く`の順で進めます。

### 6.5 UIが動かない場合のCLI経路

```bash
hermes profile create content-planner \
  --description "現在のWorking AI YouTube資料から、対象、約束、デモ、根拠、禁止事項を抽出し、制作briefに整理する。"

hermes profile create script-editor \
  --description "content-plannerが確認した内容だけを使い、Working AIのフック、シーン構成、CTA案を作り、未確認の内容を表示する。"

hermes profile list
```

Profileを作った後、Desktopを更新してBotsタブを再確認します。新しいProfileで会話するには、ProfileごとにProviderとモデルの設定が必要になる場合があります。

## 7. Bot Mode実習：YouTubeコンテンツを共同制作する

### 7.1 実習ケース

新しい告知文を要約する代わりに、現在の**AI Gap YouTubeコンテンツパッケージ**を制作成果物へ発展させます。パッケージには、リサーチ、シリーズ設計、EP1台本、撮影キューシート、編集ガイド、マーケティング計画、ソースチェックリストが含まれます。

```text
[現在のコンテンツ]
チャンネル：Working AI
シリーズ：AI格差の時代
対象エピソード：EP1「AIに仕事を頼んだら、退勤が早くなりました」
対象：現場のIT企画担当、PM、AI導入に関心のある実務者
約束：AIを導入したものの使い方が分からない人に向けて、
      3人のエージェント（dev、reviewer、orchestrator）がbrief → 実行 → 検証する流れを画面で見せる。

[読む資料と制作ルール]
1. 指定した現在のコンテンツパッケージだけをsource of truthとして使う。
2. 確定内容、制作計画、ランタイム未確認を分ける。
3. 統計、出典、実行結果の状態を保ち、未確認は[確認が必要]または[ランタイム未実行]と表示する。
4. 外部検索、チャンネルへのアップロード、外部メッセージ、ファイル操作はしない。
5. 台本案ができても、撮影・編集・アップロード完了とはみなさない。
```

### 7.2 グループを作る

`content-planner`と`script-editor`を`YouTubeコンテンツ制作`というグループに移動し、グループチャットを開きます。グループチャットは通常の個人sessionとは別の行として表示され、複数のボットが順番に応答できます。

### 7.3 グループに送るプロンプト

```text
現在のWorking AI YouTubeコンテンツパッケージだけを使って、EP1の制作協業をしてください。
外部検索、チャンネルへのアップロード、ファイル操作、メッセージ送信はしないでください。

[読む資料]
- パッケージREADME
- チャンネル・市場リサーチ
- シリーズ・アングル
- EP1台本
- ソースチェックリスト

@content-planner まず、次を抽出してください。
1. チャンネル、シリーズ、EP1の対象と視聴者への約束
2. 核となるメッセージとデモの流れ
3. 画面で証明できる根拠と、準備・確認が必要な項目
4. 撮影できる1ページのコンテンツbrief
確定内容、計画、[ランタイム未実行]を分けてください。

@script-editor content-plannerのbriefと上記資料だけを使い、次を作成してください。
1. Working AIの30〜45秒フック
2. 6シーン構成：フック → 問題定義 → エージェント紹介 → brief入力 → 実行・検証 → 限界・CTA
3. 各シーンの画面上の根拠とナレーションの要点
4. 最後に[確認が必要]、[ランタイム未実行]、人が承認する項目
新しい統計、成果、実行結果を作らないでください。
```

### 7.4 期待する結果の形

正確な文言はモデルによって変わります。次の構造と状態の分離を確認します。

```text
[コンテンツbrief]
- チャンネル、シリーズ、EP：...
- 対象・視聴者への約束：...
- 核となるメッセージ：...
- デモの流れ：...
- 画面上の根拠・出典：...
- 状態：確定 / 制作計画 / [ランタイム未実行]

[撮影案]
- フック：...
- シーン1〜6：...
- CTA：...

[確認が必要・人の承認]
- なし、または項目一覧
```

企画担当が対象、メッセージ、デモ、根拠を分けていること、編集担当が指定資料だけを使っていること、ランタイム未確認が残っていることを確認します。二つのBot Chatとグループ行が表示され、外部検索、ファイル書き込み、チャンネルアップロード、メッセージ送信が起きていないことも確認します。

### 7.5 Bot Modeの結果を記録する

| 確認項目 | 実際の結果 |
| --- | --- |
| `content-planner` Bot Chat | `[実行後に記録]` |
| `script-editor` Bot Chat | `[実行後に記録]` |
| `YouTubeコンテンツ制作`グループ | `[表示 / 非表示]` |
| brief → 台本の応答順 | `[実行後に記録]` |
| `@user`による判断依頼 | `[あり / なし]` |
| ランタイム未確認の表示 | `[あり / なし]` |
| 外部副作用 | `[なし / 内容]` |
| キャプチャ・転記の場所 | `[記録]` |

## 8. 任意課題：Routinesでローカル予約テスト

手動のグループチャット確認が終わってから行います。

### 8.1 Routinesの意味

Bot ModeのRoutinesは単なるメモではなく、Hermes Cronとして登録される予約タスクです。Cronは新しいAgent sessionで実行されるため、現在のチャットの文脈がそのまま引き継がれるとは考えません。

最初のテストでは次を守ります。

- 結果はlocalだけにする。
- Telegram、Discord、Slack、Email、`all`の送信を選ばない。
- テスト直後にpauseまたはremoveする。
- Provider呼び出しと費用が発生する可能性があるため、実行回数を確認する。

### 8.2 Desktopで作成する

1. Botsタブで`content-planner`を選びます。
2. ボットの`Routines`タイルを開きます。
3. タスク名を`bot-mode-local-smoke`にします。
4. 次のプロンプトを入力します。

```text
現在時刻と「YouTubeコンテンツ制作予約テスト」という文言だけをローカル結果として記録してください。
外部メッセージの送信、ファイルの削除・作成、Web検索はしないでください。
```

5. 一回限り、または短いテスト時間を選びます。
6. Deliveryがある場合は`local`を選びます。
7. 保存し、`hermes cron list`またはRoutines一覧で確認します。

### 8.3 CLIで確認して削除する

```bash
hermes cron create "10m" \
  "現在時刻と『YouTubeコンテンツ制作予約テスト』だけをローカル結果として記録し、外部送信はしないでください。" \
  --name "bot-mode-local-smoke"

hermes cron list
hermes cron status
```

IDを確認したら、最近の実行履歴を見ます。

```bash
hermes cron runs <job_id> --limit 5
```

テスト終了後は必ず停止または削除します。

```bash
hermes cron pause <job_id>
hermes cron remove <job_id>
```

実行されない場合は`hermes gateway status`、`hermes cron status`、`hermes cron list`の順で確認します。Gateway schedulerの状態を理解する前に、予約タスクを追加しないでください。

## 9. ローカルとリモートの実行境界

標準のDesktopはローカルbackendを管理します。別のマシンの`hermes serve`へ接続するRemote gatewayもありますが、最初の実習では使いません。

Remoteへ切り替える場合は次を記録します。

- Desktopを表示するコンピューターと、Agentがツールを実行するコンピューターが異なる場合があります。
- ターミナル、ファイル操作、AgentツールはリモートのHermesホストで動きます。
- `Settings → Gateways`でRemote URLと認証を設定します。
- Basic Auth backendを公開インターネットにそのまま出さないでください。公式文書は、信頼ネットワークやVPNではBasic Auth、公開アクセスではOAuthを推奨しています。

Remoteを使った場合は、画面のコンピューター、Agent実行ホスト、認証方式を別々に記録します。

## 10. トラブルシューティング

| 症状 | 最初にすること | 停止・復旧の基準 |
| --- | --- | --- |
| `hermes: command not found` | 新しいシェルを開くか、`.zshrc`/`.bashrc`を再読み込みします。Windowsは新しいPowerShellを開きます | PATHを何度も変更せず、インストール場所と`hermes doctor`を記録します |
| Desktopは開くが応答しない | `Settings → Providers`または`hermes model`でProviderとモデルを確認します | APIキーは記録せず、認証エラーの文言だけを残します |
| `hermes doctor`に依存関係エラーがある | インストール経路とエラーを保存し、`hermes update`を検討します | 複数のPython・Nodeを手動で混ぜません |
| Botsタブがない | Desktopを更新し、`Settings → Plugins`でBot Modeを確認します | 先に古いBot Modeリポジトリをクローンしません |
| 作成したボットが一覧にない | Desktopをreload/restartし、`hermes profile list`を実行します | 名前の重複とProvider設定を記録します |
| グループチャットが静か | 二つのProfileがグループに入っているか、正確な`@ボット名`か、各ProfileにProviderがあるか確認します | 同じプロンプトを繰り返し送らず、一度停止して状態を記録します |
| ボットがファイル作成や外部操作を提案する | すぐに停止して承認しません。`--yolo`を切り、読み取り専用の抜粋でやり直します | Profileの分離だけで安全とは判断しません |
| Routineが実行されない | `hermes gateway status` → `hermes cron status` → `hermes cron list` → `hermes cron runs <job_id>`を順に確認します | 別のタスクを作る前にpause/removeします |
| Remoteでファイル場所が違う | 接続中のGatewayと実行ホストを確認します | 非公開ファイルをアップロードせず、ローカル実習に戻します |

### 古いBot Mode手動プラグインについて

古いREADMEには、次の手動インストールが記載されていました。

```text
git clone https://github.com/NousResearch/Hermes-Bot-Mode ~/.hermes/desktop-plugins/hermes-bots
```

現在のDesktopの推奨インストール手順として、このコマンドを使わないでください。古いビルドや開発環境を再現する場合だけ、履歴として参照します。確認が必要な場合も、プラグインはGatewayではなくDesktopアプリを実行するコンピューターに置くことを記録します。

## 11. 実行記録カード

実習後に空欄を埋めます。キー、トークン、非公開資料は記録しません。

```yaml
実行日時: "YYYY-MM-DD HH:MM KST"
OS: ""
インストール経路: "Desktop installer | install.sh | install.ps1 | 既存CLI"
hermes_version: ""
doctor_result: ""
provider: "名前だけ記録"
model: "モデル名だけ記録"
desktop_smoke_test: "通過 | 失敗 | 未実行"
bot_mode: "内蔵確認 | 未確認"
profiles:
  - name: content-planner
    result: ""
  - name: script-editor
    result: ""
group_chat: "通過 | 失敗 | 未実行"
routine: "未使用 | localテスト後に削除 | 確認が必要"
evidence: "キャプチャまたは転記の場所"
external_side_effect: "なし | 内容"
known_gap: ""
next_safe_action: ""
```

### 成果物の分け方

入力、出力、証拠を分けます。

- 入力：現在のAI Gap YouTubeパッケージとプロンプト
- 出力：グループチャットのコンテンツbriefと撮影案
- 証拠：`hermes --version`、`hermes doctor`、Bot Mode一覧、グループチャット画面
- 未実行：Provider、Desktop、Bot Mode、実際の撮影・アップロードのうち、まだ確認していないもの

## 12. 停止基準と次のセッションへの引き継ぎ

基本チャットが成功し、Bot Modeの二つのProfileが表示されたら、1回目の実習は十分です。グループチャットが成功しても、Routines、Messaging、Remoteを一度に追加しません。外部送信、チャンネルアップロード、非公開資料が必要になった時点で、このノートの安全範囲を超えます。

次のセッションには次の文を使います。

```text
Hermes Desktopと基本チャットは[通過/失敗/未実行]です。
確認したバージョンは[バージョン]で、Provider・モデルは[名前]です。
Bot Modeは[内蔵確認/未確認]で、content-plannerとscript-editorは[状態]です。
YouTubeコンテンツ制作グループチャットは[通過/失敗/未実行]で、外部副作用は[なし/内容]です。
次の安全な作業は[グループ結果の確認/出典・画面の確認/local Routineの確認/トラブルシューティング]です。
```

## ケースの参考範囲

この実習では、現在のAI Gap YouTubeコンテンツパッケージの範囲、リサーチ、シリーズ設計、EP1台本、ソースチェックリストを使います。実際の撮影、アップロード、ランタイム実行が完了したことを意味しません。

## 参考資料

以下は2026-08-22に確認したNous Research公式資料です。

1. [Hermes Agent公式サイト](https://hermes-agent.nousresearch.com/) — Desktopのダウンロード、対応OS、サイト上の表示バージョン
2. [Quickstart](https://hermes-agent.nousresearch.com/docs/getting-started/quickstart) — Provider選択、最初の会話の確認、機能を追加する順序
3. [Installation](https://hermes-agent.nousresearch.com/docs/getting-started/installation) — macOS、Windows、Linux、WSL2のインストール経路と依存関係
4. [Desktop App](https://hermes-agent.nousresearch.com/docs/user-guide/desktop) — CLIとの状態共有、内蔵Bot Mode、Routines、Remote Gateway
5. [Profiles](https://hermes-agent.nousresearch.com/docs/user-guide/profiles) — Profileごとの状態分離、作成方法、セキュリティ上の限界
6. [Scheduled Tasks (Cron)](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron) — 予約、実行、確認、停止、削除
7. [Security](https://hermes-agent.nousresearch.com/docs/user-guide/security) — 承認、YOLOの警告、Gateway認証、Profileとsandboxの違い
8. [Hermes Agent公式リポジトリ](https://github.com/NousResearch/hermes-agent) — 現在のソースと公式文書
9. [Hermes Bot Modeアーカイブ](https://github.com/NousResearch/Hermes-Bot-Mode) — 旧プラグインの記録とDesktop内蔵への移行
