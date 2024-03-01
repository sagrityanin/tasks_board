#! /bin/sh
if [ -e proj/celery.log ]
then
    rm proj/celery.log
fi

exec celery -A proj worker -l INFO