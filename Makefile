lint:
	    @poetry run flake8 hasta_la_vista_money users receipts bot --exclude=migrations

export-requirements:
		@poetry export -f requirements.txt --output requirements.txt --without-hashes

dokku:
		git push dokku main

github:
		git push origin main

start:
		@poetry run python manage.py runserver

test:
		@poetry run python manage.py test

coverage:
		@poetry run coverage run manage.py test
		@poetry run coverage xml
		@poetry run coverage report

install:
		@poetry install