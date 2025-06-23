#!/bin/bash

# Start PostgreSQL service
service postgresql start

# Wait a bit for PostgreSQL to fully boot
sleep 3

# Setup DB if not already created
su - postgres -c "psql -tc \"SELECT 1 FROM pg_database WHERE datname = '$DB_NAME'\" | grep -q 1 || psql -c \"CREATE DATABASE $DB_NAME;\""
su - postgres -c "psql -c \"ALTER USER $DB_USER WITH PASSWORD '$DB_PASSWORD';\""
su - postgres -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;\""

# Run Django migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Load fixture data only if no posts exist
echo "Checking if posts exist..."
python manage.py shell -c "from sentiment_analysis_app.models import Posts; exit(0) if Posts.objects.exists() else exit(1)"
if [ $? -ne 0 ]; then
  echo "Loading fixture data..."
  python manage.py loaddata sentiment_analysis_app/fixtures/all_data.json
fi

# Run Gunicorn
exec gunicorn sentiment_analysis.wsgi:application --bind 0.0.0.0:8000
