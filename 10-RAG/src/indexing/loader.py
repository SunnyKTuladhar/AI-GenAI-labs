from pathlib import Path


def load_document(data_dir: str) -> list[dict]:
    documents = []

    for file_path in Path(data_dir).rglob("*.md"):
        # print(file_path)
        content = file_path.read_text(encoding="utf-8")
        # print(content)
        documents.append({"content": content, "source": str(file_path)})
    # print(documents)

    return documents

