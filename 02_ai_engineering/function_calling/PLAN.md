# Function Calling — Build Plan

**Model:** Gemma 4 31B (Google AI Studio, free tier)  
**SDK:** `google-genai`  
**Goal:** Multi-turn CLI chat where the LLM decides when to call Python tools.

**Portfolio role:** This is a small proof of controlled tool use, not a full agent product. It should show that tools are schema-defined, testable, bounded, and logged.

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

### ~~Step 2 — Tool Schemas~~ ✅ DONE
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

### ~~Step 3 — Agent Loop (`agent.py`)~~ ✅ DONE
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

### ~~Step 4 — Multi-turn CLI~~ ✅ DONE
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

## Hardening To Do Before Calling It Portfolio-Ready

### 1. Max tool-call guard

Add a per-turn limit, e.g. max 5 tool calls before returning an error to the user.

Why:
- prevents infinite loops
- shows production judgment
- makes the agent safer to demo

### 2. Tool error handling

Wrap each tool call in `try/except` and return a structured error object to the model.

Example shape:

```python
{"ok": false, "error": "File not found", "tool": "read_file"}
```

Why:
- tools fail in real systems
- the model should receive an observation, not crash the process

### 3. Structured tool-call logging

Log each call as JSONL:

```json
{"run_id":"...", "tool":"calculate", "args":{"expression":"2+2"}, "ok":true, "latency_ms":12}
```

Why:
- proves observability discipline
- can feed the later `06_observability` module

### 4. Unit tests for tools

Test tools without the LLM:
- calculator accepts safe math
- calculator rejects unsafe expressions
- file reader handles missing file
- weather handles HTTP failure gracefully

Why:
- separates deterministic code testing from model behavior

### 5. Saved demo transcript

Add a short `demo_transcript.md` showing:
- user asks for weather
- user asks for math
- user asks to read a file and summarize it
- agent calls tools transparently

Why:
- gives reviewers a quick understanding without running API keys

---

## Interview Angles

1. **What problem:** LLMs can't do real-time lookups or math reliably — tools bridge that gap
2. **Design decision:** Kept tool logic and schema separate so tools are unit-testable without the LLM in the loop
3. **Production concern:** Tool calls can loop infinitely — add a max-iterations guard (e.g. 5 tool calls per turn)
4. **Reliability concern:** Tool calls fail — return structured errors and let the model recover
5. **Observability concern:** Log every tool call with run ID, latency, success/failure, and arguments

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
