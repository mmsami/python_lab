import time

import httpx
from bs4 import BeautifulSoup


def scrape_books(max_pages=3):
    with httpx.Client() as client:
        for page in range(1, max_pages + 1):
            print(f"--- Fetching Page {page} ---")

            # The f-string injects the current page number directly into the URL
            url = f"https://books.toscrape.com/catalogue/page-{page}.html"

            response = client.get(url=url)
            if response.status_code != 200:
                print(f"Reached the end or encountered an error at page {page}")
                break
            soup = BeautifulSoup(response.text, "lxml")
            books = soup.find_all("article", class_="product_pod")

            for book in books:
                title = book.h3.a["title"]
                price = book.find("p", class_="price_color").text
                print(f"Title: {title} | Price: {price}")

            time.sleep(1)


if __name__ == "__main__":
    scrape_books(max_pages=3)
