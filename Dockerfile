FROM python:3.5.2-alpine

RUN apk update
RUN apk add vim git

ADD requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

WORKDIR /web
RUN git clone https://github.com/nanakenashi/image_clock.git clock

ENV FLASK_APP /web/clock/app.py
CMD flask run -h 0.0.0.0 -p $PORT
