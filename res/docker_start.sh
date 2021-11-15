#!/bin/sh
cd /home/access-pc/
pipenv run python3 manage.py makemigrations
pipenv run python3 manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('django_admin', 'admin@localhost', 'pass')" | python manage.py shell
token=$(python manage.py drf_create_token django_admin | awk '{print $3}')
sed -i -e "s/.*token.*/token = $token/g" config_default.ini
pipenv run /bin/sh /home/access-pc/start.sh