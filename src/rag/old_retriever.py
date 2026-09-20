from src.rag.loader import load_documents 
from src.rag.chunker import split_text
from src.rag.embedding import create_embedding
from src.rag.similarity import cosine_similarity

# 毎回 knowledgeからembeddingするパターン
def retrieve(question: str, top_k: int = 3) -> list[dict]:
    
    # 質問からコンピューターが計算できる数値の並び(ベクトル)に変換する
    question_embedding = create_embedding(question)
    
    results = []
    
    # knowledge配下のフォルダからテキストを読み込む
    documets = load_documents()
    
    for document in documets:
        # chunckに分割
        chunks = split_text(document["content"])
        
        for chunk in chunks:
            # テキストファイルからoverlapした内容を数値(ベクトル)に変換する
            chunk_embedding = create_embedding(chunk)
            # 質問の内容とベクトルが近しいか判別
            score = cosine_similarity(question_embedding, chunk_embedding)
            
            results.append({
                # ファイル名
                "source": document["source"],
                # 評価文字列
                "content": chunk,
                # ベクトル値
                "score": score
            })
    
    # 評価結果をソートする  降順
    results.sort(
        key=lambda result: result["score"],
        reverse=True
    )
    
    # 上記　○○位まで返却する
    return results[:top_k]


if __name__ == "__main__":
    question = "DNSがおかしい場合はどう確認すればいい？"

    results = retrieve(question)

    for result in results:
        print("----- RESULT -----")
        print("source:", result["source"])
        print("score:", result["score"])
        print("content:", result["content"])