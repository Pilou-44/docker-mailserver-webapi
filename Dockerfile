FROM python:3.10-alpine

WORKDIR /app

COPY . /app

RUN pip install -r /app/requirements.txt
