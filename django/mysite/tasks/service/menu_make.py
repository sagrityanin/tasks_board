

def get_menu(request):
    menu = [{"title": "О сайте", "url_name": "/about"},
            {"title": "Добавить задачу", "url_name": "/new-task"}]
    if str(request.user) == "AnonymousUser":
        menu.append({"title": "Войти", "url_name": "/login"})
        menu.append({"": "#"})
    else:
        menu.append({"title": "Выйти", "url_name": "/logout"})
        menu.append({"title": request.user, "url_name": "#"})
    return menu


def get_sidebar(request):
    sidebar = [{"url": "task-list", "category": "Все задачи с фильтром"},
               {"url": "usertasks", "category": "Все задачи пользователя"},
               {"url": "user-active-tasks", "category": "Задачи пользователя в работе"},
               ]

    return sidebar

def get_context(request):
    context = {"menu": get_menu(request), "title": "Главная страница",
               "sidebar": get_sidebar(request)}
    return context

