# SAP Spider — Full Implementation Plan

## Current State
- Spider scrapes page 1 of SAP Germany jobs (25 results)
- Extracts: title, city, url
- Pagination selector works: `ul.pagination li.active + li a::attr(href)`
- Job ID is embedded in every URL: `/job/.../1278781801/` — last segment

## What Needs Building

### Step 1 — Inspect job detail page HTML
Before writing any parsing code, run playwright on one real job URL to see actual HTML structure.

```python
# Use sap_career.py as base, point it at one job URL e.g.:
link = "https://jobs.sap.com/job/Berlin-Senior-Product-Security-Engineer-%28fmd%29-10557/1278781801/"
# Dump inner_html of the main job content div
# Look for: posted date, closing date, description, responsibilities, requirements
```

Run and inspect. Then decide which fields are separable by HTML tags vs full description fallback.

### Step 2 — Add two-level crawl to spider

`parse` (list pages) → yields Request per job → `parse_job` (detail page)

```python
async def parse(self, response):
    for row in response.css("table#searchresults tbody tr"):
        title = row.css("span.jobTitle.hidden-phone a.jobTitle-link::text").get("").strip()
        relative_link = row.css("span.jobTitle.hidden-phone a.jobTitle-link::attr(href)").get("")
        city = row.css("td.colLocation span.jobLocation::text").get("").strip()
        job_id = relative_link.rstrip("/").split("/")[-1]

        # STOP CONDITION: if job_id already in seen_ids, stop paginating
        if job_id in self.seen_ids:
            self.logger.info(f"Hit known job {job_id} — stopping pagination")
            return

        yield scrapy.Request(
            url="https://jobs.sap.com" + relative_link,
            meta={**self._playwright_meta(), "title": title, "city": city, "job_id": job_id},
            callback=self.parse_job,
        )

    # follow next page only if no stop triggered
    next_page = response.css("ul.pagination li.active + li a::attr(href)").get()
    if next_page:
        yield scrapy.Request(url=response.urljoin(next_page), meta=self._playwright_meta(), callback=self.parse)

async def parse_job(self, response):
    yield {
        "job_id":       response.meta["job_id"],
        "title":        response.meta["title"],
        "city":         response.meta["city"],
        "url":          response.url,
        "posted_date":  response.css("SELECTOR::text").get("").strip(),   # fill after step 1
        "closing_date": response.css("SELECTOR::text").get("").strip(),   # fill after step 1
        "description":  " ".join(response.css("SELECTOR ::text").getall()).strip(),  # fill after step 1
    }
```

### Step 3 — Load seen IDs on startup

```python
import json
import os

class SapSpider(scrapy.Spider):
    name = "sap_spider"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seen_ids = self._load_seen_ids()

    def _load_seen_ids(self):
        path = "sap_jobs.json"
        if not os.path.exists(path):
            return set()
        with open(path) as f:
            try:
                data = json.load(f)
                return {job["job_id"] for job in data if "job_id" in job}
            except (json.JSONDecodeError, KeyError):
                return set()
```

### Step 4 — Switch output to SQLite via pipeline (optional upgrade)

In `pipelines.py`:
```python
import sqlite3

class SQLitePipeline:
    def open_spider(self, spider):
        self.conn = sqlite3.connect("sap_jobs.db")
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                job_id TEXT PRIMARY KEY,
                title TEXT,
                city TEXT,
                url TEXT,
                posted_date TEXT,
                closing_date TEXT,
                description TEXT,
                scraped_at TEXT
            )
        """)

    def process_item(self, item, spider):
        self.conn.execute("""
            INSERT OR IGNORE INTO jobs VALUES (?,?,?,?,?,?,?,datetime('now'))
        """, (item["job_id"], item["title"], item["city"], item["url"],
              item["posted_date"], item["closing_date"], item["description"]))
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.conn.close()
```

Enable in settings.py:
```python
ITEM_PIPELINES = {
    "scraping_pipeline.pipelines.SQLitePipeline": 300,
}
```

## Target JSON/DB Schema

```json
{
  "job_id":       "1278781801",
  "title":        "Senior Product Security Engineer (f/m/d)",
  "city":         "Berlin, DE, 10557",
  "url":          "https://jobs.sap.com/job/Berlin-.../1278781801/",
  "posted_date":  "2025-04-01",
  "closing_date": "2025-05-01",
  "description":  "Full job description text — or split into responsibilities/requirements if HTML tags allow"
}
```

## Run Commands

```bash
cd 01_web_scraping/scraping_pipeline

# First run — scrapes all jobs + all detail pages
scrapy crawl sap_spider -o sap_jobs.json

# Subsequent runs — only new jobs, stops on first known job_id
scrapy crawl sap_spider -o sap_jobs.json
```

## Current File State
- Spider: `scraping_pipeline/spiders/sap_spider.py`
- Settings: `scraping_pipeline/settings.py`
- Pipelines: `scraping_pipeline/pipelines.py` (unused, ready for SQLite)
- Output: `sap_jobs.json`

## Key Decisions Made
- Sort order is `referencedate desc` (newest first) — safe to stop on first known ID
- Job ID extracted from URL, no need to visit detail page for it
- Start with JSON output, SQLite is a pipeline swap when needed
- `networkidle` causes timeouts on SAP (constant background XHR) — use `wait_for_selector` only
- Pagination URL is relative (`?q=...`) — always use `response.urljoin()` not string concat
