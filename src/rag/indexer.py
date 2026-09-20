from src.rag.loader import load_documents
from src.rag.chunker import split_text
from src.rag.embedding import create_embedding
from src.supabase_client import supabase

def build_index():
    documents = load_documents()
    
    for document in documents:
        chunks = split_text(document["content"])
        
        for chunk in chunks:
            embedding = create_embedding(chunk)
            data = {
                "source": document["source"],
                "content": chunk,
                "embedding": embedding
            }
            
            supabase.table("rag_documents").insert(data).execute()
            print(f"INSERT：{document['source']}")


if __name__ == "__main__":
    build_index()