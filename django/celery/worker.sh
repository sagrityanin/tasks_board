#! /bin/sh
rm proj/celery.log
celery -A proj worker -l INFO