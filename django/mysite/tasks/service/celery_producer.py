from proj.tasks import send_telegram_message


def send_telegram(telegram_id: str, message: str) -> bool:
    send_telegram_message(telegram_id, message)
