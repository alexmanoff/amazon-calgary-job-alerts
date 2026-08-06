import re
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from models import Job

URL = "https://hiring.amazon.ca/search/warehouse-jobs?cmpid=ECPNLC185H12"

def fetch_jobs() -> list[Job]:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(locale="en-CA")
        page.goto(URL, wait_until="networkidle", timeout=90000)
        soup = BeautifulSoup(page.content(), "html.parser")
        browser.close()

    jobs, used = [], set()
    for link in soup.select('a[href*="/jobDetail/"]'):
        url = link.get("href", "")
        if url.startswith("/"):
            url = "https://hiring.amazon.ca" + url
        if not url or url in used:
            continue
        used.add(url)
        card = link.find_parent(["article", "li", "div"])
        text = card.get_text(" ", strip=True) if card else link.get_text(" ", strip=True)
        title = link.get_text(" ", strip=True) or "Amazon job"
        match = re.search(r"(JOB-CA-\d+|a0R[A-Za-z0-9]+)", url)
        job_id = match.group(1) if match else url
        jobs.append(Job("amazon_hiring", job_id, title, "", url, text))
    return jobs
