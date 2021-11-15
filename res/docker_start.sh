#!/bin/sh
cd /home/access-pc/
pipenv run python3 manage.py makemigrations
pipenv run python3 manage.py migrate
pipenv run /bin/sh /home/access-pc/start.sh