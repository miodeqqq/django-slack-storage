#!/bin/bash

set -e

echo "${0}: running migrations."
python manage.py migrate

echo "from django.contrib.auth.models import User; print(\"Admin exists\") if User.objects.filter(username='admin').exists() else User.objects.create_superuser('admin', 'maciek@mjanuszewski.pl', 'admin')" | python manage.py shell

echo "${0}: collecting statics."
python manage.py collectstatic --noinput -l

echo "${0}: starting gunicorn."

gunicorn slack_client.wsgi:application \
  --name root \
  --bind 0.0.0.0:8000 \
  --timeout 900 \
  --workers 3 \
  --reload \
  --log-level=info \
  --log-file=-
  "$@"