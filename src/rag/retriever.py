from src.rag.embedding import create_embedding
from src.supabase_client import supabase

def retrieve(question: str, top_k: int = 3) -> list[dict]:
    
    # 質問からコンピューターが計算できる数値の並び(ベクトル)に変換する
    question_embedding = create_embedding(question)
    # supabaseのmath_rag_documents関数を呼び出す
    response = (
        supabase
        .rpc(
            "match_rag_documents",
            {
                # 引数
                "query_embedding": question_embedding,
                "match_count": top_k
            }
        )
        .execute()
    )
    
    return response.data


if __name__ == "__main__":
    question = "DNSがおかしい場合はどう確認すればいい？"

    results = retrieve(question)

    for result in results:
        print("----- RESULT -----")
        print("source:", result["source"])
        print("score:", result["similarity"])
        print("content:", result["content"])