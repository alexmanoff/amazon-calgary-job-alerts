import os
from config import PROFILES
from matcher import matches
from sources.amazon_hiring import fetch_jobs as fetch_hiring
from sources.amazon_hvr import fetch_jobs as fetch_hvr
from storage import load_seen, save_seen
from telegram_sender import send_message

def main() -> None:
    seen = load_seen()
    jobs = []
    for fetcher in (fetch_hiring, fetch_hvr):
        try:
            jobs.extend(fetcher())
        except Exception as exc:
            print(f"Source error: {exc}")

    current = {f"{job.source}:{job.job_id}" for job in jobs}
    initialize = os.getenv("INITIALIZE_ONLY", "false").lower() == "true"

    if initialize or not seen:
        save_seen(seen | current)
        print(f"Initialized with {len(current)} jobs")
        return

    for job in jobs:
        key = f"{job.source}:{job.job_id}"
        if key in seen:
            continue
        for profile in PROFILES:
            ok, reasons = matches(job, profile)
            if not ok:
                continue
            chat_id = os.environ[profile.chat_id_env]
            send_message(
                chat_id,
                f"New Amazon job for {profile.name}\n\n"
                f"{job.title}\nMatched: {', '.join(reasons)}\n\n{job.url}"
            )

    save_seen(seen | current)

if __name__ == "__main__":
    main()
