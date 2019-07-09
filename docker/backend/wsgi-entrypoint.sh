#!/usr/bin/env bash

ls -al /app/backend/server/static/client/static/js

echo "Start backend server"
until cd /app/backend/server
do
    echo "Waiting for server volume..."
done

until ./manage.py migrate
do
    echo "Waiting for postgres ready..."
    sleep 2
done

./manage.py collectstatic --noinput

gunicorn server.wsgi --bind 0.0.0.0:8000 --workers 4 --threads 4
#./manage.py runserver 0.0.0.0:8000 # --settings=settings.dev_docker