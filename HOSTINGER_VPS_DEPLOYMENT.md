# 🚀 Hostinger VPS Deployment Guide

## 📋 Prerequisites

- Hostinger VPS with Ubuntu 20.04+ or similar
- SSH access to your VPS
- Domain name pointing to your VPS IP address
- Root or sudo access

## 🎯 Step-by-Step Deployment

### Step 1: Connect to Your Hostinger VPS

```bash
ssh root@your-vps-ip
# Or if using a different user:
ssh username@your-vps-ip
```

### Step 2: Update System and Install Dependencies

```bash
# Update system packages
apt update && apt upgrade -y

# Install required packages
apt install -y curl git python3-pip python3-venv nginx certbot python3-certbot-nginx
```

### Step 3: Install Docker and Docker Compose

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Verify installation
docker --version
docker-compose --version

# Add current user to docker group (if not root)
usermod -aG docker $USER
```

### Step 4: Clone Repository from GitHub

```bash
# Navigate to a suitable directory
cd /opt  # or /var/www or your preferred location

# Clone the repository
git clone https://github.com/youssef-anas/game-boosters.git
cd game-boosters

# Verify you're in the right directory
ls -la
```

### Step 5: Create `.env` File on VPS

```bash
# Create .env file
nano .env
```

**Paste the following content and customize with your actual values:**

```bash
# Django Settings
DEBUG=False
SECRET_KEY=your-very-secure-secret-key-change-this
DOMAIN_NAME=your-domain.com

# Database Configuration (for Docker)
DB_NAME=gameboosters_db01
DB_USER=postgres
DB_PASSWORD=your-strong-database-password-here
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

# PayPal Configuration (optional)
PAYPAL_CLIENT_ID=your-paypal-client-id
PAYPAL_CLIENT_SECRET=your-paypal-client-secret
PAYPAL_MODE=live
```

**Important:** 
- Press `Ctrl+O` to save, then `Enter` to confirm
- Press `Ctrl+X` to exit nano
- **CHANGE the SECRET_KEY** - Generate a new one:
  ```bash
  python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```

### Step 6: Generate Django Secret Key

```bash
# If Python Django is available, generate secret key:
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Or use openssl:
openssl rand -base64 32

# Copy the generated key and update it in .env file
nano .env
```

### Step 7: Build and Start Docker Containers

```bash
# Make sure you're in the project directory
cd /opt/game-boosters  # or wherever you cloned it

# Build and start all services
docker-compose -f docker-compose.prod.yml up -d --build

# Check if containers are running
docker-compose -f docker-compose.prod.yml ps

# View logs to ensure everything started correctly
docker-compose -f docker-compose.prod.yml logs -f
```

**Wait for services to start** (check logs for any errors)

### Step 8: Create Django Superuser

```bash
# Create an admin user
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

# Follow the prompts to create admin account
```

### Step 9: Configure Firewall

```bash
# Allow necessary ports
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS

# Enable firewall
ufw enable

# Check status
ufw status
```

### Step 10: Set Up SSL/HTTPS with Certbot

```bash
# Install certbot if not already installed
apt install -y certbot python3-certbot-nginx

# Get SSL certificate (replace with your domain)
certbot certonly --standalone -d your-domain.com -d www.your-domain.com

# Certificates will be saved to:
# /etc/letsencrypt/live/your-domain.com/fullchain.pem
# /etc/letsencrypt/live/your-domain.com/privkey.pem
```

### Step 11: Configure Nginx for SSL (Optional - if using host nginx)

If you want to use host nginx instead of Docker nginx:

```bash
# Create nginx config
nano /etc/nginx/sites-available/gameboosters
```

Paste this configuration:

```nginx
upstream web {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    client_max_body_size 50M;

    # Static files
    location /static/ {
        alias /opt/game-boosters/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Media files
    location /media/ {
        alias /opt/game-boosters/media/;
        expires 30d;
    }

    # WebSocket traffic
    location /ws/ {
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://web;
        proxy_read_timeout 86400;
    }

    # HTTP requests
    location / {
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://web;
        proxy_redirect off;
    }
}
```

Enable the site:
```bash
ln -s /etc/nginx/sites-available/gameboosters /etc/nginx/sites-enabled/
nginx -t
systemctl reload nginx
```

### Step 12: Update Docker Compose to Use Host Network (Optional)

If using host nginx, you can expose the web service to host:

Update `docker-compose.prod.yml` to expose port 8000 to host:
```yaml
web:
  ports:
    - "127.0.0.1:8000:8000"  # Only accessible from localhost
```

### Step 13: Set Up Auto-Start on Reboot

```bash
# Create systemd service for docker-compose
nano /etc/systemd/system/gameboosters.service
```

Paste this:

```ini
[Unit]
Description=GameBoosterss Docker Compose
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/game-boosters
ExecStart=/usr/local/bin/docker-compose -f docker-compose.prod.yml up -d
ExecStop=/usr/local/bin/docker-compose -f docker-compose.prod.yml down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
systemctl daemon-reload
systemctl enable gameboosters.service
systemctl start gameboosters.service
```

### Step 14: Verify Deployment

```bash
# Check all containers are running
docker-compose -f docker-compose.prod.yml ps

# Check logs
docker-compose -f docker-compose.prod.yml logs --tail=50

# Test website (should return HTTP 200)
curl http://localhost:8000

# Check if accessible from outside (from your local machine)
curl http://your-vps-ip:8000
```

## 🔧 Useful Commands

### View Logs
```bash
# All services
docker-compose -f docker-compose.prod.yml logs -f

# Specific service
docker-compose -f docker-compose.prod.yml logs -f web
docker-compose -f docker-compose.prod.yml logs -f db
```

### Restart Services
```bash
docker-compose -f docker-compose.prod.yml restart
```

### Stop Services
```bash
docker-compose -f docker-compose.prod.yml down
```

### Update Application
```bash
cd /opt/game-boosters
git pull origin main
docker-compose -f docker-compose.prod.yml up -d --build
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
```

### Backup Database
```bash
docker-compose -f docker-compose.prod.yml exec db pg_dump -U postgres gameboosters_db01 > backup_$(date +%Y%m%d).sql
```

## 🔒 Security Checklist

- [ ] Changed `SECRET_KEY` in `.env`
- [ ] Set `DEBUG=False` in production
- [ ] Used strong database password
- [ ] Configured firewall (UFW)
- [ ] Set up SSL/HTTPS certificate
- [ ] Updated `ALLOWED_HOSTS` in settings
- [ ] Secured `.env` file (chmod 600)
- [ ] Disabled root SSH login (if possible)
- [ ] Set up SSH key authentication

## 🐛 Troubleshooting

### Containers not starting
```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs

# Check container status
docker-compose -f docker-compose.prod.yml ps
docker ps -a
```

### Database connection issues
```bash
# Check database is running
docker-compose -f docker-compose.prod.yml exec db pg_isready -U postgres

# Check database logs
docker-compose -f docker-compose.prod.yml logs db
```

### Static files not loading
```bash
# Re-collect static files
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

# Check nginx volume mounts
docker-compose -f docker-compose.prod.yml exec nginx ls -la /app/staticfiles
```

### WebSocket not working
```bash
# Check Redis is running
docker-compose -f docker-compose.prod.yml exec redis redis-cli ping

# Check Redis logs
docker-compose -f docker-compose.prod.yml logs redis
```

## 📝 Notes

- Replace `your-domain.com` with your actual domain name
- Replace `/opt/game-boosters` with your actual project path
- Keep your `.env` file secure and never commit it to Git
- Regularly backup your database
- Monitor logs for errors
- Set up automatic SSL renewal: `certbot renew --dry-run`

## 🎉 Success!

Once all steps are complete, your application should be accessible at:
- HTTP: `http://your-domain.com`
- HTTPS: `https://your-domain.com` (after SSL setup)

Admin panel: `https://your-domain.com/admin/`

