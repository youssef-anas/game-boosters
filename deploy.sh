#!/bin/bash

# GameBoosters Deployment Script for Hostinger VPS
# This script automates the deployment process

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="gameboosters"
PROJECT_DIR="/home/django/game-boosters-main"
VENV_DIR="$PROJECT_DIR/venv"
BACKUP_DIR="/home/django/backups"
LOG_DIR="/var/log/gameboosters"

echo -e "${GREEN}Starting GameBoosters deployment...${NC}"

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

# Create database backup
DB_BACKUP_FILE="$BACKUP_DIR/backup_$(date +%Y%m%d_%H%M%S).sql"
if command -v pg_dump &> /dev/null; then
    pg_dump -h localhost -U gameboosters_user gameboosters_db01 > "$DB_BACKUP_FILE" 2>/dev/null || print_warning "Database backup failed (this is normal if database doesn't exist yet)"
    if [ -f "$DB_BACKUP_FILE" ]; then
        gzip "$DB_BACKUP_FILE"
        print_status "Database backup created: ${DB_BACKUP_FILE}.gz"
    fi
else
    print_warning "pg_dump not found, skipping database backup"
fi

print_status "Pulling latest changes from git..."
git pull origin main || git pull origin master || print_warning "Git pull failed, continuing with current code"

print_status "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

print_status "Installing/updating Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

print_status "Installing gunicorn if not already installed..."
pip install gunicorn

print_status "Running Django migrations..."
python manage.py migrate

print_status "Collecting static files..."
python manage.py collectstatic --noinput

print_status "Creating log directory..."
sudo mkdir -p "$LOG_DIR"
sudo chown django:django "$LOG_DIR"

print_status "Setting proper permissions..."
sudo chown -R django:django "$PROJECT_DIR"

print_status "Restarting application service..."
sudo systemctl restart gameboosters

print_status "Checking service status..."
if sudo systemctl is-active --quiet gameboosters; then
    print_status "GameBoosters service is running successfully!"
else
    print_error "GameBoosters service failed to start!"
    sudo systemctl status gameboosters
    exit 1
fi

print_status "Testing nginx configuration..."
if sudo nginx -t; then
    print_status "Nginx configuration is valid!"
    sudo systemctl reload nginx
else
    print_error "Nginx configuration is invalid!"
    exit 1
fi

print_status "Cleaning up old backups (keeping last 7 days)..."
find "$BACKUP_DIR" -name "backup_*.sql.gz" -mtime +7 -delete 2>/dev/null || true

print_status "Deployment completed successfully!"
print_status "Application should be accessible at your domain or VPS IP"

# Display service status
echo ""
print_status "Service Status:"
sudo systemctl status gameboosters --no-pager -l
echo ""
print_status "Recent logs:"
sudo tail -n 10 "$LOG_DIR/error.log" 2>/dev/null || print_warning "No error logs found yet" 