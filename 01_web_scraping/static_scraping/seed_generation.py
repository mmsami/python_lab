base_url = "https://englishjobs.de/jobs/product_manager"
num_pages = 3
page_urls = []

for counter in range(1, num_pages + 1):
    if counter == 1:
        page_urls.append(base_url)
    full_urls = base_url + "?page=" + str(counter)
    page_urls.append(full_urls)

print(page_urls)
