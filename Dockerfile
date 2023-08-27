FROM python:3.7

RUN mkdir -p /app
WORKDIR /app

ADD . /app/
#ADD requirements.txt /app/
#ADD constraints.txt /app/
RUN pip install -r requirements.txt


