#!/bin/bash

# SSL Certificate Renewal Script for GameBoosters VPS
# This script automatically renews Let's Encrypt SSL certificates

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="/home/django/game-boosters-main"
DOMAIN="yourdomain.com"  # Replace with your actual domain
EMAIL="your-email@domain.com"  # Replace with your email

echo -e "${GREEN}Starting SSL certificate renewal...${NC}"

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

# Navigate to project directory
cd "$PROJECT_DIR"

# Check if project directory exists
if [ ! -d "$PROJECT_DIR" ]; then
    print_error "Project directory $PROJECT_DIR does not exist!"
    exit 1
fi

# Check if docker-compose.prod.yml exists
if [ ! -f "docker-compose.prod.yml" ]; then
    print_error "docker-compose.prod.yml not found!"
    exit 1
fi

print_status "Stopping nginx container to free up ports..."
docker-compose -f docker-compose.prod.yml stop nginx

print_status "Checking certificate expiration..."
# Check if certificate exists and when it expires
if [ -f "ssl/live/$DOMAIN/fullchain.pem" ]; then
    EXPIRY_DATE=$(openssl x509 -enddate -noout -in "ssl/live/$DOMAIN/fullchain.pem" | cut -d= -f2)
    EXPIRY_EPOCH=$(date -d "$EXPIRY_DATE" +%s)
    CURRENT_EPOCH=$(date +%s)
    DAYS_UNTIL_EXPIRY=$(( ($EXPIRY_EPOCH - $CURRENT_EPOCH) / 86400 ))
    
    print_status "Certificate expires on: $EXPIRY_DATE ($DAYS_UNTIL_EXPIRY days from now)"
    
    # Only renew if certificate expires in less than 30 days
    if [ $DAYS_UNTIL_EXPIRY -gt 30 ]; then
        print_status "Certificate is still valid for more than 30 days. Skipping renewal."
        docker-compose -f docker-compose.prod.yml up -d nginx
        exit 0
    fi
else
    print_warning "No existing certificate found. Will create a new one."
fi

print_status "Renewing SSL certificate..."
# Renew certificate using certbot
docker run --rm \
  -v $(pwd)/ssl:/etc/letsencrypt \
  -v $(pwd)/ssl:/var/lib/letsencrypt \
  -p 80:80 \
  -p 443:443 \
  certbot/certbot renew \
  --standalone \
  --quiet \
  --email "$EMAIL" \
  --agree-tos \
  --no-eff-email \
  -d "$DOMAIN" \
  -d "www.$DOMAIN"

# Check if renewal was successful
if [ $? -eq 0 ]; then
    print_status "Certificate renewal successful!"
else
    print_error "Certificate renewal failed!"
    docker-compose -f docker-compose.prod.yml up -d nginx
    exit 1
fi

print_status "Copying renewed certificates..."
# Copy renewed certificates to nginx SSL directory
if [ -f "ssl/live/$DOMAIN/fullchain.pem" ]; then
    cp "ssl/live/$DOMAIN/fullchain.pem" ssl/cert.pem
    cp "ssl/live/$DOMAIN/privkey.pem" ssl/key.pem
    
    # Set proper permissions
    chmod 600 ssl/cert.pem ssl/key.pem
    print_status "Certificates copied successfully!"
else
    print_error "Renewed certificates not found!"
    docker-compose -f docker-compose.prod.yml up -d nginx
    exit 1
fi

print_status "Starting nginx container..."
# Start nginx container with new certificates
docker-compose -f docker-compose.prod.yml up -d nginx

# Wait a moment for nginx to start
sleep 5

print_status "Checking nginx status..."
# Check if nginx started successfully
if docker-compose -f docker-compose.prod.yml ps nginx | grep -q "Up"; then
    print_status "Nginx started successfully!"
else
    print_error "Nginx failed to start!"
    docker-compose -f docker-compose.prod.yml logs nginx
    exit 1
fi

print_status "Testing HTTPS connection..."
# Test HTTPS connection
if curl -s -o /dev/null -w "%{http_code}" "https://$DOMAIN" | grep -q "200\|301\|302"; then
    print_status "HTTPS connection test successful!"
else
    print_warning "HTTPS connection test failed. Check nginx logs."
    docker-compose -f docker-compose.prod.yml logs nginx
fi

print_status "SSL certificate renewal completed successfully!"
print_status "Your site is now accessible via HTTPS: https://$DOMAIN"

# Log the renewal
echo "$(date): SSL certificate renewed successfully for $DOMAIN" >> /home/django/ssl_renew.log 