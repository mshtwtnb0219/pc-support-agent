
from src.rag.loader import load_documents

# 自力でChunk分割 100はデフォルト値
def split_text(text: str, chunk_size: int = 100, overlap: int = 20) -> list[str]:
    chunks = []
    
    step = chunk_size - overlap
    
    for i in range(0,len(text), step):
        # i:i → slice 〇文字以上、〇文字未満
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)
    return chunks
    
    
if __name__ == "__main__":
    documents = load_documents()

    for document in documents:
        chunks = split_text(document["content"])

        for chunk in chunks:
            print("----- CHUNK -----")
            print(chunk)