#!/bin/bash

sleep 1

if [ $DJANGO_DEBUG = "true" ]; then
    echo "[START] install dependencies"
    pip install -r requirements.txt
fi

if [ $MIGRATIONS = "true" ]; then
    echo "[START] apply migrations"
    python manage.py migrate
fi

if [ $PRERUN = "true" ]; then
    echo "[START] run preinit script"
    echo "exec(open('prerun.py').read())" | python manage.py shell
fi

chmod 777 attachments
if [ $DJANGO_DEBUG = "true" ]; then
    echo "[START] launch app in DEBUG mode"
    python manage.py runserver 0.0.0.0:8000
else
    python manage.py collectstatic --noinput
    echo "[START] launch app in RELEASE mode"
    uwsgi --chdir=. \
          --module=web.wsgi:application \
          --env DJANGO_SETTINGS_MODULE=web.settings \
          --master \
          --http=0.0.0.0:8000 \
          --processes=2 \
          --uid=1000 --gid=2000 \
          --harakiri=20 \
          --max-requests=5000 \
          --vacuum
fi