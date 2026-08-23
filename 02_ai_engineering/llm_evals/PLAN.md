# LLM Evals — Build Plan

**Timebox:** 45 minutes. **Rule:** type it yourself, no coding agent.

**Goal:** A minimum credible eval harness over `structured_extraction`. Deterministic checks first,
LLM-as-judge only where determinism is impossible. Report pass rate, latency, and cost.

**Stack:** plain Python + `json`. `pytest` optional — do not spend the timebox on test plumbing.

---

## File Structure

```
llm_evals/
├── PLAN.md
├── cases.json           ← 10 cases: input file + expected fields
├── run_eval.py          ← runner + report
└── reports/
    └── eval_<run_id>.json
```

---

## Build Steps

### Step 1 — Cases (`cases.json`)

Ten cases is enough. Each case:

```json
{
  "id": "sap_frontrunner_01",
  "input_file": "../structured_extraction/samples/sap_ai_frontrunner.txt",
  "expect": { "seniority": "junior", "language": "en", "work_model": "unclear" },
  "expect_contains": { "tech_stack": ["Python", "TypeScript"] }
}
```

Only assert fields that are genuinely unambiguous in the source text. If you have to argue with
yourself about the right answer, the case is bad — drop it. Writing cases is where you find out
your schema is wrong, which is the actual point of the exercise.

### Step 2 — Checks

Two deterministic check types, nothing more:

- **exact** — `actual[field] == expected`
- **contains** — every expected list item appears in the actual list (case-insensitive)

Skip LLM-as-judge tonight. You can *explain* it from note 04 and note 12; you do not need to build it
in 45 minutes, and a half-built judge is worse than none.

### Step 3 — Runner

`run_eval.py` iterates cases, calls `extract()`, records per case:
`id`, `passed`, `failed_fields`, `latency_ms`, `input_tokens`, `output_tokens`, `est_cost_usd`.

Handle a case that throws: record it as a failure with the exception message. One bad case must not
kill the run — that is the whole reason the harness exists.

### Step 4 — Report

Print a table to stdout, write the full JSON to `reports/eval_<run_id>.json`:

```
CASES 10 | PASS 8 | FAIL 2 | p50 1.2s | p95 2.8s | total $0.004
FAILED: sap_frontrunner_01 (seniority), dhl_02 (tech_stack)
```

Percentiles matter more than the mean — say that out loud tomorrow if latency comes up.

---

## Acceptance Checks

- Run it twice. Note whether the same cases fail both times. **Non-determinism across runs is itself a
  finding** — if pass rate swings, that is the flakiness story the JD's "model or agent behaviour"
  line is asking about.
- Break one case's expectation on purpose → confirm it reports as a failure with the field named,
  rather than passing silently.

---

## Interview Angles

1. **What problem:** unit tests check code; nothing checks whether model output is still correct after
   a prompt or model change. Evals are the regression suite for the non-deterministic part.
2. **Design decision:** deterministic field checks before LLM-as-judge — judges add cost, latency, and
   their own error rate, so use them only where no deterministic check exists.
3. **Production risk:** eval set rots as the schema evolves, and a passing suite gives false confidence.
   Cases get versioned with the schema and reviewed when either changes.
4. **What this gates:** pass-rate threshold as a ship/rollback gate before a prompt or model swap goes out.
