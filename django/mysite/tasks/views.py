import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User as UserClass
from django.contrib import auth
from django.db import transaction
from django.http import HttpResponseNotFound, HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django_ratelimit.decorators import ratelimit
from django_ratelimit.exceptions import Ratelimited

import logging

from .models import Task, Person, StatusModel, Pc
from .forms import AddTaskForm, EditTaskForm, LoginUserForm, TaskListForm, PcListForm
from tasks.service.user import check_user_in_creator_executer
from tasks.service.menu_make import get_menu, get_sidebar, get_context
from tasks.service.task import send_note, ListTasksMixin, ListTaskMixin
from tasks.service.pc import ListPcMixin
from tasks.service.logging import LOGGING

logging.config.dictConfig(LOGGING)

status = {"создана": "Активные задачи", "выполнена": "Выполненые задачи",
          "отклонена": "Отклоненные задачи", "all": "Все задачи"}


class PcList(ListPcMixin, LoginRequiredMixin):
    form_class = PcListForm
    model = Pc
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = self.get_context()
        context["title"] = "Список сотрудников и сетевых узлов"
        context["page_url"] = "/pc/"
        return context
    
    def get_query_params(self):
        res = ""
        if field := self.request.GET.get("sort_form"):
            res = f"sort_form={field}"
            if order := self.request.GET.get("order_form"):
                res += f"&order_form={order}"
        if sort_string := self.request.GET.get("sort_form"):
            res += f"&sort_form={sort_string}"
        if order := self.request.GET.get("order_form"):
            res += f"&order_form={order}"
        if search_string := self.request.GET.get("q"):
            res += f"&q={search_string}"
        return res

    def get_queryset(self):
        query = Pc.objects.all()
        if search := self.request.GET.get("q"):
            query = query.filter(Q(title__icontains=search)
                                  | Q(telefon_number__icontains=search)
                                  | Q(ip__icontains=search)
                                  | Q(rdb_user__icontains=search)
                                  | Q(email__icontains=search))
        if sort_field := self.request.GET.get("sort_form"):
            query = query.order_by(sort_field)
        else:
            query = query.order_by("title")
        return query


class TaskList(ListTaskMixin):
    form_class = TaskListForm
    model = Task

    def get_context_data(self, *, object_list=None, **kwargs):
        context = self.get_context()
        context["title"] = "Список задач"
        context["page_url"] = "/task-list/"
        return context


@ratelimit(key="post:username", method=ratelimit.ALL, rate=os.getenv("LOGIN_RARELIMIT"))
def auth_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get("password")
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                auth.login(request, user)
                redirect_uri = request.GET.get("next", "/")
                return redirect(redirect_uri)
        else:
            return HttpResponse("<h2>Invalid username or password</h2>")
    else:
        form = LoginUserForm()
        return render(request, "tasks/login.html", {"form": form, "menu": get_menu(request),
                                                    "sidebar": get_sidebar(request)})


def index(request):
    context = get_context(request)
    return render(request, "tasks/index.html", context=context)


def logout(request):
    context = get_context(request)
    return render(request, "tasks/logout.html", context=context)


class UserTasks(ListTasksMixin):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = self.get_context()
        context["title"] = f"Список задач пользователя {self.request.user.username}"
        context["user"] = self.request.user
        context["page_url"] = "/usertasks"
        return context

    def get_queryset(self):
        tasks = Task.objects.filter(Q(creator=self.request.user.person.id) | Q(
            executor=self.request.user.person.id)).order_by("-time_updated").select_related(
            "creator", "executor").order_by("-status")
        return tasks


class UserActiveTasks(ListTasksMixin):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = self.get_context()
        context["title"] = f"Задачи пользователя {self.request.user.username} в работе"
        context["user"] = self.request.user
        context["page_url"] = "/user-active-tasks/"
        return context

    def get_queryset(self):
        tasks = Task.objects.filter(executor=self.request.user.person.id).filter(
            Q(status=StatusModel.objects.get(title="Создана")) 
            | Q(status=StatusModel.objects.get(title="В работе"))).order_by(
            "-time_updated").select_related("executor", "status").order_by("time_updated")
        return tasks


@ratelimit(key='post:user', method=ratelimit.UNSAFE, rate=os.getenv("NEW_TASK_RARELIMIT"))
@login_required(login_url="/login/")
@transaction.atomic
def edit_task(request, task_id):
    if request.method == "POST":
        instance = Task.objects.get(pk=task_id)
        form = EditTaskForm(request.POST, instance=instance)
        if not check_user_in_creator_executer(request, task_id):
            return HttpResponseForbidden(
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


@ratelimit(key='post:user', method=ratelimit.ALL, rate=os.getenv("NEW_TASK_RARELIMIT"))
@login_required(login_url="/login/")
@transaction.atomic
def new_task(request):
    current_user = request.user
    if request.method == "POST":
        form = AddTaskForm(request.POST, current_user=current_user)
        if form.is_valid():
            form.save()
            task = Task.objects.filter(executor=form.cleaned_data["executor"]).filter(
                status=StatusModel.objects.get(title="Создана")).order_by("-time_updated")[0]
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
    context = get_context(request)
    return render(request, "tasks/about.html", context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


def view_handler403(request, exception=None):
    if isinstance(exception, Ratelimited):
        context = get_context(request)
        context["title"] = "Доступ временно заблокирован"
        return render(request, "tasks/403.html", context=context)
    return HttpResponseForbidden('Sorry Forbidden')
