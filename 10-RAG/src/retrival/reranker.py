from sentence_transformers import CrossEncoder

MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"

model = CrossEncoder(MODEL_NAME)


def reranker(query: str, results, top_k: int = 3):
    pairs = []
    for result in results:
        content = result.payload["content"]
        pairs.append((query, content))

    scores = model.predict(pairs)

    ranked_results = []

    for result, score in zip(results, scores):
        ranked_results.append((result, score))

    ranked_results.sort(key=lambda x: x[1], reverse=True)

    return ranked_results[:top_k]
