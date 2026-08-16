import os
from datetime import datetime, timezone

from telegram_sender import send_message


def main() -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    send_message(
        os.environ["ALEX_CHAT_ID"],
        "✅ Amazon Job Monitor is working\n\n"
        "Monthly health check: the GitHub workflow is still active.\n"
        f"Checked at: {now}",
    )
    print("Monthly heartbeat sent to Alex")


if __name__ == "__main__":
    main()
