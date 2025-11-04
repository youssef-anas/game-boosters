#!/bin/bash

# GameBoosters Docker Deployment Script for Hostinger VPS
# This script automates the deployment process using Docker

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="gameboosters"
PROJECT_DIR="/home/django/game-boosters-main"
BACKUP_DIR="/home/django/backups"

echo -e "${GREEN}Starting GameBoosters Docker deployment...${NC}"

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root. Please run as django user."
   exit 1
fi

# Check if project directory exists
if [ ! -d "$PROJECT_DIR" ]; then
    print_error "Project directory $PROJECT_DIR does not exist!"
    exit 1
fi

# Navigate to project directory
cd "$PROJECT_DIR"

print_status "Creating backup before deployment..."

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Create database backup if containers are running
if docker-compose -f docker-compose.prod.yml ps | grep -q "Up"; then
    DB_BACKUP_FILE="$BACKUP_DIR/backup_$(date +%Y%m%d_%H%M%S).sql"
    docker-compose -f docker-compose.prod.yml exec -T db pg_dump -U postgres gameboosters_db01 > "$DB_BACKUP_FILE" 2>/dev/null || print_warning "Database backup failed"
    if [ -f "$DB_BACKUP_FILE" ]; then
        gzip "$DB_BACKUP_FILE"
        print_status "Database backup created: ${DB_BACKUP_FILE}.gz"
    fi
else
    print_warning "Containers not running, skipping database backup"
fi

print_status "Pulling latest changes from git..."
git pull origin main || git pull origin master || print_warning "Git pull failed, continuing with current code"

print_status "Stopping existing containers..."
docker-compose -f docker-compose.prod.yml down || print_warning "No containers to stop"

print_status "Building Docker images..."
docker-compose -f docker-compose.prod.yml build

print_status "Starting services..."
docker-compose -f docker-compose.prod.yml up -d

print_status "Waiting for services to be ready..."
sleep 10

print_status "Running Django migrations..."
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

print_status "Collecting static files..."
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

print_status "Checking service status..."
if docker-compose -f docker-compose.prod.yml ps | grep -q "Up"; then
    print_status "All services are running successfully!"
else
    print_error "Some services failed to start!"
    docker-compose -f docker-compose.prod.yml ps
    docker-compose -f docker-compose.prod.yml logs
    exit 1
fi

print_status "Cleaning up old backups (keeping last 7 days)..."
find "$BACKUP_DIR" -name "backup_*.sql.gz" -mtime +7 -delete 2>/dev/null || true

print_status "Deployment completed successfully!"
print_status "Application should be accessible at your domain or VPS IP"

# Display service status
echo ""
print_status "Service Status:"
docker-compose -f docker-compose.prod.yml ps
echo ""
print_status "Recent logs:"
docker-compose -f docker-compose.prod.yml logs --tail=10 