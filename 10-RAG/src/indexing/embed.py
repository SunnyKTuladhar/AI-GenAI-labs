from sentence_transformers import SentenceTransformer

MODEL_NAME = "BAAI/bge-small-en-v1.5"

model = SentenceTransformer(MODEL_NAME)


def embed_chunks(chunks: list[dict]) -> list[dict]:
    texts = [chunk["content"] for chunk in chunks]

    embeddings = model.encode(texts)

    embeded_chunks = []

    for chunk, embedding in zip(chunks, embeddings):
        embeded_chunks.append(
            {
                "content": chunk["content"],
                "source": chunk["source"],
                "embedding": embedding.tolist(),
            }
        )

    return embeded_chunks
