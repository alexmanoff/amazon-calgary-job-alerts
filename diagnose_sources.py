from config import ALEX, LOCATIONS
from matcher import matches
from sources.amazon_hiring import fetch_jobs as fetch_hiring
from sources.amazon_hvr import fetch_jobs as fetch_hvr


def inspect_source(name, fetcher):
    print(f"\n{'=' * 60}")
    print(f"SOURCE: {name}")
    print("=" * 60)

    try:
        jobs = fetcher()
    except Exception as exc:
        print(f"ERROR: {exc}")
        return

    print(f"TOTAL JOBS FOUND: {len(jobs)}")

    local_jobs = [
        job for job in jobs
        if any(location in job.text for location in LOCATIONS)
    ]

    print(f"CALGARY / ROCKY VIEW / BALZAC: {len(local_jobs)}")

    alex_matches = []

    for job in local_jobs:
        ok, reasons = matches(job, ALEX)

        if ok:
            alex_matches.append((job, reasons))

    print(f"ALEX MATCHES: {len(alex_matches)}")

    print("\nLOCAL JOB SAMPLES:")

    for job in local_jobs[:10]:
        print("-" * 40)
        print(f"ID: {job.job_id}")
        print(f"TITLE: {job.title}")
        print(f"LOCATION: {job.location}")
        print(f"URL: {job.url}")

    print("\nALEX MATCHES:")

    for job, reasons in alex_matches[:10]:
        print("-" * 40)
        print(f"ID: {job.job_id}")
        print(f"TITLE: {job.title}")
        print(f"MATCHED BY: {', '.join(reasons)}")
        print(f"URL: {job.url}")


def main():
    inspect_source("AMAZON HIRING", fetch_hiring)
    inspect_source("AMAZON HVR", fetch_hvr)


if __name__ == "__main__":
    main()
