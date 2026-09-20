from src.supabase_client import supabase
from src.rag.embedding import create_embedding


def insert_test():
    content = "Wi-Fiの接続状態を確認してください"
    
    # ベクトル変換
    embedding = create_embedding(content)
    
    data = {
        "source": "test",
        "content": content,
        "embedding": embedding
    }
    
    response = (
        supabase
        .table("rag_documents")
        .insert(data)
        .execute()
    )
    
    print(response)

    
    
# 実行
if __name__ == "__main__":
    insert_test()