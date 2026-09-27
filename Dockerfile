# Dockerイメージ(3.13-slimが入ったLinux)
FROM python:3.13-slim

# コンテナの作業ディレクトリ
WORKDIR /app

# /app/requirements.txtにコピー
COPY requirements.txt .
# テキストファイルに記載されている依存ライブラリをインストール
RUN pip install --no-cache-dir -r requirements.txt
# /app/main.pyにコピー
COPY main.py .
# /app/srcにコピー
COPY src ./src 
# /app/knowledgeにコピー
COPY knowledge ./knowledge

# FastAPI 8000ポートで実行
EXPOSE 8000

# コンテナ起動
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]