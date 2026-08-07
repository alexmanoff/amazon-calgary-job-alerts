import os

from telegram_sender import send_message


def main():
    recipients = [
        ("Alex", os.environ["ALEX_CHAT_ID"]),
        ("Mom", os.environ["MOM_CHAT_ID"]),
    ]

    for name, chat_id in recipients:
        send_message(
            chat_id,
            f"✅ Amazon Job Monitor test\n\n"
            f"Profile: {name}\n"
            f"Telegram notifications are working."
        )
        print(f"Test message sent to {name}")


if __name__ == "__main__":
    main()
