#!/bin/bash

# Run any database migrations
if [ "$DJANGO_MIGRATE_DB_ON_STARTUP" != "False" ]; then
  echo "Running database migrations..."
  python manage.py migrate
fi

exec "$@"