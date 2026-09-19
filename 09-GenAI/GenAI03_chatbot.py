import os
from datetime import datetime

import gradio as gr

from dotenv import load_dotenv
load_dotenv()

from strands import Agent, tool
from strands.models.openai import OpenAIModel


# -----------------------------
# 1. Define tools
# -----------------------------

@tool
def calculate(expression: str) -> str:
    """Calculate a mathematical expression.

    Args:
        expression: A mathematical expression such as "25 * 4 + 10".

    Returns:
        The calculated result.
    """
    try:
        result = eval(expression, {"__builtins__": {}})
        return str(result)
    except Exception as e:
        return f"Could not calculate the expression: {e}"


@tool
def get_current_time() -> str:
    """Get the current date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@tool
def get_weather(city: str) -> str:
    """Get the weather for a city.

    This is a demo tool that returns mock weather data.

    Args:
        city: Name of the city.

    Returns:
        Weather information for the city.
    """

    # Demo data
    weather = {
        "kathmandu": "Sunny, 24°C",
        "pokhara": "Partly cloudy, 22°C",
        "london": "Cloudy, 15°C",
        "new york": "Sunny, 20°C",
    }

    return weather.get(
        city.lower(),
        f"No weather data available for {city}."
    )


# -----------------------------
# 2. Initialize model
# -----------------------------

model = OpenAIModel(
    model_id="openai/gpt-oss-120b",
    client_args={
        "api_key": os.getenv("GROQ_API_KEY"),
        "base_url": "https://api.groq.com/openai/v1"
    }
)


# -----------------------------
# 3. Create Strands Agent
# -----------------------------

agent = Agent(
    model=model,
    tools=[
        calculate,
        get_current_time,
        get_weather,
    ]
)


# -----------------------------
# 4. Chat function
# -----------------------------

def chat(message, history):
    response = agent(message)
    return str(response)


# -----------------------------
# 5. Gradio UI
# -----------------------------

gr.ChatInterface(
    fn=chat,
    title="Strands Tool-Using Chatbot",
    description="A chatbot powered by Strands + Groq + GPT-OSS-120B",
).launch()