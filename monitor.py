import os

from config import PROFILES
from matcher import matches
from sources.amazon_hvr import fetch_jobs as fetch_hvr
from sources.amazon_jobs import fetch_jobs as fetch_amazon_jobs
from storage import load_seen, save_seen
from telegram_sender import send_message


SOURCES = (
    ("amazon_hvr", fetch_hvr),
    ("amazon_jobs", fetch_amazon_jobs),
)


def key_for(job) -> str:
    return f"{job.source}:{job.job_id}"


def main() -> None:
    seen = load_seen()
    initialize_all = os.getenv("INITIALIZE_ONLY", "false").lower() == "true"
    updated_seen = set(seen)

    for source_name, fetcher in SOURCES:
        try:
            jobs = fetcher()
        except Exception as exc:
            print(f"{source_name} source error: {exc}")
            continue

        print(f"{source_name} jobs found: {len(jobs)}")
        current_keys = {key_for(job) for job in jobs}

        source_already_initialized = any(
            item.startswith(f"{source_name}:") for item in seen
        )

        if initialize_all or not source_already_initialized:
            updated_seen.update(current_keys)
            print(
                f"{source_name}: baseline saved with {len(current_keys)} jobs; "
                "no alerts sent"
            )
            continue

        new_jobs = [job for job in jobs if key_for(job) not in seen]
        print(f"{source_name} new jobs: {len(new_jobs)}")

        for job in new_jobs:
            for profile in PROFILES:
                ok, reasons = matches(job, profile)
                if not ok:
                    continue

                chat_id = os.environ[profile.chat_id_env]
                send_message(
                    chat_id,
                    f"New Amazon job for {profile.name}\n\n"
                    f"{job.title}\n"
                    f"Location: {job.location or 'See job page'}\n"
                    f"Matched: {', '.join(reasons)}\n"
                    f"Source: {job.source}\n\n"
                    f"{job.url}"
                )

        updated_seen.update(current_keys)

    save_seen(updated_seen)


if __name__ == "__main__":
    main()
