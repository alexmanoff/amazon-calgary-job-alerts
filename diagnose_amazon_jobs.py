import re
from playwright.sync_api import sync_playwright

URL = (
    "https://www.amazon.jobs/en/search?"
    "city=Calgary&country=CAN&county=Alberta&latitude=51.04533&"
    "loc_query=Calgary%2C+AB%2C+Canada&longitude=-114.06301&"
    "radius=24km&region=Alberta&sort=recent"
)


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            locale="en-CA",
            viewport={"width": 1440, "height": 1400},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/149.0.0.0 Safari/537.36"
            ),
        )

        response = page.goto(URL, wait_until="domcontentloaded", timeout=90000)
        page.wait_for_timeout(5000)

        print("HTTP STATUS:", response.status if response else "NO RESPONSE")
        print("FINAL URL:", page.url)
        print("TITLE:", page.title())

        body_text = page.locator("body").inner_text()
        print("BODY TEXT LENGTH:", len(body_text))

        all_links = page.locator("a").evaluate_all(
            """els => els.map(a => ({
                text: (a.innerText || '').trim(),
                href: a.href || ''
            }))"""
        )

        print("TOTAL LINKS:", len(all_links))

        job_links = []
        seen = set()
        for item in all_links:
            href = item.get("href", "")
            if not re.search(r"amazon\.jobs/(?:en/)?jobs/\d+", href, re.I):
                continue
            if href in seen:
                continue
            seen.add(href)
            job_links.append(item)

        print("JOB LINKS FOUND:", len(job_links))

        for item in job_links[:20]:
            job_id_match = re.search(r"/jobs/(\d+)", item["href"])
            print("-" * 60)
            print("TITLE:", item["text"])
            print("JOB ID:", job_id_match.group(1) if job_id_match else "")
            print("URL:", item["href"])

        ids_in_text = sorted(set(re.findall(r"Job ID:\s*(\d+)", body_text, re.I)))
        print("JOB IDS IN BODY TEXT:", len(ids_in_text))
        print("FIRST JOB IDS:", ids_in_text[:20])

        print("\nBODY TEXT START:")
        print(body_text[:5000])

        browser.close()


if __name__ == "__main__":
    main()
