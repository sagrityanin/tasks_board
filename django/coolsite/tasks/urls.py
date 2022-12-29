from django.urls import path, re_path

from tasks.views import index, tasks, new_task, about, login, edit_task

urlpatterns = [
    path('', index, name='tasks'),
    path('tasks/<str:category>/', tasks, name='tasks_by_category'),
    path('new-task/', new_task, name='new-task'),
    path('about/', about, name='about'),
    path('login/', login, name='login'),
    path('task/<uuid:task_id>', edit_task, name='task')
]
