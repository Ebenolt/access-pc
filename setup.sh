#!/bin/bash

sudo apt-get install python3 python3-pip pipenv

pipenv install

sudo apt-get install libmysqlclient-dev
#default-libmysqlclient-dev

echo "Start env with pipenv shell"
echo "Start Server with 'python3 manage.py runserver 8080' or ./start.sh"
