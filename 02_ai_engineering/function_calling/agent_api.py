from ast import While
import os
import requests
import json
from pathlib import Path
from dotenv import load_dotenv

from tools.file_reader import SCHEMA as file_schema
from tools.file_reader import read_file
from tools.math_tools import SCHEMAS as math_schemas
from tools.math_tools import add, calculate, multiply
from tools.weather import SCHEMA as weather_schema
from tools.weather import get_weather

load_dotenv(Path(__file__).parent.parent.parent / ".env")

GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemma-4-31b-it"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent"

# Your tools definitions (same as before)
TOOL_MAP = {
      "get_weather": get_weather,
      "read_file": read_file,
      "calculate": calculate,
      "add": add,
      "multiply": multiply,
}

def run_agent():
    print("Agent ready. Type 'exit' to quit.")

    messages = []

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ("exit", "quit"):
            break

        messages.append({
            "role": "user",
            "parts": [{"text": user_input}]
        })

    print(f"Messages: {json.dumps(messages, indent=2)}")


if __name__ == "__main__":
    run_agent()
