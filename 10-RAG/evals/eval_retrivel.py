import json

from deepeval import evaluate
from deepeval.evaluate import AsyncConfig
from deepeval.metrics import (
    ContextualPrecisionMetric,
    ContextualRecallMetric,
)
from deepeval.models import GeminiModel
from deepeval.test_case import LLMTestCase
from dotenv import load_dotenv

from src.retrival.query_embedder import embed_query
from src.retrival.reranker import reranker
from src.retrival.retriver import retrieve

load_dotenv()


GOLDEN_PATH = "golden/golden_dataset.json"

JUDGE_MODEL = "gemini-3.5-flash-lite"

THRESHOLD = 0.7


def load_goldens(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def run():
    # -----------------------------------
    # 1. Load golden dataset
    # -----------------------------------

    goldens = load_goldens(GOLDEN_PATH)

    print(f"Loaded {len(goldens)} goldens")

    # -----------------------------------
    # 2. Create Gemini judge
    # -----------------------------------

    judge_model = GeminiModel(
        model=JUDGE_MODEL,
        temperature=0,
    )

    # -----------------------------------
    # 3. Create test cases
    # -----------------------------------

    test_cases = []

    for golden in goldens[:5]:
        query = golden["question"]

        expected_output = golden["ideal_answer"]

        # -------------------------------
        # Query → embedding
        # -------------------------------

        query_vector = embed_query(query)

        # -------------------------------
        # Qdrant retrieval
        # -------------------------------

        retrieved = retrieve(
            query_vector=query_vector,
            top_k=10,
        )

        # -------------------------------
        # Reranking
        # -------------------------------

        reranked = reranker(
            query=query,
            results=retrieved,
            top_k=3,
        )

        # -------------------------------
        # Extract chunk text
        # -------------------------------

        retrieval_context = [result.payload["content"] for result, score in reranked]

        # -------------------------------
        # Create DeepEval test case
        # -------------------------------

        test_cases.append(
            LLMTestCase(
                input=query,
                expected_output=expected_output,
                retrieval_context=retrieval_context,
                # We are NOT evaluating generation yet.
                actual_output="Retriever evaluation only.",
            )
        )

    # -----------------------------------
    # 4. Define metrics
    # -----------------------------------

    metrics = [
        ContextualRecallMetric(
            threshold=THRESHOLD,
            model=judge_model,
            include_reason=True,
        ),
        ContextualPrecisionMetric(
            threshold=THRESHOLD,
            model=judge_model,
            include_reason=True,
        ),
    ]



    # -----------------------------------
    # 5. Run evaluation
    # -----------------------------------

    results = evaluate(
        test_cases=test_cases,
        metrics=metrics,
        async_config=AsyncConfig(
            run_async=True,
            max_concurrent=1,
            throttle_value=15,
        ),
    )

    return results


if __name__ == "__main__":
    run()
