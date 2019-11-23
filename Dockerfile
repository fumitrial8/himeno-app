FROM python:3.5.2-alpine

RUN apk update
RUN apk add vim git
RUN apk add --update openjdk8
RUN apk add musl-dev gcc make g++ file build-base wget freetype-dev libpng-dev world[openblas-dev]
RUN cd /tmp \
    && wget http://www.netlib.org/lapack/lapack-3.8.0.tar.gz \
    && tar zxf lapack-3.8.0.tar.gz \
    && cd lapack-3.8.0/ \
    && cp make.inc.example make.inc \
    && make blaslib \
    && make lapacklib \
    && cp librefblas.a /usr/lib/libblas.a \
    && cp liblapack.a /usr/lib/liblapack.a \
    && cd / \
    && rm -rf /tmp/*
RUN pip install --upgrade pip

ADD requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

WORKDIR /web
RUN git clone https://github.com/fumitrial8/himeno-app.git clock

ENV FLASK_APP /web/clock/app.py
CMD flask run -h 0.0.0.0 -p $PORT
