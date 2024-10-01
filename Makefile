.PHONY: lint
lint:
		@cd ./hasta_la_vista_money && \
			echo "Running ruff check..." && \
			poetry run ruff check . --fix

.PHONY: format
format:
	@cd ./hasta_la_vista_money && \
			echo "Running black..." && \
			poetry run black . && \
			echo "" && \
			echo "Running ruff..." && \
			poetry run ruff format


.PHONY: transprepare
transprepare:
		@poetry run django-admin makemessages

.PHONY: transcompile
transcompile:
		@poetry run django-admin compilemessages

.PHONY: shell
shell:
		@poetry shell

.PHONY: .env
.env:
		@test ! -f .env && cp .env.example .env

.PHONY: install
install: .env
		@poetry install

.PHONY: migrate
migrate:
		poetry run python ./manage.py makemigrations && \
		echo "" && \
		echo "Migrating..." && \
		poetry run python ./manage.py migrate


.PHONY: docker-build
docker-build: .env
		docker compose build

.PHONY: docker-up
docker-up:
		@[ -f ./.env ] && \
			docker compose --env-file ./.env up -d || \
			docker compose up -d

.PHONY: gettext
gettext:
		sudo apt install gettext -y

.PHONY: setup
setup: migrate staticfiles gettext transcompile
		echo "Creating superuser '${DJANGO_SUPERUSER_USERNAME}' with password '${DJANGO_SUPERUSER_PASSWORD}' and email '${DJANGO_SUPERUSER_EMAIL}'" && \
		DJANGO_SUPERUSER_USERNAME="${DJANGO_SUPERUSER_USERNAME}" \
		DJANGO_SUPERUSER_PASSWORD="${DJANGO_SUPERUSER_PASSWORD}" \
		DJANGO_SUPERUSER_EMAIL="${DJANGO_SUPERUSER_EMAIL}" \
		poetry run python ./manage.py createsuperuser --noinput

.PHONY: staticfiles
staticfiles:
		@poetry run python manage.py collectstatic

.PHONY: start
start:
		@poetry run python manage.py runserver

.PHONY: secretkey
secretkey:
		@poetry run python -c 'from django.utils.crypto import get_random_string; print(get_random_string(40))'

.PHONY: test
test:
		DB_USER="postgres" DB_PASSWORD="postgres" poetry run python ./manage.py test -v 2

.PHONY: coverage
coverage:
		@poetry run coverage run manage.py test
		@poetry run coverage xml
		@poetry run coverage report

.PHONY: poetry-export-prod
poetry-export-prod:
		@poetry export -f requirements.txt -o requirements/prod.txt --without-hashes

.PHONY: poetry-export-dev
poetry-export-dev: poetry-export-prod
		@poetry export -f requirements.txt -o requirements/dev.txt --with dev --without-hashes

.PHONY: celery
celery:
		@cd ./app && \
			poetry run celery -A calndr worker --loglevel=info
