import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User as UserClass
from django.contrib import auth
from django.db import transaction
from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.db.models import Q
from django_ratelimit.decorators import ratelimit
import logging

from .models import Task, Person
from .forms import AddTaskForm, EditTaskForm, LoginUserForm
from tasks.service.user import check_user_in_creator_executer
from tasks.service.menu_make import get_menu, get_sidebar
from tasks.service.task import send_note, get_tasks, ListTasksMixin
from tasks.service.logging import LOGGING

logging.config.dictConfig(LOGGING)

status = {"создана": "Активные задачи", "выполнена": "Выполненые задачи",
          "отклонена": "Отклоненные задачи", "all": "Все задачи"}


@ratelimit(key="post:username", method=ratelimit.ALL, rate="23/m")
def auth_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        # username = request.POST.get('username')
        username = UserClass.objects.get(email=email).username
        password = request.POST.get("password")
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return render(request, "tasks/index.html", {"menu": get_menu(request), "title": "Главная страница",
                                                            "sidebar": get_sidebar(request)})
        else:
            return HttpResponse("<h2>Invalid username or password</h2>")
    else:
        form = LoginUserForm()
        return render(request, "tasks/login.html", {"form": form, "menu": get_menu(request),
                                                       "sidebar": get_sidebar(request)})

def index(request):
    context = {"menu": get_menu(request), "title": "Главная страница",
                                                "sidebar": get_sidebar(request)}
    return render(request, "tasks/index.html", context=context)


class Tasks(ListTasksMixin):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = self.get_context()
        context["title"] = "Список задач"
        context["page_url"] = "/tasks/" + self.kwargs["category"]
        return context

    def get_queryset(self):
        if self.kwargs["category"] == "all":
            tasks = Task.objects.filter(Q(creator=self.request.user.person) | Q(
                executor=self.request.user.person) | Q(is_visible=True)).order_by("-time_updated")
        else:
            tasks = Task.objects.filter(Q(creator=self.request.user.person) | Q(
                executor=self.request.user.person) | Q(is_visible=True)).filter(status=self.kwargs["category"]
                                                                                ).order_by("-time_updated")
        return tasks


class UserTasks(ListTasksMixin):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = self.get_context()
        context["title"] = f"Список задач пользователя {self.request.user.username}"
        context["user"] = self.request.user
        context["page_url"] = "/usertasks"
        return context

    def get_queryset(self):
        tasks = Task.objects.filter(Q(creator=self.request.user.person.id) | Q(
            executor=self.request.user.person.id)).order_by("-time_updated")
        return tasks


@ratelimit(key='post:username', method=ratelimit.ALL, rate='100/h')
@login_required(login_url="/login/")
@transaction.atomic
def edit_task(request, task_id):
    if request.method == "POST":
        instance = Task.objects.get(pk=task_id)
        form = EditTaskForm(request.POST, instance=instance)
        if not check_user_in_creator_executer(request, task_id):
            return HttpResponseNotFound(
                f"<h1>У пользователя: {request.user} нет прав для редактирования этой задачи</h1>")
        if form.is_valid():
            form.save()
            logging.info(f"{request.user} made task")
            context = {"menu": get_menu(request), "title": "Главная страница",
                       "sidebar": get_sidebar(request), "executor": form.cleaned_data["executor"],
                       "task": form.cleaned_data["title"], "action": "изменена"}
            return render(request, "tasks/index.html", context=context)
    else:
        task = get_object_or_404(Task, pk=task_id)
        form = EditTaskForm(instance=task)
        task_link = f"/task/{task_id}"
        if isinstance(task.creator, Person):
            username = task.creator.user.username
        elif isinstance(task.creator, UserClass):
            username = task.creator.username
    return render(request, "tasks/edit_task.html", {"form": form, "menu": get_menu(request),
                                                    "title": "Изменение задачи",
                                                    "created": task.time_created,
                                                    "updated": task.time_updated, "creator": username,
                                                    "task_link": task_link, "sidebar": get_sidebar(request)})


@ratelimit(key='post:username', method=ratelimit.ALL, rate='10/h')
@login_required(login_url="/login/")
@transaction.atomic
def new_task(request):
    current_user = request.user
    if request.method == "POST":
        form = AddTaskForm(request.POST, current_user=current_user)
        if form.is_valid():
            form.save()
            task = Task.objects.filter(executor=form.cleaned_data["executor"]).filter(
                status="создана").order_by("-time_updated")[0]
            send_note(form.cleaned_data["title"], form.cleaned_data["executor"], task)
            logging.info(f"{current_user} made task")
            context = {"menu": get_menu(request), "title": "Главная страница",
                       "sidebar": get_sidebar(request), "executor": form.cleaned_data["executor"],
                       "task": form.cleaned_data["title"], "action": "создана"}
            return render(request, "tasks/index.html", context=context)
    else:
        form = AddTaskForm(current_user=current_user)
    return render(request, "tasks/new_task.html", {"form": form, "menu": get_menu(request),
                                                   "title": "Добавление задачи",
                                                   "sidebar": get_sidebar(request)})


def about(request):
    return render(request, "tasks/about.html", {"menu": get_menu(request), "title": "О сайте"})


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
