from pathlib import Path

def load_documents():
    knowledge_dir = Path("knowledge")
    
    documents = []
    
    for file_path in knowledge_dir.glob("*.txt"):
        content = file_path.read_text(encoding="utf-8")

        documents.append(
            {
                "source": file_path.name,
                "content": content
            })
        
    return documents

# このファイルが直接実行されたときだけ、以下の処理を実行する
if __name__ == "__main__":
    docs = load_documents()

    for doc in docs:
        print(doc["source"])
        print(doc["content"])