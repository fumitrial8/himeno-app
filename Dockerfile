FROM python:3.5.2-alpine

RUN apk update
RUN apk add vim git
RUN apk add --update openjdk8
RUN apk add musl-dev gcc make g++ file
ENV BLAS /usr/local/lib/libfblas.a
ENV LAPACK /usr/local/lib/liblapack.a
RUN apk add --update musl python3-dev freetype-dev make g++ gfortran wget && \
    cd /tmp && wget -q --no-check-certificate \
        https://raw.githubusercontent.com/catholabs/docker-alpine/master/blas.sh \
        https://raw.githubusercontent.com/catholabs/docker-alpine/master/blas.tgz \
        https://raw.githubusercontent.com/catholabs/docker-alpine/master/lapack.sh \
        https://raw.githubusercontent.com/catholabs/docker-alpine/master/lapack.tgz \
        https://raw.githubusercontent.com/catholabs/docker-alpine/master/make.inc \
        http://dl.ipafont.ipa.go.jp/IPAexfont/ipaexg00301.zip && \
    sh ./blas.sh && sh ./lapack.sh && \
    cp ~/src/BLAS/libfblas.a /usr/local/lib && \
    cp ~/src/lapack-3.5.0/liblapack.a /usr/local/lib && \
RUN pip install --upgrade pip

ADD requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

WORKDIR /web
RUN git clone https://github.com/fumitrial8/himeno-app.git clock

ENV FLASK_APP /web/clock/app.py
CMD flask run -h 0.0.0.0 -p $PORT
