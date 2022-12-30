# Запуск проекта
docker compose up -d

# Создание суперпользователя
docker compose exec task_app python manage.py createsuperuser
