FROM python:3.7

RUN mkdir -p /app
WORKDIR /app

ADD . /app/
RUN pip install -r requirements.txt

ENTRYPOINT ["/app/docker-entrypoint.sh"]
