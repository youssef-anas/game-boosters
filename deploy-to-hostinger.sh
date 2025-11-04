#!/bin/bash
# Automated Deployment Script for Hostinger VPS
# This script will deploy GameBoosterss to your Hostinger VPS

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
SSH_KEY_PATH="/c/Users/youss/.ssh/id_rsa"
SSH_PASSPHRASE="123456789"

# Project Details
DOMAIN_NAME="madboost.gg"
PROJECT_DIR="/opt/game-boosters"

# Colors for output
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  GameBoosterss VPS Deployment Script${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Convert Windows path to Git Bash path
if [[ "$SSH_KEY_PATH" == /c/* ]]; then
    SSH_KEY_PATH="${SSH_KEY_PATH#/c/}"
    SSH_KEY_PATH="/c/$SSH_KEY_PATH"
fi

# Start ssh-agent and add key
echo -e "${YELLOW}Setting up SSH agent...${NC}"
eval "$(ssh-agent -s)"

# Function to add SSH key with passphrase
add_ssh_key() {
    echo -e "${YELLOW}Adding SSH key (you'll be prompted for passphrase: 123456789)...${NC}"
    SSH_ADD_OUTPUT=$(ssh-add "$SSH_KEY_PATH" 2>&1)
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ SSH key added successfully!${NC}"
        return 0
    else
        echo -e "${RED}❌ Failed to add SSH key. Please check your key path and passphrase.${NC}"
        echo "SSH output: $SSH_ADD_OUTPUT"
        return 1
    fi
}

# Add SSH key
if ! add_ssh_key; then
    echo -e "${YELLOW}Please enter your SSH key passphrase when prompted: 123456789${NC}"
    echo -e "${YELLOW}Or manually add the key: ssh-add $SSH_KEY_PATH${NC}"
    read -p "Press Enter after adding the key..."
fi

# Function to run commands on VPS via SSH
run_ssh_command() {
    ssh -i "$SSH_KEY_PATH" -o StrictHostKeyChecking=no -o ConnectTimeout=10 -p "$VPS_PORT" "$VPS_USER@$VPS_HOST" "$1"
}

# Function to copy file to VPS
copy_to_vps() {
    scp -i "$SSH_KEY_PATH" -o StrictHostKeyChecking=no -P "$VPS_PORT" "$1" "$VPS_USER@$VPS_HOST:$2"
}

echo -e "${YELLOW}Step 1: Testing SSH connection...${NC}"
echo -e "${YELLOW}You may be prompted for SSH key passphrase: 123456789${NC}"
if run_ssh_command "echo 'Connection successful'"; then
    echo -e "${GREEN}✅ SSH connection successful!${NC}"
else
    echo -e "${RED}❌ SSH connection failed. Please check your credentials.${NC}"
    echo -e "${YELLOW}Try manually connecting: ssh -i $SSH_KEY_PATH $VPS_USER@$VPS_HOST${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}Step 2: Installing Docker and dependencies on VPS...${NC}"
run_ssh_command "bash -c '
    apt update && apt upgrade -y
    apt install -y curl git python3-pip nginx certbot python3-certbot-nginx sshpass
    if ! command -v docker &> /dev/null; then
        curl -fsSL https://get.docker.com -o get-docker.sh
        sh get-docker.sh
        rm get-docker.sh
    fi
    if ! command -v docker-compose &> /dev/null; then
        curl -L \"https://github.com/docker/compose/releases/latest/download/docker-compose-\$(uname -s)-\$(uname -m)\" -o /usr/local/bin/docker-compose
        chmod +x /usr/local/bin/docker-compose
    fi
    echo \"Docker installation complete\"
'"

echo ""
echo -e "${YELLOW}Step 3: Cloning repository...${NC}"
run_ssh_command "bash -c '
    if [ ! -d \"$PROJECT_DIR\" ]; then
        mkdir -p /opt
        git clone https://github.com/youssef-anas/game-boosters.git $PROJECT_DIR
    else
        cd $PROJECT_DIR
        git pull origin main
    fi
    echo \"Repository ready\"
'"

echo ""
echo -e "${YELLOW}Step 4: Creating .env file on VPS...${NC}"
run_ssh_command "bash -c '
cat > $PROJECT_DIR/.env << \"ENVEOF\"
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

# PayPal Configuration (optional)
PAYPAL_CLIENT_ID=your-paypal-client-id
PAYPAL_CLIENT_SECRET=your-paypal-client-secret
PAYPAL_MODE=live
ENVEOF
    chmod 600 $PROJECT_DIR/.env
    echo \".env file created\"
'"

echo ""
echo -e "${YELLOW}Step 5: Configuring firewall...${NC}"
run_ssh_command "bash -c '
    ufw allow 22/tcp
    ufw allow 80/tcp
    ufw allow 443/tcp
    echo \"y\" | ufw enable || true
    echo \"Firewall configured\"
'"

echo ""
echo -e "${YELLOW}Step 6: Creating systemd service...${NC}"
run_ssh_command "bash -c '
cat > /etc/systemd/system/gameboosters.service << \"SERVICEEOF\"
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
    systemctl daemon-reload
    systemctl enable gameboosters.service
    echo \"Systemd service created\"
'"

echo ""
echo -e "${YELLOW}Step 7: Building and starting Docker containers...${NC}"
run_ssh_command "bash -c '
    cd $PROJECT_DIR
    docker-compose -f docker-compose.prod.yml down || true
    docker-compose -f docker-compose.prod.yml up -d --build
    echo \"Containers started\"
'"

echo ""
echo -e "${YELLOW}Step 8: Waiting for services to be ready...${NC}"
sleep 10

echo ""
echo -e "${YELLOW}Step 9: Checking container status...${NC}"
run_ssh_command "cd $PROJECT_DIR && docker-compose -f docker-compose.prod.yml ps"

echo ""
echo -e "${GREEN}✅ Deployment complete!${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "1. Create Django superuser:"
echo "   ssh -i $SSH_KEY_PATH $VPS_USER@$VPS_HOST"
echo "   cd $PROJECT_DIR"
echo "   docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser"
echo ""
echo "2. Set up SSL certificate (after DNS is configured):"
echo "   ssh -i $SSH_KEY_PATH $VPS_USER@$VPS_HOST"
echo "   certbot certonly --standalone -d $DOMAIN_NAME -d www.$DOMAIN_NAME"
echo ""
echo "3. View logs:"
echo "   ssh -i $SSH_KEY_PATH $VPS_USER@$VPS_HOST"
echo "   cd $PROJECT_DIR"
echo "   docker-compose -f docker-compose.prod.yml logs -f"
echo ""
echo -e "${GREEN}Your application should be accessible at: http://$VPS_HOST:8000${NC}"
echo -e "${GREEN}Once DNS is configured: https://$DOMAIN_NAME${NC}"

