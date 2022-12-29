from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect
from django import forms
from .models import *
from .forms import AddTaskForm, EditTaskForm
from django.shortcuts import get_object_or_404
from django.contrib import messages

menu = [{'title': "О сайте", 'url_name': '/about'},
        {'title': "Добавить задачу", 'url_name': '/new-task'},
        {'title': "Список задач по категориям", 'url_name': '/tasks/all'},
        {'title': "Выйти", 'url_name': '/logout'}]
status = {"created": "Активные задачи", "executed": "Выполненые задачи",
          "deprecated": "Отклоненные задачи", "all": "Все задачи"}


# class TaskForm(forms.ModelForm):
#     class Meta:
#         model = Task
#         fields = ("title", 'note', 'is_visible', 'status', 'creator', 'executor')


def index(request):
    return render(request, 'tasks/index.html', {'menu': menu, 'title': 'Главная страница'})


def tasks(request, category):
    if category == "all":
        tasks = Task.objects.all().order_by("-time_updated")
    elif category not in status:
        return HttpResponse("Заданная категория задач отсутствует")
    else:
        tasks = Task.objects.filter(status=category).order_by("-time_updated")
    context = {
        'tasks': tasks,
        'menu': menu,
        'title': status[category]
    }
    return render(request, 'tasks/tasks.html', context=context)


def edit_task(request, task_id):
    if request.method == 'POST':
        instance = Task.objects.get(pk=task_id)
        form = EditTaskForm(request.POST, instance=instance)
        if form.is_valid():
            Task.creator = Task.objects.get(pk=task_id).creator
            form.save()
            return redirect('tasks')
    else:
        task = get_object_or_404(Task, pk=task_id)
        form = EditTaskForm(instance=task)
        task_link = f"/task/{task_id}"
    return render(request, 'tasks/edit_task.html', {'form': form, 'menu': menu, 'title': 'Изменение задачи',
                                                   'created': task.time_created,
                                                   'updated': task.time_updated, "creator": task.creator.name,
                                                    'task_link': task_link})


def new_task(request):
    if request.method == 'POST':
        form = AddTaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks')
    else:
        form = AddTaskForm()
    return render(request, 'tasks/new_task.html', {'form': form, 'menu': menu, 'title': 'Добавление задачи'})


def about(request):
    return render(request, 'tasks/about.html', {'menu': menu, 'title': 'О сайте'})


def logout(request):
    return HttpResponse("Здесь будет logout")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')