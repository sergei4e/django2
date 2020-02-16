#!/bin/sh

python manage.py makemigrations
python manage.py migrate

python manage.py collectstatic --noinput

rm celery*.pid

celery multi start 1 -A super_news -B -l info --logfile=/code/logs/%n%I.log

gunicorn -b 0.0.0.0:8000 --reload -w 4 super_news.wsgi
