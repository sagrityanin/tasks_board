import os

from celery import Celery

app = Celery('proj',
             broker=f"redis://{os.getenv('CELERY_REDIS_HOST')}:{os.getenv('CELERY_REDIS_PORT')}/{os.getenv('CELERY_REDIS_DB')}",
             # backend='rpc://',
             include=['proj.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()
