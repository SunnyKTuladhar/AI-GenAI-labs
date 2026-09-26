from sentence_transformers import SentenceTransformer

MODEL_NAME = "BAAI/bge-small-en-v1.5"

model = SentenceTransformer(MODEL_NAME)


def embed_query(query: str) -> list[float]:
    embedding = model.encode(query)
    return embedding.tolist()


# if __name__ == "__main__":
#     embedding = embed_query("what is the exam poly here?")
#     print("----" * 1000)
#     print(embedding)
