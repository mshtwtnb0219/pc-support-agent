from src.openai_client import client
from src.rag.retriever import retrieve

def generate_answer(question: str) -> str:
    # 関連するKnowledgeを検索
    results = retrieve(question)
    
    # 検索結果からLLMに渡すContextを作成
    contexts = []
    
    for result in results:
        contexts.append(result["content"])
    
    # リスト内の文字列を連結する
    context = "\n\n".join(contexts)
    
    # Contextを使って回答を生成
    response = client.responses.create(
        model="gpt-5.5",
        instructions=(
            "あなたはPCトラブルシューティングのアシスタントです。"
            "提供された参考情報をもとに質問に回答してください。"
            "参考情報だけでは判断できない場合は、その旨を伝えてください。"
        ),
        input=f"""
参考情報:
{context}

質問:
{question}
"""
    )
    
    return response.output_text

if __name__ == "__main__":
    question = "DNSがおかしい場合はどう確認すればいい？"
    answer = generate_answer(question)

    print(answer)