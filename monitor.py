import os
from config import PROFILES
from matcher import matches
from sources.amazon_hvr import fetch_jobs as fetch_hvr
from storage import load_seen, save_seen
from telegram_sender import send_message


def main() -> None:
    seen = load_seen()

    try:
        jobs = fetch_hvr()
    except Exception as exc:
        print(f"HVR source error: {exc}")
        raise

    print(f"HVR jobs found: {len(jobs)}")

    current = {f"{job.source}:{job.job_id}" for job in jobs}
    initialize = os.getenv("INITIALIZE_ONLY", "false").lower() == "true"

    if initialize or not seen:
        save_seen(seen | current)
        print(f"Initialized with {len(current)} jobs")
        return

    new_jobs = [job for job in jobs if f"{job.source}:{job.job_id}" not in seen]
    print(f"New HVR jobs: {len(new_jobs)}")

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
                f"Matched: {', '.join(reasons)}\n\n"
                f"{job.url}"
            )

    save_seen(seen | current)


if __name__ == "__main__":
    main()
