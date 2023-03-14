# pull official base image
FROM python:3.9.16-alpine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.4.0

# set work directory
WORKDIR /app

COPY requirements.txt /app/

COPY . /app/

RUN pip install --upgrade pip && pip install -r requirements.txt
