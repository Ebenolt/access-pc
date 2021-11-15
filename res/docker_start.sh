#!/bin/sh
echo "STEP 1"
cd /home/access-pc/
echo "STEP 2"
pipenv run python3 manage.py makemigrations
echo "STEP 3"
pipenv run python3 manage.py migrate
echo "STEP 4"
echo "from django.contrib.auth.models import User; User.objects.create_superuser('django_admin', 'admin@localhost', 'pass')" | pipenv run python3 manage.py shell
echo "STEP 5"
token=$(pipenv run python3 manage.py drf_create_token django_admin | awk '{print $3}')
echo "STEP 6"
sleep 5
sed -i -e "s/.*token.*/token = $token/g" res/config.ini
echo "STEP 8"
pipenv run /bin/sh /home/access-pc/start.sh