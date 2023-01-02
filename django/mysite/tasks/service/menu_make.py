

def get_menu(request):
    menu = [{"title": "О сайте", "url_name": "/about"},
            {"title": "Добавить задачу", "url_name": "/new-task"},
            {"title": "Выйти", "url_name": "/logout"},
            {"title": request.user, "url_name": "#"}]
    return menu


def get_sidebar(request):
    sidebar = [{"url": "tasks/all", "category": "Все задачи"},
               {"url": "tasks/создана", "category": "Активные"},
               {"url": "tasks/выполнена", "category": "Выполненные"},
               {"url": "tasks/отклонена", "category": "Отклоненные"},
               {"url": "usertasks", "category": "Задачи пользователя"}
               ]

    return sidebar