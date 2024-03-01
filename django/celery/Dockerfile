FROM python:3.11-alpine3.19


WORKDIR /home/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# устанавливаем зависимости
RUN apk update
RUN apk add gcc python3-dev libpq-dev musl-dev gettext
RUN pip install --upgrade pip
COPY . .
RUN pip  install -r requirements.txt
CMD ["/home/app/worker.sh"]
