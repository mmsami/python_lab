import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types
from tools.file_reader import SCHEMA as file_schema
from tools.file_reader import read_file
from tools.math_tools import SCHEMAS as math_schemas
from tools.math_tools import add, calculate, multiply
from tools.weather import SCHEMA as weather_schema
from tools.weather import get_weather

load_dotenv(Path(__file__).parent.parent.parent / ".env")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable is not set")

MODEL_NAME = "gemma-4-31b-it"


all_schemas = [weather_schema, file_schema] + math_schemas
function_declarations = [types.FunctionDeclaration(**schema) for schema in all_schemas]

client = genai.Client(api_key=GOOGLE_API_KEY)
tools = types.Tool(function_declarations=function_declarations)
config = types.GenerateContentConfig(tools=[tools])

TOOL_MAP = {
    "get_weather": get_weather,
    "read_file": read_file,
    "calculate": calculate,
    "add": add,
    "multiply": multiply,
}


def run_agent():
    print("Agent ready. Type 'exit' to quit.")

    # Start a chat session – this automatically manages history
    chat = client.chats.create(model=MODEL_NAME, config=config)

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ("exit", "quit"):
            break

        response = chat.send_message(user_input)

        candidate = response.candidates[0] if response.candidates else None
        parts = (
            candidate.content.parts if (candidate and candidate.content) else None
        ) or []

        # handle tool calls
        for part in parts:
            if part.function_call:
                fn_name = part.function_call.name
                fn_args = dict(part.function_call.args or {})
                print(f"[calling tool: {fn_name}({fn_args})]")

                if fn_name and fn_name in TOOL_MAP:
                    result = TOOL_MAP[fn_name](**fn_args)
                    response = chat.send_message(
                        types.Part.from_function_response(
                            name=fn_name,
                            response={"result": result},
                        )
                    )

        print(f"Agent: {response.text}")


if __name__ == "__main__":
    run_agent()
