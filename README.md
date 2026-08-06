# Amazon Calgary Job Alerts

One GitHub Actions workflow checks two Amazon hiring sites and sends matching
vacancies to Alex and Mom in separate private Telegram chats.

## Secrets
- TELEGRAM_BOT_TOKEN
- ALEX_CHAT_ID
- MOM_CHAT_ID

## First run
Run the workflow manually with `initialize_only` enabled. This records current
vacancies without sending them as new alerts.
