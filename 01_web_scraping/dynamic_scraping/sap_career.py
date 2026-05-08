import asyncio

from playwright.async_api import async_playwright

link = "https://jobs.sap.com/search/?createNewAlert=false&q=&locationsearch=&optionsFacetsDD_department=&optionsFacetsDD_customfield3=&optionsFacetsDD_country=DE"


async def scrape():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto(url=link)

        # wait for dynamic content to load
        await page.wait_for_selector("div.searchResultsShell")

        body_text = await page.inner_text("body")

        print(body_text)
        await browser.close()


asyncio.run(scrape())
