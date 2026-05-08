import asyncio

from playwright.async_api import Browser, Locator, Page, async_playwright

link = "https://quotes.toscrape.com/scroll"


async def scrape_infinite_scroll():
    async with async_playwright() as p:
        browser: Browser = await p.chromium.launch(headless=True)
        page: Page = await browser.new_page()
        await page.goto(url=link)

        # We'll scroll 3 times to load more content
        for _ in range(3):
            # Scroll to the very bottom of the document
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

            # Wait for the 'Loading...' indicator to disappear or for new content
            # A short sleep is often necessary for the JS to trigger the fetch
            await page.wait_for_timeout(2000)

        quotes_locator: Locator = page.locator(".quote")
        count = await quotes_locator.count()
        for i in range(count):
            # Get a locator for the specific index
            quote = quotes_locator.nth(i)

            # Accessing text via locators is cleaner
            # we can chain them: quote.locator(".text")
            text = await quote.locator(".text").inner_text()
            author = await quote.locator(".author").inner_text()

            print(f"Quote: {text} | Author: {author}")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(scrape_infinite_scroll())
