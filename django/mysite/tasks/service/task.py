from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import FormMixin

import logging
import os

from tasks.forms import TaskListForm
from tasks.models import Task
from tasks.service.menu_make import get_menu, get_sidebar
from .celery_producer import send_telegram


def get_task_name(count: int) -> str:
    if count % 100 != 11 and count % 10 == 1:
        return "задача"
    task_list = [2, 3, 4]
    if count % 10 in task_list and (count % 100) // 10 !=1:
        return "задачи"
    return "задач"

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
    http_method_names = ["get", "post"]
    template_name = "tasks/tasks_by_page.html"
    context_object_name = "task_list"

    def get_context(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = get_menu(self.request)
        context["sidebar"] = get_sidebar(self.request)
        return context


class ListTaskMixin(LoginRequiredMixin, FormMixin, ListView):
    allow_empty = True
    paginate_by = int(os.getenv("TASKS_ON_PAGE_COUNT"))
    http_method_names = ["get"]
    template_name = "tasks/task_list.html"
    context_object_name = "task_list"

    def get(self, request, *args, **kwargs):
        self.request = request
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)
        self.form = TaskListForm
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty and len(self.object_list) == 0:
            raise Http404(u"Empty list and '%(class_name)s.allow_empty' is False."
                          % {'class_name': self.__class__.__name__})

        context = self.get_context_data(object_list=self.object_list, form=self.form)
        context["len"] = len(self.object_list)
        context["task_name"] = get_task_name(len(self.object_list))
        return render(request, "tasks/task_list.html", context=context)

    def get_queryset(self):
        tasks = Task.objects.filter(Q(creator=self.request.user.person) | Q(
            executor=self.request.user.person) | Q(is_visible=True)).select_related(
            "creator", "executor", "status").order_by("-time_updated")
        if self.request.GET.get("creator") is not None and self.request.GET.get("creator") != "":
            tasks = tasks.filter(creator=self.request.GET.get("creator"))
        if self.request.GET.get("executor") is not None and self.request.GET.get("executor") != "":
            tasks = tasks.filter(executor=self.request.GET.get("executor"))
        if self.request.GET.get("status") is not None and self.request.GET.get("status") != "":
            tasks = tasks.filter(status=self.request.GET.get("status"))
        return tasks

    def get_context(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = get_menu(self.request)
        context["sidebar"] = get_sidebar(self.request)
        return context
