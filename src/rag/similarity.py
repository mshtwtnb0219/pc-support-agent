import math

from src.rag.embedding import create_embedding


def cosine_similarity(vector_a: list[float], vector_b: list[float]) -> float:
    dot_product = sum(a * b for a, b in zip(vector_a, vector_b))

    magnitude_a = math.sqrt(sum(a * a for a in vector_a))
    magnitude_b = math.sqrt(sum(b * b for b in vector_b))

    return dot_product / (magnitude_a * magnitude_b)


if __name__ == "__main__":
    question = "インターネットにつながらない"

    texts = [
        "Wi-Fiの接続状態を確認してください",
        "DNS名前解決が正常か確認してください",
        "今日の夕飯はカレーです"
    ]

    question_embedding = create_embedding(question)

    for text in texts:
        text_embedding = create_embedding(text)

        score = cosine_similarity(
            question_embedding,
            text_embedding
        )

        print(text, score)