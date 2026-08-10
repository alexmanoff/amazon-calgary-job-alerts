import re
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from models import Job

URL = "https://hvr-amazon.my.site.com/BBIndex?sfdcIFrameOrigin=null"

LOCATION_RE = re.compile(
    r"(?:Calgary|Rocky View County|Rocky View|Balzac|Airdrie)"
    r"(?:\s*,\s*(?:AB|Alberta))?(?:\s*,\s*(?:CAN|Canada))?",
    re.I,
)


def _context_for_job(body_text: str, job_id: str, radius: int = 700) -> str:
    match = re.search(rf"Job ID:\s*{re.escape(job_id)}", body_text, re.I)
    if not match:
        return ""
    start = max(0, match.start() - radius)
    end = min(len(body_text), match.end() + radius)
    return body_text[start:end]


def _extract_location(*texts: str) -> str:
    for text in texts:
        match = LOCATION_RE.search(text or "")
        if match:
            return match.group(0).strip(" ,")
    return ""


def fetch_jobs() -> list[Job]:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(locale="en-CA")
        page.goto(URL, wait_until="networkidle", timeout=90000)
        body_text = page.locator("body").inner_text()
        soup = BeautifulSoup(page.content(), "html.parser")
        browser.close()

    jobs, used = [], set()
    for link in soup.find_all("a", href=True):
        container = link.find_parent(["article", "li", "tr", "div"])
        text = container.get_text(" ", strip=True) if container else ""
        match = re.search(r"Job ID:\s*(\d+)", text, re.I)
        if not match:
            continue

        job_id = match.group(1)
        url = link["href"]
        if url.startswith("/"):
            url = "https://hvr-amazon.my.site.com" + url
        if url in used:
            continue
        used.add(url)

        context = _context_for_job(body_text, job_id)
        location = _extract_location(text, context)
        description = text if len(text) >= len(context) else context

        jobs.append(
            Job(
                "amazon_hvr",
                job_id,
                link.get_text(" ", strip=True) or "Amazon job",
                location,
                url,
                description,
            )
        )
    return jobs
