from django.contrib.auth import views as auth_views
from django.urls import path, re_path

from tasks.views import index, new_task, about, edit_task, Tasks, UserTasks

urlpatterns = [
    path("", index, name="tasks"),
    path("new-task/", new_task, name="new-task"),
    path("about/", about, name="about"),
    path("task/<uuid:task_id>", edit_task, name="task"),
    path("login/", auth_views.LoginView.as_view(template_name="tasks/login.html"), name="login",
         kwargs={'redirect_authenticated_user': True}),
    path("logout/", auth_views.LogoutView.as_view(template_name="tasks/logout.html"), name="logout"),
    path("tasks/<str:category>/", Tasks.as_view(), name="tasks_by_category"),
    path("usertasks/", UserTasks.as_view(), name="usertasks")
]
