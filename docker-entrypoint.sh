#!/bin/bash
set -e

echo "Starting GameBoosterss application..."

# Wait for database
echo "Waiting for PostgreSQL..."
while ! pg_isready -h "$DB_HOST" -U "$DB_USER" -t 5; do
  echo "Database is unavailable - sleeping"
  sleep 2
done
echo "Database is up!"

# Wait for Redis
if [ "$USE_REDIS" = "True" ]; then
  echo "Waiting for Redis..."
  REDIS_PORT=${REDIS_PORT:-6379}
  while ! timeout 1 bash -c "echo > /dev/tcp/$REDIS_HOST/$REDIS_PORT" 2>/dev/null; do
    echo "Redis is unavailable - sleeping"
    sleep 2
  done
  echo "Redis is up!"
fi

# Run migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput || true

# Create superuser (optional - remove in production)
# echo "Creating superuser..."
# python manage.py createsuperuser --noinput || true

echo "Starting Daphne server..."
exec daphne -b 0.0.0.0 -p 8000 gameBoosterss.asgi:application

