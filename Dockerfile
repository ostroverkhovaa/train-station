FROM python:3.12-alpine3.18
LABEL maintainer="skubakovaa@gmail.com"

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN adduser -D -h /app my-user \
    && chown -R my-user /app

USER my-user
