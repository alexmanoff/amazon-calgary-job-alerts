import re
from playwright.sync_api import sync_playwright

from models import Job

URL = (
    "https://www.amazon.jobs/en/search?"
    "city=Calgary&country=CAN&county=Alberta&latitude=51.04533&"
    "loc_query=Calgary%2C+AB%2C+Canada&longitude=-114.06301&"
    "radius=50km&region=Alberta&sort=recent"
)

JOB_URL_RE = re.compile(r"amazon\.jobs/(?:en/)?jobs/(\d+)", re.I)
LOCATION_RE = re.compile(
    r"(?:Calgary|Rocky View County|Rocky View|Balzac|Airdrie)"
    r"(?:\s*,\s*(?:AB|Alberta))?(?:\s*,\s*(?:CAN|Canada))?",
    re.I,
)


def _card_text(link) -> str:
    return link.evaluate(
        """el => {
            let node = el;
            for (let i = 0; i < 7 && node; i++, node = node.parentElement) {
                const text = (node.innerText || '').trim();
                if (/Job ID:/i.test(text) && text.length < 3500) return text;
            }
            return (el.parentElement?.innerText || el.innerText || '').trim();
        }"""
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
        if response and response.status != 200:
            browser.close()
            raise RuntimeError(f"amazon.jobs returned HTTP {response.status}")

        page.wait_for_timeout(5000)
        body_text = page.locator("body").inner_text()
        links = page.locator('a[href*="/jobs/"]')

        jobs: list[Job] = []
        seen_ids: set[str] = set()

        for index in range(links.count()):
            link = links.nth(index)
            href = link.get_attribute("href") or ""
            if href.startswith("/"):
                href = "https://www.amazon.jobs" + href

            match = JOB_URL_RE.search(href)
            if not match:
                continue

            job_id = match.group(1)
            if job_id in seen_ids:
                continue
            seen_ids.add(job_id)

            title = (link.inner_text() or "").strip() or "Amazon job"
            card_text = _card_text(link)
            context = _context_for_job(body_text, job_id)
            location = _extract_location(card_text, context)
            description = card_text or context

            jobs.append(
                Job(
                    source="amazon_jobs",
                    job_id=job_id,
                    title=title,
                    location=location,
                    url=href,
                    description=description,
                )
            )

        browser.close()
        return jobs
