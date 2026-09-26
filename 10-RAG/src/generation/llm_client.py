import os 
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL_NAME = "gemini-3.5-flash-lite"

def generate_text(prompt:str)->str:
    response = client.models.generate_content(
        model = MODEL_NAME,
        contents=prompt,
    )

    return response.text

# def generate_text(prompt: str):
#     """Streaming — yields text chunks as they arrive. Use this for
#     'instant answer' feel in a chat UI (see your earlier question)."""
#     response_stream = client.models.generate_content_stream(
#         model=MODEL_NAME,
#         contents=prompt,
#     )
#     for chunk in response_stream:
#         if chunk.text:
#             yield chunk.text