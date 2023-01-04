#!/bin/bash

echo "Start app"
gunicorn coolsite.wsgi --bind 0.0.0.0:8000 --workers 2
echo "App started"

exec "$@
