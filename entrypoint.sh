#!/bin/sh

# Exit script on any error
set -e

# Run database migrations
echo "Applying database migrations..."
python manage.py makemigrations

# Run database make migrations
echo "Applying database migrations..."
python manage.py migrate

# Collect static files (if needed)
echo "Collecting static files..."
python manage.py collectstatic --noinput

# You can add other Django management commands if needed

# Start the Gunicorn server
echo "Starting Gunicorn server..."
exec gunicorn --workers 3 --bind 0.0.0.0:8000 mehdibar.wsgi:application
