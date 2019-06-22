FROM python:3.7-alpine

MAINTAINER Pawel Maciejski <pawel.maciejski@gmail.com>

RUN apk add --upgrade --no-cache \
    bash \
    curl && \
    apk add --no-cache --virtual .build-dependencies \
    build-base \
    libxml2-dev \
    libxslt-dev \
    linux-headers \
    python3-dev

WORKDIR /usr/src/app

COPY requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt && rm /tmp/requirements.txt

RUN apk del .build-dependencies

COPY . .

CMD [ "python", "./run.py" ]
