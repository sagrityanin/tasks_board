# ПРОЕКТ Tasks board создан для выполнения следующих задач
- Создание задач
- Фиксирование выполнения задач
- Просмотр активных, выполненных и отклоненных задач

## СТРУКТУРА ПРОЕКТ
### Проект развернут в docker-compose и состоит из следующих модулей
- nginx - взаимодействует с пользователем
- task_aap - Django-приложение осуществляет обработку запросов пользователей и 
    создане Selery-задач для уведомления пользователей
- task_db - Postgresql, база данных проекта
- celery-redis - Selery-brocker
- celery_worker - берет задачи из брокера и выполняет их(уведомления пользователей)

### ЗАПУСК ПРОЕКТА
После развертывания проекта нужно:
- настроить nginx: настройка доменного имени. сертификатов ssl, портов
- создать суперпользователя(docker compose exec task_app python manage.py createsuperuser)
- настроить пользователей в админпанели Django
