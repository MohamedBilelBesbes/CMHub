FROM python:3.9

ENV PYTHONUNBUFFERED 1

WORKDIR /app

ADD . /app

COPY requirements.txt /app/

RUN pip install -r /app/requirements.txt

COPY . /app
