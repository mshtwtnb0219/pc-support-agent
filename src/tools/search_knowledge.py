from src.rag.retriever import retrieve


def search_knowledge(query: str) -> str:
    # 質問に対して近しい上位3つのchunkを取得
    results = retrieve(query)
    
    contexts = []
    
    for result in results:
        contexts.append(
            f"""
source: {result["source"]}
content: {result["content"]}
similarity: {result["similarity"]}
"""
        )
        
    return "\n".join(contexts)
    
    
if __name__ == "__main__":
    result = search_knowledge(
        "DNSがおかしい場合はどう確認すればいい？"
    )

    print(result)