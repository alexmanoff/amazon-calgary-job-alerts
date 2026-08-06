import re
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from models import Job

URL = "https://hvr-amazon.my.site.com/BBIndex?sfdcIFrameOrigin=null"

def fetch_jobs() -> list[Job]:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(locale="en-CA")
        page.goto(URL, wait_until="networkidle", timeout=90000)
        soup = BeautifulSoup(page.content(), "html.parser")
        browser.close()

    jobs, used = [], set()
    for link in soup.find_all("a", href=True):
        container = link.find_parent(["article", "li", "tr", "div"])
        text = container.get_text(" ", strip=True) if container else ""
        match = re.search(r"Job ID:\s*(\d+)", text, re.I)
        if not match:
            continue
        url = link["href"]
        if url.startswith("/"):
            url = "https://hvr-amazon.my.site.com" + url
        if url in used:
            continue
        used.add(url)
        jobs.append(Job("amazon_hvr", match.group(1),
                        link.get_text(" ", strip=True) or "Amazon job",
                        "", url, text))
    return jobs
