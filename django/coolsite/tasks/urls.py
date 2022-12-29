from django.urls import path, re_path

from tasks.views import index, tasks, new_task, about, logout, edit_task

urlpatterns = [
    path('', index, name='tasks'),
    path('tasks/<str:category>/', tasks, name='tasks_by_category'),
    path('new-task/', new_task, name='new-task'),
    path('about/', about, name='about'),
    path('logout/', logout, name='logout'),
    path('task/<uuid:task_id>', edit_task, name='task')
]
