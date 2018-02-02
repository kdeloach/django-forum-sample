.PHONY: all

all: env/ db.sqlite3
	env/bin/python manage.py runserver

env/: requirements.txt
	virtualenv env/
	env/bin/pip install -r requirements.txt

db.sqlite3:
	env/bin/python manage.py migrate
	env/bin/python manage.py loaddata forum/apps/website/fixtures/initial.json
