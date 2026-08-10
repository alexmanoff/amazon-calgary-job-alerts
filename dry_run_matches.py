from config import ALEX
from matcher import matches
from sources.amazon_hvr import fetch_jobs as fetch_hvr
from sources.amazon_jobs import fetch_jobs as fetch_amazon_jobs


def inspect_source(name, fetcher):
    print(f"\n{'=' * 64}")
    print(f"SOURCE: {name}")
    print("=" * 64)

    try:
        jobs = fetcher()
    except Exception as exc:
        print(f"SOURCE ERROR: {exc}")
        return

    matched = []
    rejected = []

    for job in jobs:
        ok, reasons = matches(job, ALEX)
        if ok:
            matched.append((job, reasons))
        else:
            rejected.append(job)

    print(f"TOTAL JOBS: {len(jobs)}")
    print(f"ALEX MATCHES: {len(matched)}")
    print(f"REJECTED: {len(rejected)}")

    print("\nMATCHES — these WOULD trigger Telegram if they were new:")
    if not matched:
        print("(none)")

    for job, reasons in matched:
        print("-" * 64)
        print(f"ID: {job.job_id}")
        print(f"TITLE: {job.title}")
        print(f"LOCATION: {job.location}")
        print(f"MATCHED BY: {', '.join(reasons)}")
        print(f"URL: {job.url}")

    print("\nREJECTED SAMPLES:")
    for job in rejected[:15]:
        print("-" * 64)
        print(f"ID: {job.job_id}")
        print(f"TITLE: {job.title}")
        print(f"LOCATION: {job.location}")


def main():
    print("DRY RUN ONLY — NO TELEGRAM MESSAGES WILL BE SENT")
    inspect_source("AMAZON HVR", fetch_hvr)
    inspect_source("AMAZON JOBS", fetch_amazon_jobs)


if __name__ == "__main__":
    main()
