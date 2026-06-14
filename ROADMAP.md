# Python Automation & AI Engineering Lab — Roadmap

Target roles: AI Software Engineer, AI Application Developer, AI Product Manager, Automation Engineer
Build order: each module builds on the previous. Do them in sequence.

---

## 01_web_scraping — DONE
Static (BS4), dynamic (Selenium/Playwright), Scrapy pipeline with SAP careers spider.

---

## 02_ai_engineering — IN PROGRESS

### 01_function_calling — DONE
LLM tool use, multi-turn agent loop: plan → call tool → observe result → next step. Anthropic SDK tool_use API.

### 02_structured_extraction
Extract typed JSON from unstructured text (job postings, emails, invoices).
Validate with Pydantic. JSON mode / output_config.
**Stack:** anthropic, Pydantic
**Interview angle:** "I can bridge unstructured text and structured systems reliably."

### 03_streaming_chat
CLI chat that streams tokens as they arrive. Time-to-first-token metrics. Graceful error handling on dropped streams.
**Stack:** anthropic (streaming), asyncio
**Interview angle:** "I build for users, not just for correctness."

### 04_llm_wrappers
Thin wrapper accepting provider name + model, returning standard response object. Swap Anthropic / OpenAI / Ollama without changing caller code.
**Stack:** anthropic, openai, httpx (for Ollama)
**Interview angle:** "I design abstractions that survive provider changes."

### 05_llm_evals
Eval harness: test cases with expected outputs, run against model, score with exact match + LLM-as-judge, report pass/fail with metrics.
**Stack:** anthropic, pytest, json
**Interview angle:** "I test AI output quality, not just code correctness — a differentiator for enterprise roles."

### 06_observability
Structured logging on every LLM call: tokens in/out, latency, cost estimate, model, errors. Generate a simple summary report from logs.
**Stack:** Python logging, structlog, json
**Interview angle:** "I instrument AI systems so failures and costs are visible — not just correctness."

---

## 03_api_automation

### 01_rest_client
Reusable requests session: exponential backoff, bearer token auth, rate limit handling, Pydantic response validation.
**Stack:** requests, tenacity, Pydantic
**Interview angle:** "I write defensively, not just happy-path."

### 02_fastapi_ai_service
Wrap your LLM functions (from 02_ai_engineering) as REST endpoints. Async endpoints, Pydantic request/response validation, auto Swagger UI at /docs.
**Stack:** FastAPI, Pydantic, uvicorn
**Interview angle:** "I can expose AI capabilities to any frontend or system — I think end-to-end."

---

## 04_data_eng_core

### 01_etl_csv_parquet
Ingest CSV → clean → transform → write Parquet. Query with DuckDB.
**Stack:** polars, duckdb, pathlib

### 02_async_pipeline
Async fetch of 100+ URLs with aiohttp. Bounded concurrency with asyncio.Semaphore. Per-request error handling.
**Stack:** asyncio, aiohttp

---

## 05_workflow_automation

### 01_scheduled_jobs
APScheduler job running a pipeline on cron. Logs output, handles failures gracefully.
**Stack:** APScheduler, logging

---

## 06_infra_as_code

### 01_dockerized_scripts
Containerize your FastAPI AI service (03/02). Dockerfile + .env handling + docker-compose for local dev.
**Stack:** Docker, docker-compose, python-dotenv
**Interview angle:** "I deploy, not just run locally."

---

## Defer / skip

| Module | Reason |
|---|---|
| 03_browser_automation/cdp_demo | Advanced, low relevance for AI roles |
| graphql_queries | Niche, not in target JDs |
| simple_dag | Only if Airflow/Prefect appears in JD |
| rag_example | Already covered by smart_job_agent |
| embedding_pipeline | Already covered by smart_job_agent |
| MCP server/client | Add only if it appears in a specific JD |
| Fine-tuning | Not relevant for target roles |

---

## Already complete (reference in interviews)

| Project | Key evidence |
|---|---|
| smart_job_agent | RAG pipeline, 124k records, P@10 0.70 vs BM25 0.50, LLM reranker, evaluation framework |
| MXP automation | Python/Streamlit to Cloud Foundry in 5 weeks, replaced Java, production-deployed |
| 01_web_scraping | Static (BS4), dynamic (Selenium/Playwright), Scrapy pipeline |

---

## AI PM artifact (non-code, one doc)

Write a 1-page product framing for the smart_job_agent RAG system:
- What problem it solves and for whom
- How you measured success (P@10 0.70 vs BM25 0.50, Wilcoxon p-values)
- What trade-offs you made and why
- What would make you roll it back in production

This is not a README. It is a product decision document. One page. Plain English.
Write it as if presenting to a non-technical hiring manager.

---

## Interview prep rule

For every module, be ready to explain:
1. What problem it solves
2. One design decision you made and why
3. What would break in production and how you'd handle it

Syntax you can look up. Design judgment is what they test.
