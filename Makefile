lint:
	    @poetry run flake8 hasta_la_vista_money bot --exclude=migrations

export-requirements:
		@poetry export -f requirements.txt --output requirements.txt --without-hashes

transprepare:
		@poetry run django-admin makemessages

transcompile:
		@poetry run django-admin compilemessages

shell:
		@poetry shell

.env:
		@test ! -f .env && cp .env.example .env

migrate:
		@poetry run python manage.py migrate

migrations:
		@poetry run python manage.py makemigrations
		
install: .env
		@poetry install

docker-install: .env
		docker-compose build

docker-start:
		docker-compose up
		
setup: migrations migrate transcompile
		@echo Create a super user
		@poetry run python manage.py createsuperuser

dokku:
		git push dokku main

github:
		git push origin main

start: setup 
		@poetry run python manage.py runserver
		
secretkey:
		@poetry run python -c 'from django.utils.crypto import get_random_string; print(get_random_string(40))'

test:
		@poetry run python manage.py test

coverage:
		@poetry run coverage run manage.py test
		@poetry run coverage xml
		@poetry run coverage report

