FROM python:3.11.1

WORKDIR /microservice

COPY ./requirements.txt /microservice/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /microservice/requirements.txt

COPY ./app /microservice/app

WORKDIR /microservice/app

CMD ["gunicorn", "-c", "gunicorn_conf.py", "main:app" ]