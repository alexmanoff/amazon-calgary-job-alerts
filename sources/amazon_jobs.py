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
    r"(?:Calgary|Rocky View County|Rocky View|Balzac|Airdrie)\s*,?\s*(?:AB|Alberta)?\s*,?\s*(?:CAN|Canada)?",
    re.I,
)


def _card_text(link) -> str:
    return link.evaluate(
        """el => {
            const card = el.closest('li, article, [data-test*="job"], [class*="job"]');
            if (card) return (card.innerText || '').trim();
            let node = el;
            for (let i = 0; i < 4 && node; i++, node = node.parentElement) {
                const text = (node.innerText || '').trim();
                if (/Job ID:/i.test(text) && text.length < 2500) return text;
            }
            return (el.parentElement?.innerText || el.innerText || '').trim();
        }"""
    )


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

            location_match = LOCATION_RE.search(card_text)
            location = location_match.group(0).strip() if location_match else ""

            jobs.append(
                Job(
                    source="amazon_jobs",
                    job_id=job_id,
                    title=title,
                    location=location,
                    url=href,
                    description=card_text,
                )
            )

        browser.close()
        return jobs
