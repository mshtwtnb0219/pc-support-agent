
from src.rag.loader import load_documents

# 自力でChunk分割 100はデフォルト値
def split_text(text: str, chunk_size: int = 100) -> list[str]:
    
    chunks = []
    current_chunk = ""
    
    # 文字列を改行単位で分割する
    lines = text.splitlines()
    for line in lines:
        candidate = current_chunk + line + "\n"
        
        # 現在のchunkに追加しても chunk_sizeを超えないなら追加
        if len(current_chunk) <= chunk_size:
            current_chunk = candidate
        else:
            # 今までため込んだものを1chunkとして確定
            if current_chunk:
                chunks.append(current_chunk.strip())
            # 今の行から次のchunkを開始
            current_chunk = line + "\n"
    
    # 最後のchunkを追加
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks
    
    
if __name__ == "__main__":
    documents = load_documents()

    for document in documents:
        chunks = split_text(document["content"])

        for chunk in chunks:
            print("----- CHUNK -----")
            print(chunk)