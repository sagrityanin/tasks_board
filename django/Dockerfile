FROM python:3.11

WORKDIR /home/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update
RUN apt install -y gcc python3-dev libpq-dev musl-dev gettext
RUN pip install --upgrade pip
COPY ./requirements.txt .

RUN pip  install -r requirements.txt

COPY ./celery/proj ./proj

COPY ./mysite .

#CMD ["gunicorn", "coolsite.wsgi", "--bind 0.0.0.0:8000", "--workers 2"]
CMD chmod +x /home/flask/enterypiont.sh
ENTRYPOINT ["/home/app/entrypoint.sh"]
