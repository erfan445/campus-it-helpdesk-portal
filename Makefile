.PHONY: run migrate seed test clean

run:
	python manage.py runserver

migrate:
	python manage.py makemigrations
	python manage.py migrate

seed:
	python manage.py seed_helpdesk

test:
	python manage.py test

clean:
	find . -name "__pycache__" -type d -prune -exec rm -rf {} +
