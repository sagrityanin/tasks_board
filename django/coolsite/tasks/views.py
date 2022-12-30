from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect
from django import forms
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import *
from .forms import AddTaskForm, EditTaskForm
from tasks.service.user import check_user_in_creator_executer
from tasks.service.task import get_tasks


menu = [{"title": "О сайте", "url_name": "/about"},
        {"title": "Добавить задачу", "url_name": "/new-task"},
        {"title": "Список задач по категориям", "url_name": "/tasks/all"},
        {"title": "Войти", "url_name": "/login"},
        {"title": "Выйти", "url_name": "/logout"}]
status = {"created": "Активные задачи", "executed": "Выполненые задачи",
          "deprecated": "Отклоненные задачи", "all": "Все задачи"}


def index(request):
    return render(request, "tasks/index.html", {"menu": menu, "title": "Главная страница"})


@login_required(login_url="/about/")
def tasks(request, category):

    if category not in status and category != "all":
        return HttpResponse("Заданная категория задач отсутствует")
    tasks = get_tasks(request, category)
    context = {
        "tasks": tasks,
        "menu": menu,
        "title": status[category]
    }
    return render(request, "tasks/tasks.html", context=context)


@login_required(login_url="/about/")
@transaction.atomic
def edit_task(request, task_id):
    if request.method == "POST":
        instance = Task.objects.get(pk=task_id)
        form = EditTaskForm(request.POST, instance=instance)
        if not check_user_in_creator_executer(request, task_id):
            return HttpResponseNotFound(f"<h1>У пользователя: {request.user} нет прав для редактирования этой задачи</h1>")
        if form.is_valid():
            Task.creator = Task.objects.get(pk=task_id).creator
            form.save()
            return redirect("tasks")
    else:
        task = get_object_or_404(Task, pk=task_id)
        form = EditTaskForm(instance=task)
        task_link = f"/task/{task_id}"
    return render(request, "tasks/edit_task.html", {"form": form, "menu": menu, "title": "Изменение задачи",
                                                   "created": task.time_created,
                                                   "updated": task.time_updated, "creator": task.creator.user.username,
                                                    "task_link": task_link})


@login_required(login_url="/about/")
@transaction.atomic
def new_task(request):
    current_user = request.user
    if request.method == "POST":
        form = AddTaskForm(request.POST, current_user=current_user)
        print("post")
        if form.is_valid():
            print(current_user.person.id)
            Task.creator = current_user
            # form.fields["creator"] = forms.CharField(current_user.person.id)
            # print(form.fields["creator"])
            print(form.fields["title"])
            form.save()
            print("task created")
            return redirect("tasks")
    else:
        form = AddTaskForm(current_user=current_user)
    return render(request, "tasks/new_task.html", {"form": form, "menu": menu, "title": "Добавление задачи"})


def about(request):
    return render(request, "tasks/about.html", {"menu": menu, "title": "О сайте"})


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
