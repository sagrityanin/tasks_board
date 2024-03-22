#!/bin/sh

python manage.py makemigrations
python manage.py makemigrations tasks
python manage.py migrate
