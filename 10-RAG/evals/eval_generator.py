import json

from deepeval import evaluate
from deepeval.evaluate import AsyncConfig
from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
)
from deepeval.models import GeminiModel
from deepeval.test_case import LLMTestCase
from dotenv import load_dotenv

from src.agumentation.prompt_builder import build_prompt
from src.generation.generator import generate_answer

load_dotenv()


GOLDEN_PATH = "golden/golden_dataset.json"
JUDGE_MODEL = "gemini-3.5-flash-lite"
THRESHOLD = 0.7


def load_goldens(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def run():
    # 1. Load generator golden dataset
    goldens = load_goldens(GOLDEN_PATH)

    print(f"Loaded {len(goldens)} generator goldens")

    # 2. Create Gemini judge
    judge_model = GeminiModel(
        model=JUDGE_MODEL,
        temperature=0,
    )

    # 3. Generate answers using the GOLDEN context
    test_cases = []

    for golden in goldens[:3]:
        query = golden["question"]
        context = golden["context"]

        prompt = build_prompt(query=query, context=context)
        answer = generate_answer(prompt=prompt)

        test_cases.append(
            LLMTestCase(
                input=query,
                actual_output=answer,
                retrieval_context=context,
            )
        )

    # 4. Define generator metrics
    metrics = [
        FaithfulnessMetric(
            threshold=THRESHOLD,
            model=judge_model,
            include_reason=True,
        ),
        AnswerRelevancyMetric(
            threshold=THRESHOLD,
            model=judge_model,
            include_reason=True,
        ),
    ]

    # 5. Run evaluation

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
