def build_context(results) -> str:
    contexts = []

    for i, (result, score) in enumerate(results, start=1):
        context = result.payload["content"]

        contexts.append(f"[context {i}]\n{context}")

    return "\n\n".join(contexts)
