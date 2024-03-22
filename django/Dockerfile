FROM python:3.11 as build
RUN groupadd --gid 1000 ubuntu && useradd --uid 1000 --gid 1000 -m ubuntu

FROM python:3.11-alpine3.19

WORKDIR /home/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update
RUN apk add gcc python3-dev libpq-dev musl-dev gettext
RUN pip install --upgrade pip
COPY ./requirements.txt .

RUN pip  install -r requirements.txt

COPY ./mysite /home/app
COPY ./celery/proj ./proj
COPY --from=build /etc/passwd /etc/
COPY --from=build /etc/group /etc/

#CMD ["gunicorn", "coolsite.wsgi", "--bind 0.0.0.0:8000", "--workers 2"]
RUN chmod +x /home/app/entrypoint.sh
RUN chmod +x /home/app/migration.sh
RUN chown -R ubuntu:ubuntu /home/app
USER ubuntu
ENTRYPOINT ["/home/app/entrypoint.sh"]
