# Python Automation & AI Solution Lab — Roadmap

## Purpose

This repo is a public technical lab, not the main portfolio flagship.

Use it to prove technical range in small, explainable modules: scraping, structured extraction, tool calling, evals, observability, APIs, Docker, and workflow automation. The flagship stories remain SAP MXP/Joule, SAP Storyline Generator, `smart_job_agent`, and the future Job Intelligence Graph / Application Workflow Agent.

Target positioning:

> AI-native technical product / solution builder who can understand a workflow, design the system, use AI coding tools to build faster, and validate the result with tests, logs, and evals.

Do not position this repo as proof of pure AI Engineer depth. It is proof that you can plan and build practical automation modules with sound engineering habits.

## Module Standard

Every module should have:

1. `PLAN.md` explaining the problem, design choices, and production risks.
2. Runnable command from the module folder.
3. Small tests where possible.
4. A short sample input/output artifact.
5. One interview note: what problem it solves, one tradeoff, what would break in production.

For AI modules, also include:
- schema or output contract
- failure handling
- cost/latency note where relevant
- eval or at least deterministic acceptance checks

## 01_web_scraping — Done, Optional Hardening

Current coverage:
- Static scraping with BeautifulSoup.
- Dynamic scraping with Selenium/Playwright.
- Scrapy pipeline with SAP careers spider.

Optional hardening before using publicly:
- Add job detail-page parsing to the SAP spider.
- Store results in SQLite instead of only JSON.
- Add duplicate detection by job ID.
- Add a small test or sample fixture for parser behavior.
- Add README snippet with run command and expected output.

Interview angle:
- Shows ingestion and automation basics, especially useful when discussing job data pipelines and scraping constraints.

## 02_ai_engineering — Main Lab Track

### 01_function_calling — Done, Needs Hardening

Current coverage:
- Gemini/Gemma function calling.
- Multi-turn CLI agent loop.
- Tool schemas separated from tool logic.
- Weather, file reader, and math tools.

Portfolio hardening:
- Add max tool-call guard per user turn.
- Add structured logs for each tool call.
- Add tests for tool functions without the LLM.
- Add one saved transcript showing multi-step tool use.
- Add graceful handling for unknown tool calls and tool errors.

Interview angle:
- "I understand tool use as controlled system integration, not magic chat. Tools are schema-defined, testable, logged, and bounded."

### 02_structured_extraction — Build Next

Goal:
- Extract typed JSON from messy text such as job postings, emails, invoices, or requirements notes.
- Validate output with Pydantic.
- Retry or return structured validation errors when extraction fails.

Suggested artifact:
- Job-posting extractor: `title`, `company`, `location`, `top_requirements`, `must_haves`, `nice_to_haves`, `language`, `seniority`, `work_model`.

Stack:
- Gemini or Anthropic, Pydantic, pytest.

Interview angle:
- "I can bridge unstructured text and structured systems reliably."

### 03_streaming_chat

Goal:
- CLI or small web endpoint that streams tokens as they arrive.
- Track time-to-first-token and total latency.
- Handle dropped streams cleanly.

Stack:
- Python async, provider streaming API, optionally FastAPI SSE.

Interview angle:
- "I design for perceived responsiveness, not just correctness."

### 04_llm_wrappers

Goal:
- Thin provider wrapper accepting provider + model and returning a standard response object.
- Swap Anthropic / OpenAI-compatible / Gemini / local provider without changing callers.

Stack:
- `httpx`, provider SDKs, Pydantic response model.

Interview angle:
- "I avoid vendor lock-in by normalizing the boundary, not by overengineering the app."

### 05_llm_evals — High Priority

Goal:
- Eval harness with test cases, expected outputs, exact/deterministic checks, optional LLM-as-judge, and pass/fail report.

Suggested artifact:
- Evaluate `02_structured_extraction` on 20-30 job descriptions.
- Track extraction accuracy for top requirements, language, seniority, and hard blockers.

Stack:
- pytest, JSON/CSV test cases, optional LLM judge.

Interview angle:
- "I test AI output quality, not just code correctness."

### 06_observability — High Priority

Goal:
- Structured logging for every LLM/tool call: model, tokens, latency, estimated cost, tool name, success/failure, run ID.
- Generate a simple summary report from logs.

Stack:
- Python logging or `structlog`, JSONL logs.

Interview angle:
- "I make AI systems inspectable: failures, latency, and cost are visible."

## 03_api_automation

### 01_rest_client

Goal:
- Reusable REST client with auth, retries, timeout, rate-limit handling, and Pydantic response validation.

Why it matters:
- Supports the SAP Storyline Generator and MXP/Joule story where external integration reliability is central.

Stack:
- `httpx` or `requests`, `tenacity`, Pydantic.

### 02_fastapi_ai_service

Goal:
- Wrap the structured extraction or eval module as a FastAPI service.
- Include `/health`, `/extract`, `/eval/run`, and OpenAPI docs.

Stack:
- FastAPI, Pydantic, uvicorn.

Interview angle:
- "I can expose AI capabilities as system APIs, not only scripts."

## 04_data_eng_core

### 01_etl_csv_parquet

Goal:
- CSV ingestion -> cleaning -> validation -> Parquet output -> query with DuckDB.

Suggested dataset:
- Job postings or scraped SAP jobs.

Stack:
- Polars or pandas, DuckDB, pathlib.

Interview angle:
- "Data quality and schema discipline matter before AI can work."

### 02_async_pipeline

Goal:
- Async fetch of many URLs with bounded concurrency, retries, and per-request error logging.

Stack:
- `asyncio`, `aiohttp` or `httpx.AsyncClient`.

Interview angle:
- "I know how to make ingestion faster without losing control of failures."

## 05_workflow_automation

### 01_scheduled_jobs

Goal:
- Schedule a recurring pipeline with logs and failure handling.

Stack:
- APScheduler or cron-style runner.

Good demo:
- Daily scrape -> normalize -> extract requirements -> write SQLite/Parquet -> generate summary report.

## 06_infra_as_code

### 01_dockerized_fastapi_service

Goal:
- Containerize `03_api_automation/02_fastapi_ai_service`.
- Include `.env.example`, Dockerfile, and docker-compose.

Interview angle:
- "I package tools so someone else can run them."

## Optional Modules

### MCP Server / Client

Do not prioritize here because MCP is already evidenced by SAP MXP/Joule.

Add only if useful for the Job Intelligence Graph or Application Workflow Agent:
- read-only evidence search tool
- issue lookup tool
- assessment retrieval tool

### A2A Mini-Demo

Optional proof-of-awareness only.

Build only if a target role mentions multi-agent interoperability:
- agent 1 extracts requirements
- agent 2 validates evidence
- supervisor asks for human approval before write action

### LangGraph / Workflow Graphs

Optional if a role expects agent workflow orchestration. Do not add just for trend coverage.

## Defer / Skip

| Module | Reason |
|---|---|
| Generic chatbot | Too common; weak portfolio signal |
| RAG example | Already covered better by `smart_job_agent`; only build a Job Evidence RAG if needed |
| Embedding pipeline | Already covered by `smart_job_agent` |
| Fine-tuning | Not relevant for current target lane |
| Kubernetes | Too much infra for the target roles |
| Complex cloud architecture | Not needed unless a specific JD requires it |
| Full React app for lab modules | Use only when frontend UX is the proof |

## Existing Projects To Reference Correctly

| Project | How to describe it |
|---|---|
| SAP MXP / Joule | Shipped enterprise workflow automation; strongest pivot proof |
| SAP Storyline Generator | Current-role architecture and rebuild planning; in-progress, use scoped verbs |
| smart_job_agent | Retrieval/reranking/evaluation pipeline, data cleaning, no UI; university project |
| job_portfolio | Real personal workflow automation and evidence-governed CV/CL system |
| python_lab | Public lab for small, explainable technical modules |

Use final `smart_job_agent` numbers only:
- FAISS_PARSED average P@10 = 0.53 vs BM25_PARSED = 0.50.
- Reranking improved FAISS_PARSED from 0.36 to 0.53, Wilcoxon p = 0.0117.

## Recommended Build Order

1. Harden `02_ai_engineering/function_calling`.
2. Build `02_structured_extraction`.
3. Build `05_llm_evals` against structured extraction.
4. Add `06_observability` logs and report.
5. Wrap extraction/eval in `03_api_automation/02_fastapi_ai_service`.
6. Dockerize the FastAPI service.
7. Optionally connect this lab to the Job Intelligence Graph/Application Workflow Agent later.

## Interview Prep Rule

For every module, be ready to explain:

1. What problem it solves.
2. One design decision you made and why.
3. What would break in production and how you would handle it.

Syntax can be looked up. Design judgment is the point.
