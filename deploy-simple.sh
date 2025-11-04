#!/bin/bash
# Simple Deployment Script - Uses SSH with key authentication
# This script will guide you through deployment step by step

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# VPS Connection Details
VPS_HOST="46.202.131.43"
VPS_PORT="22"
VPS_USER="root"
SSH_KEY_PATH="$HOME/.ssh/id_rsa"

# Try Windows path if Linux path doesn't exist
if [ ! -f "$SSH_KEY_PATH" ]; then
    SSH_KEY_PATH="/c/Users/youss/.ssh/id_rsa"
fi

# Project Details
DOMAIN_NAME="madboost.gg"
PROJECT_DIR="/opt/game-boosters"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  GameBoosterss VPS Deployment Script${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Test SSH connection first
echo -e "${YELLOW}Step 1: Testing SSH connection...${NC}"
echo -e "${YELLOW}You will be prompted for your SSH key passphrase: 123456789${NC}"
echo ""

if ssh -i "$SSH_KEY_PATH" -o StrictHostKeyChecking=no -p "$VPS_PORT" "$VPS_USER@$VPS_HOST" "echo 'Connection successful'" 2>&1; then
    echo -e "${GREEN}✅ SSH connection successful!${NC}"
    echo ""
else
    echo -e "${RED}❌ SSH connection failed.${NC}"
    echo -e "${YELLOW}Please try connecting manually first:${NC}"
    echo "   ssh -i $SSH_KEY_PATH $VPS_USER@$VPS_HOST"
    echo ""
    echo -e "${YELLOW}If that works, run this script again.${NC}"
    exit 1
fi

# Function to run commands on VPS
run_ssh() {
    ssh -i "$SSH_KEY_PATH" -o StrictHostKeyChecking=no -p "$VPS_PORT" "$VPS_USER@$VPS_HOST" "$1"
}

# Step 2: Install Docker
echo -e "${YELLOW}Step 2: Installing Docker and dependencies...${NC}"
run_ssh "bash -c 'apt update && apt upgrade -y && apt install -y curl git python3-pip nginx certbot python3-certbot-nginx'"
run_ssh "bash -c 'if ! command -v docker &> /dev/null; then curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh && rm get-docker.sh; fi'"
run_ssh "bash -c 'if ! command -v docker-compose &> /dev/null; then curl -L \"https://github.com/docker/compose/releases/latest/download/docker-compose-\$(uname -s)-\$(uname -m)\" -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose; fi'"
echo -e "${GREEN}✅ Docker installed${NC}"
echo ""

# Step 3: Clone repository
echo -e "${YELLOW}Step 3: Cloning repository...${NC}"
run_ssh "bash -c 'if [ ! -d \"$PROJECT_DIR\" ]; then mkdir -p /opt && git clone https://github.com/youssef-anas/game-boosters.git $PROJECT_DIR; else cd $PROJECT_DIR && git pull origin main; fi'"
echo -e "${GREEN}✅ Repository cloned${NC}"
echo ""

# Step 4: Create .env file
echo -e "${YELLOW}Step 4: Creating .env file...${NC}"
run_ssh "bash -c 'cat > $PROJECT_DIR/.env << \"ENVEOF\"
# Django Settings
DEBUG=False
SECRET_KEY=your-django-secret-key-here
DOMAIN_NAME=$DOMAIN_NAME

# Database Configuration (for Docker)
DB_NAME=gameboosters_db01
DB_USER=postgres
DB_PASSWORD=123
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
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=your-google-oauth-client-id
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=your-google-oauth-client-secret
SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI=https://$DOMAIN_NAME/social/complete/google-oauth2/

# Payment Configuration
PAYMENT_KEY=your-payment-key
MERCHANT_UUID=your-merchant-uuid
ENVEOF
chmod 600 $PROJECT_DIR/.env'"
echo -e "${GREEN}✅ .env file created${NC}"
echo ""

# Step 5: Configure firewall
echo -e "${YELLOW}Step 5: Configuring firewall...${NC}"
run_ssh "bash -c 'ufw allow 22/tcp && ufw allow 80/tcp && ufw allow 443/tcp && echo \"y\" | ufw enable || true'"
echo -e "${GREEN}✅ Firewall configured${NC}"
echo ""

# Step 6: Create systemd service
echo -e "${YELLOW}Step 6: Creating systemd service...${NC}"
run_ssh "bash -c 'cat > /etc/systemd/system/gameboosters.service << \"SERVICEEOF\"
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
SERVICEEOF
systemctl daemon-reload && systemctl enable gameboosters.service'"
echo -e "${GREEN}✅ Systemd service created${NC}"
echo ""

# Step 7: Build and start containers
echo -e "${YELLOW}Step 7: Building and starting Docker containers...${NC}"
echo -e "${YELLOW}This may take a few minutes...${NC}"
run_ssh "bash -c 'cd $PROJECT_DIR && docker-compose -f docker-compose.prod.yml down || true'"
run_ssh "bash -c 'cd $PROJECT_DIR && docker-compose -f docker-compose.prod.yml up -d --build'"
echo -e "${GREEN}✅ Containers started${NC}"
echo ""

# Step 8: Wait and check status
echo -e "${YELLOW}Step 8: Waiting for services to start...${NC}"
sleep 15

echo -e "${YELLOW}Step 9: Checking container status...${NC}"
run_ssh "cd $PROJECT_DIR && docker-compose -f docker-compose.prod.yml ps"

echo ""
echo -e "${GREEN}✅ Deployment complete!${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo ""
echo "1. Create Django superuser:"
echo "   ssh -i $SSH_KEY_PATH $VPS_USER@$VPS_HOST"
echo "   cd $PROJECT_DIR"
echo "   docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser"
echo ""
echo "2. View logs:"
echo "   ssh -i $SSH_KEY_PATH $VPS_USER@$VPS_HOST"
echo "   cd $PROJECT_DIR"
echo "   docker-compose -f docker-compose.prod.yml logs -f"
echo ""
echo "3. Set up SSL (after DNS is configured):"
echo "   ssh -i $SSH_KEY_PATH $VPS_USER@$VPS_HOST"
echo "   certbot certonly --standalone -d $DOMAIN_NAME -d www.$DOMAIN_NAME"
echo ""
echo -e "${GREEN}Your application should be accessible at: http://$VPS_HOST:8000${NC}"
echo -e "${GREEN}Once DNS is configured: https://$DOMAIN_NAME${NC}"

