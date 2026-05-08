# Function Calling — Build Plan

**Model:** Gemma 4 27B (Google AI Studio, free tier)  
**SDK:** `google-genai`  
**Goal:** Multi-turn CLI chat where LLM decides when to call Python tools

---

## File Structure

```
function_calling/
├── PLAN.md
├── requirements.txt
├── .env.example
├── agent.py          ← main loop
└── tools/
    ├── __init__.py
    ├── weather.py    ← wttr.in (no API key)
    ├── calculator.py ← safe math eval
    └── file_reader.py← read local .txt / .csv
```

---

## Build Steps

### ~~Step 1 — Tools (no LLM yet)~~ ✅ DONE
Each tool is a plain Python function + a schema dict describing it.

**weather.py**
- `get_weather(city: str) -> str`
- Calls `wttr.in/{city}?format=3` (free, no key)

**calculator.py**
- `calculate(expression: str) -> str`
- Uses `ast.literal_eval` / `simpleeval` — no raw `eval()`

**file_reader.py**
- `read_file(path: str) -> str`
- Reads file, returns first 2000 chars + line count

### Step 2 — Tool Schemas
Each tool exports a `SCHEMA` dict in Gemini function declaration format:
```python
SCHEMA = {
    "name": "get_weather",
    "description": "Get current weather for a city",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "City name"}
        },
        "required": ["city"]
    }
}
```

### Step 3 — Agent Loop (`agent.py`)
```
while True:
    user input
    → send to Gemma with tools registered
    → if response has function_call:
        execute matching Python function
        append tool result to history
        send back to model
    → else:
        print model text reply
```
Handles: multi-turn history, consecutive tool calls, graceful exit.

### Step 4 — Multi-turn CLI
- Maintain `history` list across turns
- `quit` / `exit` to end session
- Print which tool was called (transparency)

---

## Key Design Decisions

| Decision | Why |
|---|---|
| `wttr.in` for weather | Zero API keys — runs anywhere |
| `simpleeval` not `eval()` | Prevents code injection |
| Tool schemas separate from logic | Tools stay testable without LLM |
| History passed each call | Gemini is stateless — we own context |

---

## Interview Angles

1. **What problem:** LLMs can't do real-time lookups or math reliably — tools bridge that gap
2. **Design decision:** Kept tool logic and schema separate so tools are unit-testable without the LLM in the loop
3. **Production concern:** Tool calls can loop infinitely — add a max-iterations guard (e.g. 5 tool calls per turn)

---

## Setup

```bash
pip install google-genai simpleeval python-dotenv
```

`.env`:
```
GOOGLE_API_KEY=your_key_from_aistudio.google.com
```

Get free key: https://aistudio.google.com/apikey
