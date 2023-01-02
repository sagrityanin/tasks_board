from tasks.models import Task


def check_user_in_creator_executer(request, task_id):
    if request.user.person == Task.objects.get(id=task_id).creator or\
            request.user.person == Task.objects.get(id=task_id).executor:
        return True
    return False
