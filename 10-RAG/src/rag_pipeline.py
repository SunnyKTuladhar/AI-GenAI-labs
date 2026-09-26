from src.agumentation.context_builder import build_context
from src.agumentation.prompt_builder import build_prompt
from src.generation.generator import generate_answer
from src.retrival.query_embedder import embed_query
from src.retrival.reranker import reranker
from src.retrival.retriver import retrieve


class RagPipeline:
    def __init__(self, fetch_k: int = 10, top_k: int = 5):
        self.fetch_k = fetch_k
        self.top_k = top_k

    def invoke(self, query: str) -> dict:
        # 1. Embed the user's query
        query_vector = embed_query(query=query)

        # 2. Retrieve candidate chunks from Qdrant
        retrieved_results = retrieve(
            query_vector=query_vector,
            top_k=self.fetch_k,
        )

        # 3. Rerank retrieved chunks using the CrossEncoder
        reranked_results = reranker(
            query=query,
            results=retrieved_results,
            top_k=self.top_k,
        )

        # 4. Build a clean context from the reranked chunks
        context = build_context(reranked_results)

        # 5. Build the final prompt using query + context
        prompt = build_prompt(
            query=query,
            context=context,
        )

        # 6. Generate the final answer
        answer = generate_answer(prompt)

        # 7. Return useful information for debugging/evaluation
        return {
            "query": query,
            "context": context,
            "answer": answer,
        }


if __name__ == "__main__":
    rag = RagPipeline()

    result = rag.invoke("How many credits do I need to graduate")

    print("QUERY:")
    print(result["query"])

    print("\nANSWER:")
    print(result["answer"])

    print("\nCONTEXT:")
    print(result["context"])
