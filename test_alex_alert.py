import os

from config import ALEX
from matcher import matches
from models import Job
from telegram_sender import send_message


def main() -> None:
    test_job = Job(
        source="test",
        job_id="TEST-ALEX-001",
        title="Amazon Fulfillment Associate",
        location="Calgary, AB, CAN",
        url="https://www.amazon.jobs/",
        description="Entry-level fulfillment warehouse associate position in Calgary.",
    )

    ok, reasons = matches(test_job, ALEX)
    print(f"Matcher result: {ok}")
    print(f"Matched by: {', '.join(reasons) if reasons else '(none)'}")

    if not ok:
        raise RuntimeError("Alex test vacancy did not pass the matcher")

    send_message(
        os.environ["ALEX_CHAT_ID"],
        "🧪 TEST — Amazon Job Alert\n\n"
        f"{test_job.title}\n"
        f"Location: {test_job.location}\n"
        f"Matched: {', '.join(reasons)}\n\n"
        "This is a test alert only. No real vacancy was saved or modified.",
    )
    print("Alex end-to-end test alert sent successfully")


if __name__ == "__main__":
    main()
