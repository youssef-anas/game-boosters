#!/bin/bash

# Complete SSL Setup Script for GameBoosters VPS
# This script sets up HTTPS with Let's Encrypt SSL certificates

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}  GameBoosters SSL Setup Script${NC}"
echo -e "${BLUE}================================${NC}"

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

print_header() {
    echo -e "${BLUE}[SETUP]${NC} $1"
}

# Configuration
PROJECT_DIR="/home/django/game-boosters-main"

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

print_header "SSL Setup Configuration"
echo ""

# Get domain name
read -p "Enter your domain name (e.g., example.com): " DOMAIN
if [ -z "$DOMAIN" ]; then
    print_error "Domain name is required!"
    exit 1
fi

# Get email address
read -p "Enter your email address: " EMAIL
if [ -z "$EMAIL" ]; then
    print_error "Email address is required!"
    exit 1
fi

print_header "Starting SSL Setup Process"
echo ""

print_status "Checking if Docker is running..."
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker first."
    exit 1
fi

print_status "Checking if application is running..."
if ! docker-compose -f docker-compose.prod.yml ps | grep -q "Up"; then
    print_warning "Application containers are not running. Starting them first..."
    docker-compose -f docker-compose.prod.yml up -d
    sleep 10
fi

print_status "Stopping nginx container to free up ports..."
docker-compose -f docker-compose.prod.yml stop nginx

print_status "Creating SSL directory..."
mkdir -p ssl

print_status "Checking domain resolution..."
if ! nslookup "$DOMAIN" > /dev/null 2>&1; then
    print_warning "Domain $DOMAIN might not be resolving to this server."
    print_warning "Make sure your domain points to this VPS IP address."
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_error "SSL setup cancelled."
        docker-compose -f docker-compose.prod.yml up -d nginx
        exit 1
    fi
fi

print_header "Obtaining SSL Certificate"
echo ""

print_status "Running certbot to get SSL certificate..."
docker run -it --rm \
  -v $(pwd)/ssl:/etc/letsencrypt \
  -v $(pwd)/ssl:/var/lib/letsencrypt \
  -p 80:80 \
  -p 443:443 \
  certbot/certbot certonly \
  --standalone \
  --email "$EMAIL" \
  --agree-tos \
  --no-eff-email \
  -d "$DOMAIN" \
  -d "www.$DOMAIN"

if [ $? -ne 0 ]; then
    print_error "Failed to obtain SSL certificate!"
    docker-compose -f docker-compose.prod.yml up -d nginx
    exit 1
fi

print_status "SSL certificate obtained successfully!"

print_header "Configuring Nginx for HTTPS"
echo ""

print_status "Copying certificates..."
if [ -f "ssl/live/$DOMAIN/fullchain.pem" ]; then
    cp "ssl/live/$DOMAIN/fullchain.pem" ssl/cert.pem
    cp "ssl/live/$DOMAIN/privkey.pem" ssl/key.pem
    
    # Set proper permissions
    chmod 600 ssl/cert.pem ssl/key.pem
    print_status "Certificates copied successfully!"
else
    print_error "Certificate files not found!"
    docker-compose -f docker-compose.prod.yml up -d nginx
    exit 1
fi

print_status "Updating nginx configuration..."
# Create HTTPS nginx configuration
cp nginx-https.conf nginx.conf

# Replace domain placeholders
sed -i "s/yourdomain.com/$DOMAIN/g" nginx.conf

print_status "Starting nginx with HTTPS configuration..."
docker-compose -f docker-compose.prod.yml up -d nginx

# Wait for nginx to start
sleep 5

print_status "Checking nginx status..."
if docker-compose -f docker-compose.prod.yml ps nginx | grep -q "Up"; then
    print_status "Nginx started successfully!"
else
    print_error "Nginx failed to start!"
    docker-compose -f docker-compose.prod.yml logs nginx
    exit 1
fi

print_header "Testing HTTPS Setup"
echo ""

print_status "Testing HTTPS connection..."
if curl -s -o /dev/null -w "%{http_code}" "https://$DOMAIN" | grep -q "200\|301\|302"; then
    print_status "HTTPS connection test successful!"
else
    print_warning "HTTPS connection test failed. This might be normal if the domain is not fully propagated yet."
fi

print_status "Testing HTTP to HTTPS redirect..."
REDIRECT_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "http://$DOMAIN")
if [ "$REDIRECT_STATUS" = "301" ] || [ "$REDIRECT_STATUS" = "302" ]; then
    print_status "HTTP to HTTPS redirect is working!"
else
    print_warning "HTTP to HTTPS redirect might not be working yet."
fi

print_header "Setting Up Auto-Renewal"
echo ""

print_status "Creating SSL renewal script..."
# Update the renewal script with correct domain and email
sed -i "s/yourdomain.com/$DOMAIN/g" ssl_renew.sh
sed -i "s/your-email@domain.com/$EMAIL/g" ssl_renew.sh

print_status "Making renewal script executable..."
chmod +x ssl_renew.sh

print_status "Setting up automatic renewal in crontab..."
# Add to crontab if not already present
if ! crontab -l 2>/dev/null | grep -q "ssl_renew.sh"; then
    (crontab -l 2>/dev/null; echo "0 12,18 * * * $PROJECT_DIR/ssl_renew.sh >> /home/django/ssl_renew.log 2>&1") | crontab -
    print_status "Auto-renewal scheduled (runs at 12:00 PM and 6:00 PM daily)"
else
    print_status "Auto-renewal already scheduled"
fi

print_header "SSL Setup Complete!"
echo ""

print_status "Your Django application is now accessible via HTTPS!"
print_status "URL: https://$DOMAIN"
print_status "HTTP requests will automatically redirect to HTTPS"

echo ""
print_status "Certificate Details:"
if [ -f "ssl/live/$DOMAIN/fullchain.pem" ]; then
    EXPIRY_DATE=$(openssl x509 -enddate -noout -in "ssl/live/$DOMAIN/fullchain.pem" | cut -d= -f2)
    print_status "Certificate expires on: $EXPIRY_DATE"
fi

echo ""
print_status "Next Steps:"
echo "1. Test your website at https://$DOMAIN"
echo "2. Check SSL grade at https://www.ssllabs.com/ssltest/"
echo "3. Monitor renewal logs at /home/django/ssl_renew.log"
echo "4. Update your Django settings if needed for HTTPS"

echo ""
print_status "SSL setup completed successfully! 🎉" 