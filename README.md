# PC Support Agent

Windows PC のネットワークトラブルを自動調査する AI エージェントです。

ユーザーから「インターネットにつながらない」などの問い合わせを受けると、
LLM が状況に応じて必要なネットワークコマンドを選択・実行し、
その結果をもとに原因候補や対処方法を提示します。

## 概要

OpenAI Responses API の Function Calling / Tool Calling を利用しています。

LLM が単純に回答を生成するだけではなく、調査に必要な Tool を自律的に選択します。

現在は以下の Windows コマンドに対応しています。

- `ipconfig`
- `ping`
- `nslookup`

Tool の実行結果を LLM に返却し、さらに調査が必要であれば次の Tool を実行する
Agent Loop を実装しています。

## 主な機能

- PC の IP アドレス・ネットワーク情報の取得
- デフォルトゲートウェイへの疎通確認
- インターネット上のホストへの疎通確認
- DNS 名前解決の確認
- LLM による Tool の自律選択
- 複数 Tool の連続実行
- Tool の実行結果を利用した追加調査
- 原因候補・確認結果・対処方法の生成
- Tool 実行時の例外処理
- コマンドのタイムアウト制御
- Agent Loop の最大実行回数による無限ループ防止

## Agent Loop

本アプリでは、LLM が一度だけ回答するのではなく、
Tool の実行結果をもとに次の行動を判断する Agent Loop を実装しています。

```text
ユーザー
「インターネットにつながらない」
        ↓
       LLM
        ↓
 Tool Call が必要？
    ↓ Yes      ↓ No
 Toolを実行    最終回答
    ↓
 実行結果をLLMへ返却
    ↓
       LLM
    ↓
 次の調査が必要？
```

例えば、以下のような調査を自律的に行います。

```text
ipconfig
   ↓
ping 192.168.x.x
   ↓
ping 8.8.8.8
   ↓
nslookup www.google.com
   ↓
必要に応じて追加調査
   ↓
原因候補・確認結果・対処方法を回答
```

実際に使用する Tool や実行順序は固定しておらず、
LLM がそれまでの調査結果をもとに判断します。

## Tool

### ipconfig

Windows の `ipconfig` コマンドを実行し、PC のネットワーク情報を取得します。

主に以下の確認に使用します。

- IPv4 / IPv6 アドレス
- サブネットマスク
- デフォルトゲートウェイ
- ネットワークアダプターの状態

### ping

Windows の `ping` コマンドを実行し、指定したホストへの疎通を確認します。

例えば以下のような調査に利用します。

```text
ping 192.168.1.1
ping 8.8.8.8
ping www.google.com
```

### nslookup

Windows の `nslookup` コマンドを実行し、DNS の名前解決を確認します。

```text
nslookup www.google.com
```

IP アドレスへの通信は成功しているにもかかわらず Web サイトへ接続できない場合などに、
DNS が正常に動作しているかを調査できます。

## 使用技術

- Python
- OpenAI Responses API
- Function Calling / Tool Calling
- Python `subprocess`
- python-dotenv
- Windows ネットワークコマンド

## セットアップ

### 1. リポジトリをクローン

```bash
git clone <repository-url>
cd pc-support-agent
```

### 2. 仮想環境を作成

```bash
py -m venv .venv
```

### 3. 仮想環境を有効化

PowerShell の場合：

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. 必要なライブラリをインストール

```bash
pip install openai python-dotenv
```

### 5. OpenAI API Key を設定

プロジェクト直下に `.env` を作成します。

```env
OPENAI_API_KEY=your_api_key
```

`.env` は Git の管理対象に含めないでください。

```gitignore
.env
.venv/
```

## 実行方法

`src` ディレクトリへ移動して実行します。

```powershell
cd src
py .\main.py
```

現在の v1 では、以下のような問い合わせをプログラムから LLM に渡して動作させています。

```text
インターネットがつながりません。原因を調べてください。
```

## 実行例

```text
Agent Loop開始： 1
呼び出されたTool： ipconfig

Agent Loop開始： 2
呼び出されたTool： ping
呼び出されたTool： ping
呼び出されたTool： nslookup

Agent Loop開始： 3
呼び出されたTool： ping

Agent Loop開始： 4

調査結果：
PCからインターネットへの疎通は正常です。

確認結果：
- Wi-Fi 接続：正常
- デフォルトゲートウェイへの疎通：正常
- インターネットへの疎通：正常
- DNS 名前解決：正常

原因として、ブラウザ・VPN・プロキシなどの
ネットワーク以外の問題が考えられます。
```

※ 実際の Tool の選択や実行回数は LLM の判断によって変化します。

## エラー処理

各 Windows コマンドは `try / except` を利用して実行しています。

コマンド実行中にエラーが発生した場合でもアプリケーション全体を停止させず、
エラー情報を Tool の実行結果として扱えるようにしています。

また、`subprocess.run()` にタイムアウトを設定し、
コマンドが長時間終了しない場合に Agent 全体が停止することを防いでいます。

Agent Loop にも最大実行回数を設定し、
LLM が Tool Call を繰り返した場合の無限ループを防止しています。

## プロジェクトの目的

このプロジェクトは AI エージェントの仕組みを学習することを目的として開発しています。

LangChain / LangGraph などの Agent フレームワークを最初から使用せず、
OpenAI API の Function Calling と Python を使って Agent Loop を実装しています。

これにより、以下の流れを自分で実装しながら理解することを目的としています。

```text
LLMによる判断
    ↓
Function Calling
    ↓
PythonによるTool実行
    ↓
実行結果をLLMへ返却
    ↓
次の行動をLLMが判断
```

## 今後の予定

### v2

v2 では Web アプリケーション化を予定しています。

- FastAPI によるバックエンド API 化
- React による Web UI
- ユーザーからのトラブル内容の入力
- Web UI 上での診断結果表示
- RAG を利用したトラブルシューティング情報の検索

RAG では、FAQ・Windows のトラブルシューティング資料・仮想的な社内 IT マニュアルなどを検索し、
Tool による実機調査とドキュメント検索を組み合わせた診断を目指します。

### 将来的な学習候補

v1 / v2 の基礎を理解した後、必要に応じて以下の技術についても学習予定です。

- MCP
- LangChain
- LangGraph
- Multi-Agent

## Version

**v1**

OpenAI Responses API と Function Calling を利用した、
Windows ネットワークトラブル診断 Agent の基本機能を実装。
