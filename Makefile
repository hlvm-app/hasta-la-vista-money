.PHONY: lint
lint:
	@poetry run flake8 hasta_la_vista_money config --exclude=migrations

.PHONY: format
format:
	echo "Running black..." && \
	poetry run black . && \
	echo "" && \
	echo "Running ruff..." && \
	poetry run ruff --fix


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


.PHONY: build
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
	@poetry run coverage run --source='.' manage.py test

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
	@poetry run celery -A hasta_la_vista_money worker --loglevel=info
