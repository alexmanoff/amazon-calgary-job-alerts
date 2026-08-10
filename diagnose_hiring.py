from playwright.sync_api import sync_playwright

URL = "https://hiring.amazon.ca/search/warehouse-jobs?cmpid=ECPNLC185H12"


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page(
            locale="en-CA",
            viewport={"width": 1440, "height": 1200},
        )

        response = page.goto(
            URL,
            wait_until="networkidle",
            timeout=90000,
        )

        print("HTTP STATUS:", response.status if response else "NO RESPONSE")
        print("FINAL URL:", page.url)
        print("TITLE:", page.title())

        links = page.locator("a").evaluate_all(
            """els => els.map(a => ({
                text: (a.innerText || '').trim(),
                href: a.href
            }))"""
        )

        print("TOTAL LINKS:", len(links))

        job_links = [
            item for item in links
            if "jobdetail" in item["href"].lower()
            or "job" in item["href"].lower()
        ]

        print("POSSIBLE JOB LINKS:", len(job_links))

        for item in job_links[:20]:
            print(item)

        print("\nPAGE TEXT START:")
        print(page.locator("body").inner_text()[:5000])

        browser.close()


if __name__ == "__main__":
    main()
