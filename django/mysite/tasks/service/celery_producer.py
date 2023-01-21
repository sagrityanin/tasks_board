from proj.tasks import send_telegram_message, send_icq_message


def send_telegram(telegram_id: str, message: str) -> bool:
    send_telegram_message(telegram_id, message)


def send_icq(icq_id: str, message: str) -> bool:
    send_icq_message(icq_id, message)
