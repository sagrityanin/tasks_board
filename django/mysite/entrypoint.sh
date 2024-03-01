#!/bin/sh

python manage.py makemigrations
python manage.py makemigrations tasks
python manage.py migrate

echo "Start app"
exec gunicorn coolsite.wsgi --bind 0.0.0.0:8000 --workers 2
echo "App started"

exec "$@
