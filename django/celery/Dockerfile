FROM python:3.11 as build
RUN groupadd --gid 1000 ubuntu && useradd --uid 1000 --gid 1000 -m ubuntu

FROM python:3.11-alpine3.19

WORKDIR /home/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# устанавливаем зависимости
RUN apk update
RUN apk add gcc python3-dev libpq-dev musl-dev gettext
RUN pip install --upgrade pip
COPY . .
COPY --from=build /etc/passwd /etc/
COPY --from=build /etc/group /etc/
RUN chown -R ubuntu:ubuntu /home/app
RUN pip  install -r requirements.txt
RUN chmod +x /home/app/worker.sh
USER ubuntu

ENTRYPOINT ["/home/app/worker.sh"]
