#!/bin/sh

set -e

if [ -n "$DATABASE_URL" ]; then
    until psql "$DATABASE_URL" -c '\l'; do
      >&2 echo "Postgres is unavailable - sleeping for 1s"
      sleep 1
    done
    >&2 echo "Postgres is up - executing command"
fi

exec "$@"