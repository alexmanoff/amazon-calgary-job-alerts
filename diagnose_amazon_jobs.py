import re
import requests
from bs4 import BeautifulSoup

URL = (
    "https://www.amazon.jobs/en/search?"
    "city=Calgary&country=CAN&county=Alberta&latitude=51.04533&"
    "loc_query=Calgary%2C+AB%2C+Canada&longitude=-114.06301&"
    "radius=24km&region=Alberta&sort=recent"
)


def main():
    response = requests.get(
        URL,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/149.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-CA,en;q=0.9",
        },
        timeout=30,
    )

    print("HTTP STATUS:", response.status_code)
    print("FINAL URL:", response.url)
    print("CONTENT TYPE:", response.headers.get("content-type"))

    if response.status_code != 200:
        print("PAGE START:")
        print(response.text[:2000])
        return

    soup = BeautifulSoup(response.text, "html.parser")
    links = []
    seen = set()

    for link in soup.find_all("a", href=True):
        href = link["href"]
        if "/jobs/" not in href:
            continue
        if href.startswith("/"):
            href = "https://www.amazon.jobs" + href
        if href in seen:
            continue
        seen.add(href)

        text = link.get_text(" ", strip=True)
        container = link.find_parent(["article", "li", "div"])
        container_text = container.get_text(" ", strip=True) if container else text
        job_id_match = re.search(r"Job ID:\s*([A-Za-z0-9-]+)", container_text, re.I)

        links.append(
            {
                "title": text,
                "url": href,
                "job_id": job_id_match.group(1) if job_id_match else "",
                "text": container_text[:500],
            }
        )

    print("JOB LINKS FOUND:", len(links))

    for item in links[:20]:
        print("-" * 60)
        print("TITLE:", item["title"])
        print("JOB ID:", item["job_id"])
        print("URL:", item["url"])
        print("TEXT:", item["text"])


if __name__ == "__main__":
    main()
