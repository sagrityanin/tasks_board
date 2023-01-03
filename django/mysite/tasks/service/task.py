from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import ListView

import logging
import os

from tasks.models import Task
from tasks.service.menu_make import get_menu, get_sidebar
from .celery_producer import send_telegram


def get_tasks(request, category: str):
    if category == "all":
        tasks = Task.objects.filter(Q(creator=request.user.person) | Q(executor=request.user.person) | Q(
            is_visible=True)).order_by("-time_updated")
    else:
        tasks = Task.objects.filter(Q(creator=request.user.person) | Q(executor=request.user.person) | Q(
            is_visible=True)).filter(status=category).order_by("-time_updated")
    return tasks


def send_note(title, executor, task):
    send_text = f"Для пользователя {executor.user.username} была создана задача \n {title} " \
                f"\n {os.getenv('URL')}/task/{task.id}"
    if executor.note_chanal == "telegramm":
        send_telegram(executor.telegramm_id, send_text)
        logging.info(f"Send telegram note to {executor.user.username}")

    else:
        logging.info(f"Nowhere to send note for {executor.user.username}")


class ListTasksMixin(LoginRequiredMixin, ListView):
    allow_empty = True
    paginate_by = int(os.getenv("TASKS_ON_PAGE_COUNT"))
    model = Task
    http_method_names = ["get"]
    template_name = "tasks/tasks_by_page.html"
    context_object_name = "task_list"

    def get_context(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = get_menu(self.request)
        context["sidebar"] = get_sidebar(self.request)
        return context
