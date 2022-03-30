FROM python:3.8

WORKDIR /app/loc/

COPY requirements.txt /app/loc

ENV PIP_NO_CACHE_DIR 1

RUN pip install -r requirements.txt

COPY . .