from django.contrib.auth import views as auth_views
from django.urls import path

from tasks.views import index, new_task, about, edit_task, UserTasks, auth_view, logout, \
    UserActiveTasks, TaskList, PcList


urlpatterns = [
    path("", index, name="tasks"),
    path("new-task/", new_task, name="new-task"),
    path("about/", about, name="about"),
    path("task/<uuid:task_id>", edit_task, name="task"),
    path("logout_fun/", logout, name="logout_func"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("usertasks/", UserTasks.as_view(), name="usertasks"),
    path("login/", auth_view, name="login"),
    path("user-active-tasks/", UserActiveTasks.as_view(), name="user_active_tasks"),
    path("task-list/", TaskList.as_view(), name="task_list"),
    path("pc/", PcList.as_view(), name="pc_list")
]
