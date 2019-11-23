FROM python:3.5.2-alpine

RUN apk update
RUN apk add vim git
RUN apt-get update && apt-get install -y \
    default-jdk \
RUN pip install --upgrade pip

ADD requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

WORKDIR /web
RUN git clone https://github.com/fumitrial8/himeno-app.git clock

ENV FLASK_APP /web/clock/app.py
CMD flask run -h 0.0.0.0 -p $PORT
