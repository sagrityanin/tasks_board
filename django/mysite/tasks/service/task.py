import os

from django.db.models import Q
import logging
from tasks.models import Task, User
from .celery_producer import send_telegram


def get_tasks(request, category):
    if category == "all":
        tasks = Task.objects.filter(Q(creator=request.user.person) | Q(executor=request.user.person) |
                                    Q(is_visible=True)).order_by("-time_updated")
    else:
        tasks = Task.objects.filter(Q(creator=request.user.person) | Q(executor=request.user.person) |
                                    Q(is_visible=True)).filter(status=category).order_by("-time_updated")
    return tasks


def send_note(title, executor, task):
    send_text = f"Для пользователя {executor.user.username} была создана задача \n {title} " \
                f"\n {os.getenv('URL')}/task/{task.id}"
    if executor.note_chanal == "telegramm":
        send_telegram(executor.telegramm_id, send_text)
        logging.info(f"Send telegram note to {executor.user.username}")

    else:
        logging.info(f"Nowhere to send note for {executor.user.username}")
