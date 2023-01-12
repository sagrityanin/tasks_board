from datetime import datetime
import logging
import requests
import os

from .celery import app


@app.task(max_retries=10, autoretry_for=(Exception,), retry_backoff=10)
def send_telegram_message(telegram_id: str, message: str) -> bool:
    with open("proj/celery.log", "a") as f:
        f.write(telegram_id + ", " + message + "\n" + str(datetime.now()))
        url = "https://api.telegram.org/bot" + os.getenv("TELEGRAMM_TOKEN") + "/sendMessage"
        r = requests.post(url, data={
            "chat_id": telegram_id,
            "text": message
        })
        logging.info(r.content)
        logging.info(f"Send telegram message {message} to {telegram_id}")
        return True


@app.task
def file_write(text: str) -> bool:
    with open("res.txt", "a") as f:
        f.write(text)
        return True
