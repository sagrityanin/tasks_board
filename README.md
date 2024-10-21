# ПРОЕКТ Tasks board создан для выполнения следующих задач
- Создание задач
- Фиксирование выполнения задач
- Просмотр активных, выполненных и отклоненных задач

## СТРУКТУРА ПРОЕКТ
### Проект развернут в docker-compose и состоит из следующих модулей
- nginx - взаимодействует с пользователем
- task-app - Django-приложение осуществляет обработку запросов пользователей и 
    создане Selery-задач для уведомления пользователей
- task_db - Postgresql, база данных проекта
- celery-redis - Celery-brocker
- celery_worker - берет задачи из брокера и выполняет их(уведомления пользователей)

### ЗАПУСК ПРОЕКТА
После развертывания проекта нужно:
- настроить nginx: настройка доменного имени. сертификатов ssl, портов
- создать суперпользователя(docker compose exec task-app python manage.py createsuperuser)
- настроить пользователей в админпанели Django

### Подготовка для k8s
docker build ./nginx -t sagrityanin4/tasks_board_proxy:1.0
docker push sagrityanin4/tasks_board_proxy:1.0
docker build ./django/celery -t sagrityanin4/tasks_board_worker:1.0
docker push sagrityanin4/tasks_board_worker:1.0
docker build ./django -t sagrityanin4/tasks_board_app:1.2
docker push sagrityanin4/tasks_board_app:1.2

### Миграции
- docker build ./django -f ./django/Dockerfile_init -t sagrityanin4/tasks_board_init:1.2
- docker compose -f docker-compose.migration.yaml up -d
- docker compose -f docker-compose.migration.yaml logs task-app
- docker push sagrityanin4/tasks_board_init:1.2
