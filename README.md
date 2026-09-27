# PC Support Agent

PCのネットワークトラブルを診断するAIエージェントです。

OpenAI Responses APIのFunction Callingを利用し、
ユーザーの質問に応じてネットワーク診断ツールやRAGによる
ナレッジ検索を自律的に実行します。

## Features

- OpenAI Responses APIを利用したAIエージェント
- Function Callingによるツールの自律実行
- ping / ipconfig / nslookupによるネットワーク診断
- Supabase + pgvectorを利用したRAG
- SHA-256によるナレッジの差分インデックス
- FastAPIによるバックエンドAPI
- React + TypeScriptによるチャットUI
- マルチターン会話
- Markdown表示
- エラーハンドリング

## Architecture

```text
React
  │
  │ POST /chat
  ▼
FastAPI
  │
  ▼
AI Agent
  │
  ├── ping
  ├── ipconfig
  ├── nslookup
  │
  └── search_knowledge
          │
          ▼
      Embedding
          │
          ▼
   Supabase / pgvector
```

## Tech Stack

### Backend

- Python
- FastAPI
- OpenAI Responses API
- OpenAI Embeddings API
- Supabase
- pgvector

### Frontend

- React
- TypeScript
- Vite
- Chakra UI
- React Markdown

### AI / RAG

- Function Calling
- Agent Loop
- Embeddingによるベクトル検索
- Supabase / pgvectorによるナレッジ検索
- SHA-256によるナレッジの差分更新

## Project Structure

```text
pc-support-agent/
├── main.py                     # FastAPI エントリーポイント
├── src/
│   ├── agent.py                # Agent Loop
│   ├── openai_client.py        # OpenAI クライアント
│   ├── supabase_client.py      # Supabase クライアント
│   │
│   ├── tools/
│   │   ├── definitions.py      # Function Calling のTool定義
│   │   ├── ping.py             # ping実行
│   │   ├── ipconfig.py         # ipconfig実行
│   │   ├── nslookup.py         # nslookup実行
│   │   └── search_knowledge.py # RAG検索Tool
│   │
│   └── rag/
│       ├── loader.py           # ナレッジファイル読み込み
│       ├── chunker.py          # テキスト分割
│       ├── embedding.py        # Embedding生成
│       ├── retriever.py        # pgvectorによる類似検索
│       ├── generator.py        # RAG単体の回答生成
│       └── indexer.py          # ナレッジの登録・差分更新
│
├── knowledge/
│   └── network_trouble.txt     # PCトラブルのナレッジ
│
├── frontend/
│   ├── src/
│   │   ├── App.tsx             # チャット画面
│   │   └── main.tsx            # Reactエントリーポイント
│   └── package.json
│
├── .env                        # 環境変数（Git管理対象外）
├── .gitignore
└── README.md
```

## Setup

### 1. Repository Clone

```bash
git clone <repository-url>
cd pc-support-agent
```

### 2. Backend Setup

Pythonの仮想環境を作成します。

#### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

依存ライブラリをインストールします。

```powershell
python -m pip install -r requirements.txt
```

### 3. Environment Variables

プロジェクト直下に `.env` を作成し、以下の環境変数を設定します。

```env
OPENAI_API_KEY=your_openai_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

`.env` はGit管理対象に含めないでください。

### 4. Supabase Setup

Supabaseでプロジェクトを作成し、pgvector拡張を有効化します。

```sql
create extension if not exists vector;
```

RAGで使用するテーブルを作成します。

```sql
create table rag_documents (
    id bigint generated always as identity primary key,
    source text not null,
    content text not null,
    embedding vector(1536) not null,
    file_hash text
);
```

ベクトル類似検索用のFunctionを作成します。

```sql
create or replace function match_rag_documents(
    query_embedding vector(1536),
    match_count int default 3
)
returns table (
    id bigint,
    source text,
    content text,
    similarity float
)
language sql
stable
as $$
    select
        id,
        source,
        content,
        1 - (embedding <=> query_embedding) as similarity
    from rag_documents
    order by embedding <=> query_embedding
    limit match_count;
$$;
```

> SupabaseのRLS（Row Level Security）は利用環境に合わせて適切に設定してください。
> 開発用の無制限なアクセス許可をそのまま公開環境で使用しないでください。

### 5. RAG Indexing

`knowledge/` 配下にナレッジとなるテキストファイルを配置します。

```text
knowledge/
└── network_trouble.txt
```

以下のコマンドでナレッジをSupabaseへ登録します。

```powershell
python -m src.rag.indexer
```

Indexerでは、ナレッジをチャンクに分割してEmbeddingを生成し、
Supabase / pgvectorへ保存します。

```text
knowledge/*.txt
      │
      ▼
    Loader
      │
      ▼
   Chunker
      │
      ▼
  Embedding
      │
      ▼
Supabase / pgvector
```

ファイル内容からSHA-256ハッシュを生成し、前回登録時と比較することで、
変更のないファイルは再インデックスせず、変更されたファイルのみ更新します。

### 6. Frontend Setup

`frontend` ディレクトリへ移動します。

```powershell
cd frontend
```

依存パッケージをインストールします。

```powershell
npm install
```

### 7. Run Application

バックエンドとフロントエンドをそれぞれ起動します。

#### Backend

プロジェクトルートで仮想環境を有効化し、FastAPIを起動します。

```powershell
.\.venv\Scripts\Activate.ps1
python -m uvicorn main:app --reload
```

FastAPI:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

#### Frontend

別のターミナルで `frontend` ディレクトリへ移動し、Viteを起動します。

```powershell
cd frontend
npm run dev
```

ブラウザから以下へアクセスします。

```text
http://localhost:5173
```

## Usage

チャット画面からPCのネットワークトラブルについて質問します。

例：

```text
インターネットにつながりません。
```

AI Agentは質問内容と会話履歴をもとに、必要なToolを選択して実行します。

## Agent Workflow

AgentはOpenAI Responses APIのFunction Callingを利用して、
必要な情報が揃うまでToolの実行と結果の確認を繰り返します。

```text
User
  │
  ▼
React Chat UI
  │
  ▼
FastAPI
  │
  ▼
AI Agent
  │
  ├─ 回答可能 ──────────────────┐
  │                              │
  └─ Toolが必要                  │
       │                         │
       ▼                         │
   Function Calling              │
       │                         │
       ├─ ping                   │
       ├─ ipconfig               │
       ├─ nslookup               │
       └─ search_knowledge       │
              │                  │
              ▼                  │
         Tool Result             │
              │                  │
              └──────► AI Agent ─┘
                         │
                         ▼
                    Final Answer
```

### Available Tools

| Tool               | Description                             |
| ------------------ | --------------------------------------- |
| `ping`             | 指定したIPアドレスへの疎通を確認        |
| `ipconfig`         | ネットワークインターフェース情報を取得  |
| `nslookup`         | DNSによる名前解決を確認                 |
| `search_knowledge` | RAGを利用してPCトラブルのナレッジを検索 |

Agent自身が質問内容から必要なToolを判断するため、
ユーザーが実行するToolを指定する必要はありません。

## RAG Workflow

PCトラブルに関するナレッジは、事前にEmbeddingを生成して
Supabase / pgvectorへ保存します。

### Indexing

```text
knowledge/*.txt
      │
      ▼
    Loader
      │
      ▼
    Chunker
      │
      ▼
OpenAI Embeddings
      │
      ▼
Supabase / pgvector
```

Indexerはファイル内容からSHA-256ハッシュを生成し、
既存データと比較して更新の必要性を判定します。

```text
File
 │
 ▼
SHA-256
 │
 ▼
Compare file_hash
 │
 ├─ NEW    → Index
 ├─ SKIP   → No update
 └─ UPDATE → Delete old chunks → Re-index
```

### Retrieval

Agentがナレッジを必要と判断すると、
`search_knowledge` Toolを呼び出します。

```text
User Question
      │
      ▼
search_knowledge
      │
      ▼
Question Embedding
      │
      ▼
pgvector Similarity Search
      │
      ▼
Relevant Chunks
      │
      ▼
AI Agent
      │
      ▼
Final Answer
```

ベクトル間の類似度にはCosine Similarityを利用し、
質問内容に近いナレッジを取得します。

## Notes / Limitations

### Local Diagnostic Tools

`ping`、`ipconfig`、`nslookup` はFastAPIが動作しているマシン上で実行されます。

そのため、ローカル環境ではPC自身のネットワーク診断に利用できますが、
FastAPIをクラウド環境へデプロイした場合は、ユーザーのPCではなく
クラウドサーバー上でコマンドが実行されます。

```text
Local

Browser
   │
   ▼
Local FastAPI
   │
   └─ ping / ipconfig / nslookup
              │
              ▼
           Local PC
```

```text
Cloud

Browser
   │
   ▼
Cloud FastAPI
   │
   └─ ping / ipconfig / nslookup
              │
              ▼
         Cloud Server
```

ブラウザからユーザーPC上のOSコマンドを直接実行することはできないため、
公開環境でローカルPCを診断するには別途ローカルクライアントなどの仕組みが必要です。

### Security

- `.env` やAPIキーはGitリポジトリへコミットしないでください。
- SupabaseのRLSは公開環境に合わせて適切に設定する必要があります。
- 公開環境ではAPIのRate Limitなど、追加の対策が必要です。

### Docker Environment

Docker環境ではFastAPIがLinuxコンテナ上で動作するため、
Windows固有の `ipconfig` Toolは利用できません。

また、Linux向けのネットワークコマンドへ置き換えた場合でも、
取得できるのはユーザーPCではなくコンテナ自身のネットワーク情報です。

そのため、Docker環境はWeb API・Agent・RAGの動作確認を主な目的とし、
ローカルPCのネットワーク診断はWindows上でFastAPIを直接実行する構成を使用します。

## Docker

FastAPIバックエンドはDockerコンテナ上でも起動できます。

### Build

プロジェクトルートでDocker Imageを作成します。

```powershell
docker build -t pc-support-agent .
```

### Run

`.env` の環境変数をコンテナへ渡して起動します。

```powershell
docker run --name pc-support-agent-api -p 8000:8000 --env-file .env pc-support-agent
```

起動後、以下からFastAPIへアクセスできます。

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

### Docker Environment Limitations

Docker環境ではFastAPIがLinuxコンテナ上で動作するため、
Windows固有の `ipconfig` Toolは利用できません。

Linux向けのネットワークコマンドへ置き換えた場合でも、
取得されるのはユーザーPCではなくコンテナ自身のネットワーク情報です。

そのため、Docker環境はFastAPI・AI Agent・RAG・Frontend連携の
動作確認を主な目的としています。

ローカルPCのネットワーク診断Toolを利用する場合は、
Windows上でFastAPIを直接起動してください。

## Future Improvements

- ローカル診断用クライアントの実装
- ナレッジデータの拡充
- RAG検索精度の改善
- 会話履歴管理の改善
- API Rate Limitの実装
- 認証機能
- Dockerによるコンテナ化
- Webアプリケーションのデプロイ
