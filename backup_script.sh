#!/bin/bash

# GameBoosters Backup Script
# This script creates backups of the database and application files

set -e

# Configuration
BACKUP_DIR="/home/django/backups"
PROJECT_DIR="/home/django/game-boosters-main"
DB_NAME="gameboosters_db01"
DB_USER="gameboosters_user"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=7

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

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

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

print_status "Starting backup process..."

# Database backup
print_status "Creating database backup..."
DB_BACKUP_FILE="$BACKUP_DIR/db_backup_$DATE.sql"
if command -v pg_dump &> /dev/null; then
    if pg_dump -h localhost -U "$DB_USER" "$DB_NAME" > "$DB_BACKUP_FILE" 2>/dev/null; then
        gzip "$DB_BACKUP_FILE"
        print_status "Database backup created: ${DB_BACKUP_FILE}.gz"
        
        # Verify backup
        if gunzip -t "${DB_BACKUP_FILE}.gz" 2>/dev/null; then
            print_status "Database backup verified successfully"
        else
            print_error "Database backup verification failed"
            rm -f "${DB_BACKUP_FILE}.gz"
        fi
    else
        print_error "Database backup failed"
        exit 1
    fi
else
    print_error "pg_dump not found. Please install PostgreSQL client tools."
    exit 1
fi

# Application files backup (excluding unnecessary files)
print_status "Creating application files backup..."
APP_BACKUP_FILE="$BACKUP_DIR/app_backup_$DATE.tar.gz"

# Create tar archive excluding unnecessary files
tar --exclude='venv' \
    --exclude='.git' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.env' \
    --exclude='media' \
    --exclude='staticfiles' \
    --exclude='backups' \
    --exclude='*.log' \
    -czf "$APP_BACKUP_FILE" -C "$PROJECT_DIR" .

if [ $? -eq 0 ]; then
    print_status "Application files backup created: $APP_BACKUP_FILE"
else
    print_error "Application files backup failed"
    exit 1
fi

# Environment variables backup (if .env exists)
if [ -f "$PROJECT_DIR/.env" ]; then
    print_status "Creating environment variables backup..."
    ENV_BACKUP_FILE="$BACKUP_DIR/env_backup_$DATE.txt"
    cp "$PROJECT_DIR/.env" "$ENV_BACKUP_FILE"
    print_status "Environment variables backup created: $ENV_BACKUP_FILE"
fi

# Create backup manifest
print_status "Creating backup manifest..."
MANIFEST_FILE="$BACKUP_DIR/backup_manifest_$DATE.txt"
{
    echo "Backup created on: $(date)"
    echo "Database backup: db_backup_$DATE.sql.gz"
    echo "Application backup: app_backup_$DATE.tar.gz"
    if [ -f "$PROJECT_DIR/.env" ]; then
        echo "Environment backup: env_backup_$DATE.txt"
    fi
    echo ""
    echo "Backup sizes:"
    ls -lh "$BACKUP_DIR"/*_$DATE.* 2>/dev/null || true
} > "$MANIFEST_FILE"

print_status "Backup manifest created: $MANIFEST_FILE"

# Clean up old backups
print_status "Cleaning up old backups (keeping last $RETENTION_DAYS days)..."
find "$BACKUP_DIR" -name "db_backup_*.sql.gz" -mtime +$RETENTION_DAYS -delete 2>/dev/null || true
find "$BACKUP_DIR" -name "app_backup_*.tar.gz" -mtime +$RETENTION_DAYS -delete 2>/dev/null || true
find "$BACKUP_DIR" -name "env_backup_*.txt" -mtime +$RETENTION_DAYS -delete 2>/dev/null || true
find "$BACKUP_DIR" -name "backup_manifest_*.txt" -mtime +$RETENTION_DAYS -delete 2>/dev/null || true

# Show backup summary
print_status "Backup completed successfully!"
echo ""
print_status "Backup Summary:"
echo "=================="
echo "Backup directory: $BACKUP_DIR"
echo "Database backup: db_backup_$DATE.sql.gz"
echo "Application backup: app_backup_$DATE.tar.gz"
if [ -f "$PROJECT_DIR/.env" ]; then
    echo "Environment backup: env_backup_$DATE.txt"
fi
echo "Manifest: backup_manifest_$DATE.txt"
echo ""
echo "Total backup size:"
du -sh "$BACKUP_DIR"/*_$DATE.* 2>/dev/null | awk '{sum += $1} END {print sum " total"}'
echo ""
echo "Available backups:"
ls -lh "$BACKUP_DIR"/*.gz "$BACKUP_DIR"/*.tar.gz 2>/dev/null | wc -l | xargs echo "Total backup files:" 