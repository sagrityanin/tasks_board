from django.db.models import Q

from tasks.models import Task, User


def get_tasks(request, category):
    if category == "all":
        tasks = Task.objects.filter(Q(creator=request.user.person) | Q(executor=request.user.person) |
                                    Q(is_visible=True)).order_by("-time_updated")
    else:
        tasks = Task.objects.filter(Q(creator=request.user.person) | Q(executor=request.user.person) |
                                    Q(is_visible=True)).filter(status=category).order_by("-time_updated")
    return tasks


def send_note(title, executor):
    print(title, executor.user.username)
