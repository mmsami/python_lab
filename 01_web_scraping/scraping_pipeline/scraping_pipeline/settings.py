# Scrapy settings for scraping_pipeline project
# https://docs.scrapy.org/en/latest/topics/settings.html

BOT_NAME = "scraping_pipeline"
SPIDER_MODULES = ["scraping_pipeline.spiders"]
NEWSPIDER_MODULE = "scraping_pipeline.spiders"
ADDONS = {}

# =============================================================================
# IDENTITY
# =============================================================================

# Mimic a real Chrome browser — default Scrapy UA gets blocked instantly
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

# LinkedIn's robots.txt blocks all scrapers, so obeying it means scraping nothing
ROBOTSTXT_OBEY = False

# Default request headers to look more like a real browser
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

# =============================================================================
# RATE LIMITING  (most important section for avoiding bans)
# =============================================================================

# Only 1 request at a time — never hammer LinkedIn in parallel
CONCURRENT_REQUESTS = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 1

# Base delay between requests in seconds
DOWNLOAD_DELAY = 3

# Randomizes delay between 0.5x and 1.5x DOWNLOAD_DELAY (so 1.5s–4.5s)
# This makes your traffic pattern look much less robotic
RANDOMIZE_DOWNLOAD_DELAY = True

# =============================================================================
# AUTOTHROTTLE  (automatically slows down if the server is struggling)
# =============================================================================

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2  # Initial delay before AutoThrottle kicks in
AUTOTHROTTLE_MAX_DELAY = 30  # Never wait longer than this
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0  # Aim for 1 simultaneous request
AUTOTHROTTLE_DEBUG = False  # Set True to log throttling decisions

# =============================================================================
# DOWNLOADER MIDDLEWARES
# =============================================================================

DOWNLOADER_MIDDLEWARES = {
    # Disable the built-in static UA middleware
    "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,
    # Rotate User-Agents randomly per request
    # Install with: pip install scrapy-user-agents
    "scrapy_user_agents.middlewares.RandomUserAgentMiddleware": 400,
    # Built-in retry middleware (keep enabled)
    "scrapy.downloadermiddlewares.retry.RetryMiddleware": 550,
    # Built-in HTTP cache middleware (keep enabled)
    "scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware": 900,
}

# =============================================================================
# RETRY
# =============================================================================

RETRY_ENABLED = True
RETRY_TIMES = 3  # Retry up to 3 times before giving up
RETRY_HTTP_CODES = [429, 500, 502, 503, 504]  # Retry on these status codes

# =============================================================================
# COOKIES & SESSION
# =============================================================================

# Keep cookies enabled — LinkedIn uses session cookies for some pages
COOKIES_ENABLED = True

# =============================================================================
# HTTP CACHE  (saves responses to disk — use during development)
# Comment out or set HTTPCACHE_ENABLED = False in production
# =============================================================================

HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 86400  # Cache lives for 24 hours
HTTPCACHE_DIR = ".httpcache"  # Where to store cached responses
HTTPCACHE_IGNORE_HTTP_CODES = [429, 503]  # Don't cache error responses
HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# =============================================================================
# OUTPUT / FEED EXPORT
# =============================================================================

FEED_EXPORT_ENCODING = "utf-8"
FEED_EXPORT_OVERWRITE = True  # Overwrite output file on each run (prevents broken JSON)

# =============================================================================
# PLAYWRIGHT  (for JS-heavy pages — only used when spider requests it)
# =============================================================================

# Route all HTTP/HTTPS through Playwright's download handler
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

# Playwright requires asyncio reactor
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

# LinkedIn pages are JS-heavy — give them plenty of time to load
PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 60000  # 60 seconds
PLAYWRIGHT_DEFAULT_TIMEOUT = 60000  # 60 seconds

# Uncomment to watch the browser while debugging
# PLAYWRIGHT_LAUNCH_OPTIONS = {"headless": False}

# Default Playwright context settings (optional fine-tuning)
PLAYWRIGHT_CONTEXTS = {
    "default": {
        "viewport": {"width": 1280, "height": 800},
        "locale": "en-US",
        "timezone_id": "Europe/Berlin",
    }
}

# =============================================================================
# LOGGING
# =============================================================================

LOG_LEVEL = "INFO"  # Change to DEBUG for verbose output while developing
