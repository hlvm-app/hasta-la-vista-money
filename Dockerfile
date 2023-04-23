# pull official base image
FROM python:3.10.11-alpine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.4.0

# set work directory
WORKDIR /app

COPY requirements.txt /app/

COPY . /app/

RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt && pip install --no-cache-dir "poetry==$POETRY_VERSION"
RUN apk --no-cache add make
