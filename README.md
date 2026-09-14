# PC Support Agent

Windows PC のネットワークトラブルを調査するAIエージェントです。

## 概要

OpenAI API の Function Calling / Tool Calling を利用して、
PCのネットワーク状態を確認しながら原因を調査します。

AIが必要に応じて以下のコマンドを自律的に選択・実行します。

- ipconfig
- ping
- nslookup

## 主な機能

- PCのIPアドレス情報取得
- ルーター・外部IPへの疎通確認
- DNS名前解決の確認
- 複数Toolの連続実行
- 調査結果をもとにした原因候補・対処方法の提示
- Agent Loopによる追加調査
- エラー処理・タイムアウト制御

## 使用技術

- Python
- OpenAI Responses API
- Function Calling / Tool Calling
- subprocess
- python-dotenv

## 実行イメージ

```text
ユーザー:
インターネットがつながりません。原因を調べてください。
↓
AI:
ipconfig を実行
↓
AI:
ping を実行
↓
AI:
nslookup を実行
↓
AI:
調査結果を分析して原因候補と対処方法を回答
```
