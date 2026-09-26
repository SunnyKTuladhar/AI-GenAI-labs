# eval_rag_pipeline.py
import json

from deepeval import evaluate
from deepeval.evaluate import AsyncConfig
from deepeval.metrics import (
    AnswerRelevancyMetric,
    ContextualRelevancyMetric,
    FaithfulnessMetric,
)
from deepeval.models import GeminiModel
from deepeval.test_case import LLMTestCase
from dotenv import load_dotenv

from src.rag_pipeline import RagPipeline

load_dotenv()

GOLDEN_PATH = "golden/golden_dataset.json"  # reuse the queries
JUDGE_MODEL = "gemini-3-flash-preview"
THRESHOLD = 0.7


def load_goldens(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def run(rag):
    # 1. LOAD queries (we only need the queries --- context comes from the pipeline now)
    goldens = load_goldens(GOLDEN_PATH)

    # 2. RUN THE INJECTED PIPELINE per query, build a test case from LIVE output
    test_cases = []
    for g in goldens[:2]:
        result = rag.invoke(g["question"])  # retrieve -> rerank -> generate

        test_cases.append(
            LLMTestCase(
                input=g["question"],
                actual_output=result["answer"],  # what the generator produced
                retrieval_context=result["context"],  # what the RETRIEVER returned
            )
        )
    judge_model = GeminiModel(
        model=JUDGE_MODEL,
        temperature=0,
    )

    # 3. THE THREE TRIAD METRICS
    metrics = [
        ContextualRelevancyMetric(
            threshold=THRESHOLD, model=judge_model, include_reason=True
        ),
        FaithfulnessMetric(threshold=THRESHOLD, model=judge_model, include_reason=True),
        AnswerRelevancyMetric(
            threshold=THRESHOLD, model=judge_model, include_reason=True
        ),
    ]

    # 4. EVALUATE
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


def run_local():
    """Standalone convenience: build the pipeline, then run."""
    return run(RagPipeline())


if __name__ == "__main__":
    run_local()
