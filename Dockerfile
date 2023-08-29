FROM python:3.7-slim

RUN mkdir -p /app
WORKDIR /app

ADD . /app/
RUN pip install -r requirements.txt

