from src.rag.loader import load_documents
from src.rag.chunker import split_text
from src.rag.embedding import create_embedding
from src.supabase_client import supabase

import hashlib

# knowledgeフォルダ配下のテキストファイルをchunk化 → embeddingしてpgに登録
def build_index():
    documents = load_documents()
    
    for document in documents:
        
        # knowledgeファイルのハッシュ化を行い登録済みかを確認
        file_hash = create_file_hash(document["content"])
        
        response = (
            supabase
            .table("rag_documents")
            .select("source, file_hash")
            .eq("source", document["source"])
            .limit(1)
            .execute()
        )
        
        # response.dataが空の場合　→　新規ファイル
        if not response.data:
            print("NEW：", document["source"])
        else:
            #　ハッシュ値が一致している場合　変更なし
            db_hash = response.data[0]["file_hash"]
            if db_hash == file_hash:
                print("SKIP：", document["source"])
                continue 
            # ハッシュ値が一致していない場合　更新
            else:
                print("UPDATE：", document["source"])
                # 現状登録されているレコードを削除
                supabase \
                    .table("rag_documents") \
                    .delete() \
                    .eq("source", document["source"]) \
                    .execute()
        
        chunks = split_text(document["content"])
        
        for chunk in chunks:
            embedding = create_embedding(chunk)
            data = {
                "source": document["source"],
                "content": chunk,
                "embedding": embedding,
                "file_hash": file_hash
            }
            
            supabase.table("rag_documents").insert(data).execute()
            print(f"INSERT：{document['source']}")
            

# ハッシュ化 
def create_file_hash(content: str) -> str:
    return hashlib.sha256(
        content.encode("utf-8")
    ).hexdigest()
    


if __name__ == "__main__":
    build_index()