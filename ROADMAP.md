# Python Automation & AI Engineering Lab — Roadmap

Target roles: AI Software Engineer, AI Application Developer, Automation Engineer, Data Engineer
Current status: 01_web_scraping complete

---

## Priority 1 — Close SAP AI role gaps (build in next 2 weeks)

### 05_ai_engineering/01_function_calling
**Why:** LLM tool use / agentic systems explicitly in SAP JD. Not covered by smart_job_agent.
**What to build:** Python functions (weather lookup, calculator, file reader) registered as LLM tools; LLM decides when to call them; result fed back into conversation. Multi-turn CLI chat.
**Stack:** Anthropic SDK, tool_use API
**Interview angle:** "I understand how agents decide when to delegate vs. reason directly."

### 05_ai_engineering/02_structured_extraction
**Why:** Extracting typed data from LLMs is in almost every AI/automation role. Directly applicable to enterprise data work.
**What to build:** Extract structured JSON from unstructured text (job postings, emails, invoices) using JSON mode / output_config; validate with Pydantic.
**Stack:** anthropic, Pydantic
**Interview angle:** "I can bridge unstructured text and structured systems reliably."

### 05_ai_engineering/03_streaming_chat
**Why:** Every production AI app uses streaming. Shows you think about UX and don't just do batch calls.
**What to build:** CLI chat that streams tokens as they arrive; shows time-to-first-token; graceful error handling on dropped streams.
**Stack:** anthropic (streaming), asyncio
**Interview angle:** "I build for users, not just for correctness."

### 07_infra_as_code/dockerized_scripts
**Why:** Docker explicitly required in SAP JD. Cloud Foundry deployment (MXP project) partially covers this but no Dockerfile in portfolio.
**What to build:** Containerize one existing project (smart_job_agent retrieval step or a scraper). Dockerfile + .env handling + docker-compose for local dev.
**Stack:** Docker, docker-compose, python-dotenv
**Interview angle:** "I deploy, not just run locally."

### 02_api_automation/rest_client
**Why:** Production REST patterns (retry, auth, rate limiting) are in every AI/automation role. You already wrote this in reranker.py — extract and document it.
**What to build:** Reusable requests session with exponential backoff, bearer token auth, rate limit handling, response validation with Pydantic.
**Stack:** requests, tenacity (or manual retry), Pydantic
**Interview angle:** Shows you write defensively, not just happy-path.

---

## Priority 2 — Supporting evidence (build after Priority 1)

### 04_data_eng_core/etl_csv_parquet
**Why:** Maps to Vantage data pipeline background; modern stack shows you've kept up.
**What to build:** Ingest CSV → clean → transform → write Parquet; query with DuckDB.
**Stack:** polars, duckdb, pathlib

### 04_data_eng_core/async_pipeline
**Why:** High-volume fetch pattern common in AI data collection. Demonstrates concurrency understanding.
**What to build:** Async fetch of 100+ URLs with aiohttp; bounded concurrency with asyncio.Semaphore; error handling per request.
**Stack:** asyncio, aiohttp

### 06_workflow_automation/scheduled_jobs
**Why:** Automation identity — shows you think about recurring, unattended execution.
**What to build:** APScheduler job that runs a pipeline on a cron; logs output; handles failures gracefully.
**Stack:** APScheduler, logging

### 05_ai_engineering/04_llm_wrappers
**Why:** Standardized interface over multiple providers — directly applicable to multi-LLM systems like your smart_job_agent.
**What to build:** Thin wrapper that accepts provider name + model; returns standard response object; swap between Anthropic, OpenAI, Ollama without changing caller code.
**Stack:** anthropic, openai, httpx (for Ollama)

### 05_ai_engineering/05_llm_evals
**Why:** Testing LLM output quality is a differentiator — few candidates show this. SAP would care about this for enterprise reliability.
**What to build:** Simple eval harness: define test cases with expected outputs, run them against a model, score with exact match + LLM-as-judge, report pass/fail with metrics.
**Stack:** anthropic, pytest (or plain Python), json

---

## Priority 3 — Defer or skip

| Module | Reason to defer |
|---|---|
| 03_browser_automation/cdp_demo | Advanced, low relevance for AI roles |
| 02_api_automation/graphql_queries | Niche, not in target JDs |
| 06_workflow_automation/simple_dag | Only if Airflow/Prefect appears in JD |
| 05_ai_engineering/rag_example | Already covered by smart_job_agent (124k records, P@10 0.70) |
| 05_ai_engineering/embedding_pipeline | Already covered by smart_job_agent |
| MCP server/client | Growing but not yet in most JDs — add only if it appears in a specific role |
| Prompt engineering module | Demonstrated through other projects, not needed standalone |
| Fine-tuning | Not relevant for target roles |

---

## Already complete (reference these in interviews)

| Project | Key evidence |
|---|---|
| smart_job_agent | RAG pipeline, 124k records, P@10 0.70 vs BM25 0.50, LLM reranker, evaluation framework |
| MXP automation (SAP) | Python/Streamlit to Cloud Foundry in 5 weeks, replaced Java, production-deployed |
| 01_web_scraping | Static (BS4), dynamic (Selenium/Playwright), Scrapy pipeline with SAP careers spider |

---

## Interview prep rule

Build each module so you can explain:
1. What problem it solves
2. One design decision you made and why
3. What would break in production and how you'd handle it

Syntax you can look up. Design judgment is what they test.
