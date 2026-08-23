# Structured Extraction — Build Plan

**Timebox:** 60 minutes. **Rule:** type it yourself, no coding agent.

**Goal:** Turn a messy job posting into typed, validated JSON. Bridge unstructured text and
structured systems reliably — the single most common applied-AI prototype pattern in enterprise software.

**Stack:** `google-genai` (reuse the client pattern from `function_calling/agent.py`), `pydantic`, `python-dotenv`.

---

## File Structure

```
structured_extraction/
├── PLAN.md
├── requirements.txt
├── extract.py           ← model call + validation + retry
├── models.py            ← Pydantic schema
└── samples/
    ├── sap_ai_frontrunner.txt
    └── ...              ← 3-4 more postings, paste from anywhere
```

---

## Build Steps

### Step 1 — Schema (`models.py`)

A `JobPosting` model. Suggested fields:

| Field | Type | Notes |
|---|---|---|
| `title` | `str` | required |
| `company` | `str` | required |
| `location` | `list[str]` | multiple sites are common |
| `seniority` | `Literal["junior","mid","senior","lead","unclear"]` | forces the model to pick |
| `work_model` | `Literal["onsite","hybrid","remote","unclear"]` | |
| `language` | `Literal["en","de","other"]` | |
| `must_haves` | `list[str]` | max 8 |
| `nice_to_haves` | `list[str]` | max 8 |
| `tech_stack` | `list[str]` | named tools/frameworks only |

Use `Literal` and `Field(max_length=...)` deliberately — a constrained enum is what makes the
output usable downstream, and it is a good thing to be able to explain out loud.

### Step 2 — Extraction call (`extract.py`)

- `extract(text: str) -> JobPosting`
- Ask for JSON only. Use the SDK's structured-output / `response_mime_type="application/json"` path
  rather than parsing prose — if that fails, fall back to strict `json.loads` on the response text.
- Validate with `JobPosting.model_validate_json(...)`.

### Step 3 — Retry on validation failure

On `ValidationError`, retry **once**, feeding the error message back to the model as correction
context. Second failure → raise a clear exception naming the offending field. Do not retry forever.

### Step 4 — CLI

`python extract.py samples/sap_ai_frontrunner.txt` → pretty-printed JSON to stdout,
plus a stderr line with latency and token counts.

---

## Acceptance Checks

- All sample files extract and validate.
- Feed it a file of pure garbage → fails cleanly with a readable error, no crash, no silent empty object.
- Corrupt the schema deliberately (make a required field impossible) → confirm the retry path fires
  once and then raises. You need to have *seen* this happen, not assume it.

---

## Interview Angles

1. **What problem:** enterprise systems need typed records; LLM output is prose. Validation is the contract boundary.
2. **Design decision:** `Literal` enums over free-text strings — constrains the model and makes downstream code total.
3. **Production risk:** schema drift and silent partial extraction. Handled by validating every response
   and retrying once with the error as context, rather than trusting the first output.
4. **Cost/latency note:** one extraction ≈ one call; the retry path doubles worst-case cost — worth
   measuring before enabling it on a batch.
