FROM python:3.11


WORKDIR /home/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# устанавливаем зависимости
RUN apt update
RUN apt install -y gcc python3-dev libpq-dev musl-dev gettext
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip  install -r requirements.txt
