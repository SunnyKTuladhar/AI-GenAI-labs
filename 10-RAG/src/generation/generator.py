from src.generation.llm_client import generate_text


def generate_answer(prompt: str) -> str:
    return generate_text(prompt=prompt)
