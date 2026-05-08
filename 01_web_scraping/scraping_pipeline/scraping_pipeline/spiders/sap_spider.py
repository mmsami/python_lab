import scrapy
from scrapy_playwright.page import PageMethod


class SapSpider(scrapy.Spider):
    name = "sap_spider"

    target_url = "https://jobs.sap.com/search/?createNewAlert=false&q=&locationsearch=&optionsFacetsDD_department=&optionsFacetsDD_customfield3=&optionsFacetsDD_country=DE"

    def _playwright_meta(self):
        return {
            "playwright": True,
            "playwright_page_methods": [
                PageMethod("wait_for_selector", "table#searchresults tbody tr"),
            ],
        }

    def start_requests(self):
        yield scrapy.Request(
            url=self.target_url,
            meta=self._playwright_meta(),
            callback=self.parse,
        )

    async def parse(self, response):
        base_url = "https://jobs.sap.com"

        for row in response.css("table#searchresults tbody tr"):
            # hidden-phone span = desktop version, avoids duplicate mobile title
            title = row.css("span.jobTitle.hidden-phone a.jobTitle-link::text").get("").strip()
            relative_link = row.css("span.jobTitle.hidden-phone a.jobTitle-link::attr(href)").get("")
            # city lives inside span.jobLocation inside td.colLocation
            city = row.css("td.colLocation span.jobLocation::text").get("").strip()

            if title:
                yield {
                    "title": title,
                    "city": city,
                    "url": base_url + relative_link if relative_link else "",
                }

        # next page href is relative (?q=...&startrow=25), urljoin resolves it correctly
        next_page = response.css("ul.pagination li.active + li a::attr(href)").get()
        if next_page:
            yield scrapy.Request(
                url=response.urljoin(next_page),
                meta=self._playwright_meta(),
                callback=self.parse,
            )
