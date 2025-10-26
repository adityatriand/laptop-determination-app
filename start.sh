#!/bin/bash

# Wait for database to be ready
echo "Waiting for database to be ready..."
while ! python -c "import MySQLdb; MySQLdb.connect(host='$DATABASE_HOST', port=$DATABASE_PORT, user='$DATABASE_USER', passwd='$DATABASE_PASSWORD', db='$DATABASE_NAME')" 2>/dev/null; do
    echo "Database is unavailable - sleeping"
    sleep 2
done

echo "Database is ready!"

# Run Django commands
echo "Running Django migrations..."
python manage.py migrate

# Only collect static files in production
if [ "$DEBUG" = "False" ] || [ "$DEBUG" = "false" ]; then
    echo "Collecting static files for production..."
    python manage.py collectstatic --noinput
else
    echo "Skipping static file collection in development mode..."
fi

echo "Starting Django development server..."
python manage.py runserver 0.0.0.0:8000
