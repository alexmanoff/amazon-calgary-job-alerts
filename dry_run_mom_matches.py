from config import MOM
from matcher import matches
from models import Job
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
        ok, reasons = matches(job, MOM)
        if ok:
            matched.append((job, reasons))
        else:
            rejected.append(job)

    print(f"TOTAL JOBS: {len(jobs)}")
    print(f"MOM MATCHES: {len(matched)}")
    print(f"REJECTED: {len(rejected)}")

    print("\nMATCHES — dry run only, NO Telegram messages:")
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
    for job in rejected[:20]:
        print("-" * 64)
        print(f"ID: {job.job_id}")
        print(f"TITLE: {job.title}")
        print(f"LOCATION: {job.location}")


def validate_synthetic_cases():
    print(f"\n{'=' * 64}")
    print("SYNTHETIC MOM FILTER TESTS — NO TELEGRAM")
    print("=" * 64)

    cases = [
        ("Project Manager", "Calgary, AB, CAN", True),
        ("Program Manager", "Calgary, AB, CAN", True),
        ("Project Coordinator", "Calgary, AB, CAN", True),
        ("Operations Manager", "Calgary, AB, CAN", True),
        ("Logistics Coordinator", "Calgary, AB, CAN", True),
        ("Transportation Manager", "Calgary, AB, CAN", True),
        ("Area Manager", "Calgary, AB, CAN", True),
        ("Data Center Facility Manager", "Airdrie, AB, CAN", False),
        ("Software Development Manager", "Calgary, AB, CAN", False),
        ("Warehouse Associate", "Calgary, AB, CAN", False),
        ("Project Manager", "Toronto, ON, CAN", False),
    ]

    failures = 0

    for index, (title, location, expected) in enumerate(cases, start=1):
        job = Job(
            source="synthetic",
            job_id=f"MOM-TEST-{index:02d}",
            title=title,
            location=location,
            url="https://example.invalid/test",
            description="",
        )

        ok, reasons = matches(job, MOM)
        result = "MATCH" if ok else "REJECT"
        expected_text = "MATCH" if expected else "REJECT"
        status = "PASS" if ok == expected else "FAIL"

        print(
            f"[{status}] {title} | {location} | "
            f"result={result} | expected={expected_text} | "
            f"reasons={', '.join(reasons) if reasons else '-'}"
        )

        if ok != expected:
            failures += 1

    print("-" * 64)
    print(f"SYNTHETIC TESTS PASSED: {len(cases) - failures}/{len(cases)}")

    if failures:
        raise SystemExit(f"Synthetic Mom filter validation failed: {failures} case(s)")


def main():
    print("MOM DRY RUN ONLY — NO TELEGRAM MESSAGES WILL BE SENT")
    inspect_source("AMAZON HVR", fetch_hvr)
    inspect_source("AMAZON JOBS", fetch_amazon_jobs)
    validate_synthetic_cases()


if __name__ == "__main__":
    main()
