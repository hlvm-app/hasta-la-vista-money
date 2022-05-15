lint:
	    poetry run flake8 hasta_la_vista_money

dokku:
		git push dokku main

github:
		git push origin main

start:
		@poetry run python manage.py runserver
