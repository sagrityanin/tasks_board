from django.contrib.auth import views as auth_views
from django.urls import path

from tasks.views import index, new_task, about, edit_task, Tasks, UserTasks, auth_view, logout

urlpatterns = [
    path("", index, name="tasks"),
    path("new-task/", new_task, name="new-task"),
    path("about/", about, name="about"),
    path("task/<uuid:task_id>", edit_task, name="task"),
    path("log_old/", auth_views.LoginView.as_view(template_name="tasks/login.html"), name="log_old",
         kwargs={'redirect_authenticated_user': True}),
    path("logout_fun/", logout, name="logout_func"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("tasks/<str:category>/", Tasks.as_view(), name="tasks_by_category"),
    path("usertasks/", UserTasks.as_view(), name="usertasks"),
    path("login/", auth_view, name="login"),
]
