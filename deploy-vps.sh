#!/bin/bash
# Hostinger VPS Deployment Script for GameBoosterss
# Run this script on your Hostinger VPS

set -e

echo "🚀 Starting GameBoosterss VPS Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root or with sudo
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}Please run as root or with sudo${NC}"
    exit 1
fi

# Update system
echo -e "${YELLOW}Updating system packages...${NC}"
apt update && apt upgrade -y

# Install required packages
echo -e "${YELLOW}Installing required packages...${NC}"
apt install -y curl git python3-pip python3-venv nginx certbot python3-certbot-nginx

# Install Docker
if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}Installing Docker...${NC}"
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
else
    echo -e "${GREEN}Docker already installed${NC}"
fi

# Install Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo -e "${YELLOW}Installing Docker Compose...${NC}"
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
else
    echo -e "${GREEN}Docker Compose already installed${NC}"
fi

# Set project directory
PROJECT_DIR="/opt/game-boosters"
echo -e "${YELLOW}Project will be installed to: ${PROJECT_DIR}${NC}"

# Clone repository if not exists
if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${YELLOW}Cloning repository...${NC}"
    mkdir -p /opt
    git clone https://github.com/youssef-anas/game-boosters.git $PROJECT_DIR
else
    echo -e "${GREEN}Repository already exists${NC}"
fi

cd $PROJECT_DIR

# Create .env file if not exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env file...${NC}"
    cat > .env << 'EOF'
# Django Settings
DEBUG=False
SECRET_KEY=CHANGE_THIS_SECRET_KEY
DOMAIN_NAME=your-domain.com

# Database Configuration (for Docker)
DB_NAME=gameboosters_db01
DB_USER=postgres
DB_PASSWORD=CHANGE_THIS_DB_PASSWORD
DB_HOST=db
DB_PORT=5432
DB_CONN_MAX_AGE=60
DB_SSLMODE=prefer

# Redis Configuration (for Docker)
USE_REDIS=True
REDIS_HOST=redis
REDIS_PORT=6379

# Email Configuration
EMAIL_HOST=smtp.office365.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
DEFAULT_FROM_EMAIL=your-email@example.com

# Media Configuration
MEDIA_URL=/media/

# Social Auth - Google
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=your-google-oauth-key
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=your-google-oauth-secret
SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI=https://your-domain.com/social/complete/google-oauth2/

# Payment Configuration
PAYMENT_KEY=your-payment-key
MERCHANT_UUID=your-merchant-uuid
EOF
    echo -e "${RED}⚠️  IMPORTANT: Please edit .env file and update all values!${NC}"
    echo -e "${YELLOW}Run: nano $PROJECT_DIR/.env${NC}"
else
    echo -e "${GREEN}.env file already exists${NC}"
fi

# Configure firewall
echo -e "${YELLOW}Configuring firewall...${NC}"
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

# Create systemd service
echo -e "${YELLOW}Creating systemd service...${NC}"
cat > /etc/systemd/system/gameboosters.service << EOF
[Unit]
Description=GameBoosterss Docker Compose
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=$PROJECT_DIR
ExecStart=/usr/local/bin/docker-compose -f docker-compose.prod.yml up -d
ExecStop=/usr/local/bin/docker-compose -f docker-compose.prod.yml down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable gameboosters.service

echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Edit .env file: nano $PROJECT_DIR/.env"
echo "2. Generate Django secret key:"
echo "   python3 -c \"from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())\""
echo "3. Update SECRET_KEY, DB_PASSWORD, and other values in .env"
echo "4. Build and start containers:"
echo "   cd $PROJECT_DIR"
echo "   docker-compose -f docker-compose.prod.yml up -d --build"
echo "5. Create superuser:"
echo "   docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser"
echo "6. Set up SSL certificate (after domain DNS is configured):"
echo "   certbot certonly --standalone -d your-domain.com -d www.your-domain.com"
echo ""
echo -e "${GREEN}For detailed instructions, see: HOSTINGER_VPS_DEPLOYMENT.md${NC}"

