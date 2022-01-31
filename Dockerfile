# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster

RUN apt-get update \
  && apt-get install -y python3-pip  python3-dev \
  && pip3 install --upgrade pip

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=5000"]
