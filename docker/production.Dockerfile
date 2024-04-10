# This docker file is used for production
# Creating image based on official python3 image
FROM python:3.11.2

ENV PATH="/root/.local/bin:$PATH"

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
# Get the django project into the docker container
RUN curl -sSL https://install.python-poetry.org | python3 - && poetry --version
RUN apt-get install zbar-tools
WORKDIR /app
COPY ../ .


EXPOSE 8000
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements/prod.txt


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
