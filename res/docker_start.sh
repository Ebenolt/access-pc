#!/bin/sh
cd /home/access-pc/
sleep 60
echo "1. Preparing Migrations"
pipenv run python3 manage.py makemigrations
echo "2. Applying Migrations"
pipenv run python3 manage.py migrate
echo "3. Creating superuser / token"
echo "from django.contrib.auth.models import User; User.objects.create_superuser('django_admin', 'admin@localhost', 'pass')" | pipenv run python3 manage.py shell
token=$(pipenv run python3 manage.py drf_create_token django_admin | awk '{print $3}')
echo "4. Editing configuration"
cd res
cp config.ini temp.ini
sed -i -e "s/.*token.*/token = $token/g" temp.ini
cp temp.ini config.ini
echo ""
echo "BASE API TOKEN : $token"
echo "Now starting server at http://localhost:8080"
echo ""

cd ..
pipenv run /bin/sh /home/access-pc/start.sh
