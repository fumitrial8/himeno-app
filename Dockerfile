FROM python:3.5.2-alpine

RUN apk update
RUN apk add vim git

ADD requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
