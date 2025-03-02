#!/bin/sh

echo "Waiting for PostgreSQL to be ready..."
/wait-for-it.sh db 5432 -- echo "PostgreSQL is up!"

echo "Applying migrations..."
python manage.py migrate

echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000