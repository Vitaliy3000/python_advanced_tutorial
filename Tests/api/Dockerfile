FROM python:3.9-buster
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY .env .
COPY src src
COPY tests tests
