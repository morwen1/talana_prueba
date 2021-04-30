#!/bin/bash



docker-compose build
docker-compose down
docker-compose run --rm django python manage.py makemigrations
docker-compose run --rm django python manage.py migrate
docker-compose run --rm django python manage.py loaddata fixtures/*.json
docker-compose up -d
#docker-compose scale celeryworker=2