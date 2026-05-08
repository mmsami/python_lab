import requests
from bs4 import BeautifulSoup

url = "https://www.tilburgsciencehub.com/topics/collect-store/data-collection/web-scraping/scrape-static-websites/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Check if the request was successful
    soup = BeautifulSoup(response.text, "lxml")

    print(f"--- Scraping: {url} ---\n")

    # 1. Finding by Tag
    h1_tag = soup.find("h1")
    print(f"H1 Title: {h1_tag.get_text(strip=True) if h1_tag else 'Not Found'}")

    # 2. Finding All and Indexing
    h2_tags = soup.find_all("h2")
    if len(h2_tags) > 2:
        print(f"Third H2: {h2_tags[2].get_text(strip=True)}")

    # 3. Extracting Attributes (Links)
    print("\n--- Extracting Links ---")
    for link in soup.find_all("a", limit=5):  # Limit for clean output
        href = link.get("href")
        if href:
            print(f"Link: {href}")

    # 4. Finding by Class
    codeblock = soup.find(class_="codeblock")
    if codeblock:
        print(f"\nCodeblock Content:\n{codeblock.get_text(strip=True)}")

    # 5. Finding by ID
    seed = soup.find(id="seed-generation")
    if seed:
        print(f"\nSection by ID: {seed.get_text(strip=True)}")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
