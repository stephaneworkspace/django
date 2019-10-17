# https://runnable.com/docker/python/dockerize-your-django-application not use in production
FROM python:3.7

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

ADD . /home

WORKDIR /home

ENV DJANGO_SETTINGS_MODULE=home.deploy 

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]