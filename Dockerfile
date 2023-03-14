# pull official base image
FROM python:3.9.16-alpine

ENV VIRTUAL_ENV=/app/venv \
    PATH=/root/.poetry/bin:$PATH

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.4.0

# set work directory
WORKDIR /app

RUN python -m venv $VIRTUAL_ENV

RUN source /app/venv/bin/activate

USER root

COPY ./requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt && pip install "poetry==$POETRY_VERSION"
RUN apk update && apk add make gettext git --no-cache

COPY . /app/

EXPOSE 8000

CMD ["make", "start"]
