from src.openai_client import client


# Embedding
def create_embedding(text : str) -> list[float]:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    
    return response.data[0].embedding


if __name__ == "__main__":
    embedding = create_embedding(
        "インターネットにつながらない"
    )
    
    # 先頭から10文字を切り取り
    print(embedding[:10])
    print("次元数", len(embedding))