# syntax=docker/dockerfile:1
FROM python:3.8-alpine

WORKDIR /app

ADD . /app

RUN pip install --no-cache-dir -r requirements.txt
