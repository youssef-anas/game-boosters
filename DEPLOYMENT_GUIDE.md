## GameBoosterss Production Deployment Guide (Hostinger VPS - Ubuntu)

### 1) Prerequisites
- Ubuntu 22.04 LTS on Hostinger VPS
- Domain pointing to server A record
- Packages: `python3.10+`, `python3-venv`, `nginx`, `postgresql`, `redis-server`, `certbot`, `python3-certbot-nginx`, `supervisor` or `systemd`

```bash
sudo apt update && sudo apt install -y python3-pip python3-venv nginx postgresql redis-server certbot python3-certbot-nginx
```

### 2) Clone and Setup
```bash
sudo mkdir -p /var/www/gameboosterss && sudo chown $USER:$USER /var/www/gameboosterss
cd /var/www/gameboosterss
git clone <YOUR_REPO_URL> .
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 3) .env Configuration
Create `.env` in project root:
```
DEBUG=False
SECRET_KEY=change-me
DOMAIN_NAME=your-domain.com

DB_NAME=gameboosters
DB_USER=gameboosters
DB_PASSWORD=strong-pass
DB_HOST=127.0.0.1
DB_PORT=5432
DB_CONN_MAX_AGE=60

USE_REDIS=True
REDIS_HOST=127.0.0.1
REDIS_PORT=6379

EMAIL_HOST_USER=no-reply@your-domain.com
EMAIL_HOST_PASSWORD=your-smtp-password
DEFAULT_FROM_EMAIL=no-reply@your-domain.com

MEDIA_URL=/media/
```

### 4) Database
```bash
sudo -u postgres psql <<SQL
CREATE DATABASE gameboosters;
CREATE USER gameboosters WITH PASSWORD 'strong-pass';
GRANT ALL PRIVILEGES ON DATABASE gameboosters TO gameboosters;
ALTER ROLE gameboosters SET client_encoding TO 'utf8';
ALTER ROLE gameboosters SET default_transaction_isolation TO 'read committed';
ALTER ROLE gameboosters SET timezone TO 'UTC';
SQL
```

### 5) Migrations & Static
```bash
source /var/www/gameboosterss/.venv/bin/activate
python manage.py migrate --noinput
python manage.py collectstatic --noinput
```

Static will be collected to `staticfiles/`. Create media dir:
```bash
mkdir -p /var/www/gameboosterss/media
```

### 6) Services
- Gunicorn (WSGI) on 127.0.0.1:8001
- Daphne (ASGI) on 127.0.0.1:8002

Create systemd units:

`/etc/systemd/system/gunicorn.service`
```
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/gameboosterss
Environment="PATH=/var/www/gameboosterss/.venv/bin"
ExecStart=/var/www/gameboosterss/.venv/bin/gunicorn gameBoosterss.wsgi:application --bind 127.0.0.1:8001 --workers 3
Restart=always

[Install]
WantedBy=multi-user.target
```

`/etc/systemd/system/daphne.service`
```
[Unit]
Description=Daphne ASGI Server
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/gameboosterss
Environment="PATH=/var/www/gameboosterss/.venv/bin"
ExecStart=/var/www/gameboosterss/.venv/bin/daphne -b 127.0.0.1 -p 8002 gameBoosterss.asgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

Reload and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now gunicorn daphne
```

### 7) Nginx
Copy template `deploy/nginx.conf.example` to `/etc/nginx/sites-available/gameboosterss` and edit domain/paths:
```bash
sudo ln -s /etc/nginx/sites-available/gameboosterss /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

### 8) SSL (Certbot)
```bash
sudo certbot --nginx -d your-domain.com -d www.your-domain.com --redirect
```

### 9) Redis
Ensure Redis starts on boot:
```bash
sudo systemctl enable --now redis-server
```

### 10) Email Verification
Use Django shell to send a test mail and check logs in `logs/email.log`.

### 11) Logs & Monitoring
- Logs: `logs/django.log`, `logs/realtime.log`, `logs/notifications.log`, `logs/email.log`
- Optional Sentry:
```
pip install sentry-sdk
# Initialize in wsgi/asgi if desired
```

### 12) Restart Services
```bash
sudo systemctl restart gunicorn daphne nginx
```

# Django App Deployment Guide for Hostinger VPS

This guide will help you deploy your Django game boosters application to Hostinger VPS.

## Prerequisites

- Hostinger VPS with Ubuntu 20.04/22.04
- SSH access to your VPS
- Domain name (optional but recommended)
- Basic knowledge of Linux commands

## Step 1: Connect to Your VPS

```bash
ssh root@your-vps-ip
```

## Step 2: Update System and Install Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3 python3-pip python3-venv nginx postgresql postgresql-contrib git curl wget unzip

# Install additional dependencies for psycopg2
sudo apt install -y libpq-dev python3-dev build-essential
```

## Step 3: Create a Non-Root User

```bash
# Create a new user
sudo adduser django
sudo usermod -aG sudo django

# Switch to the new user
su - django
```

## Step 4: Set Up PostgreSQL Database

```bash
# Switch to postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE gameboosters_db01;
CREATE USER gameboosters_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE gameboosters_db01 TO gameboosters_user;
ALTER USER gameboosters_user CREATEDB;
\q

# Test the connection
psql -h localhost -U gameboosters_user -d gameboosters_db01
```

## Step 5: Clone Your Project

```bash
# Navigate to home directory
cd /home/django

# Clone your repository (replace with your actual repo URL)
git clone https://github.com/yourusername/game-boosters-main.git
cd game-boosters-main
```

## Step 6: Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

## Step 7: Configure Environment Variables

```bash
# Create .env file
nano .env
```

Add the following environment variables:

```env
DEBUG=False
SECRET_KEY=your_very_secure_secret_key_here
DB_NAME=gameboosters_db01
DB_USER=gameboosters_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
EMAIL_HOST_USER=your_email@domain.com
EMAIL_HOST_PASSWORD=your_email_password
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=your_google_oauth_key
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=your_google_oauth_secret
SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI=https://yourdomain.com/social/complete/google-oauth2/
PAYMENT_KEY=your_payment_key
MERCHANT_UUID=your_merchant_uuid
```

## Step 8: Configure Django Settings

Edit `gameBoosterss/settings.py`:

```python
# Update ALLOWED_HOSTS
ALLOWED_HOSTS = [
    'yourdomain.com',
    'www.yourdomain.com',
    'your-vps-ip',
    'localhost',
    '127.0.0.1',
]

# Update CORS_ORIGIN_WHITELIST
CORS_ORIGIN_WHITELIST = [
    'https://yourdomain.com',
    'https://www.yourdomain.com',
]

# Update social auth redirect URLs
SOCIAL_AUTH_LOGIN_ERROR_URL = 'https://yourdomain.com/social-auth-exception/'
SOCIAL_AUTH_FACEBOOK_DEAUTHORIZATION_CALLBACK_URL = "https://yourdomain.com/facebook-data-deletion/"
```

## Step 9: Run Django Migrations

```bash
# Activate virtual environment
source venv/bin/activate

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

## Step 10: Set Up Gunicorn

```bash
# Install gunicorn
pip install gunicorn

# Create gunicorn configuration
nano gunicorn_config.py
```

Add the following configuration:

```python
# gunicorn_config.py
bind = "127.0.0.1:8000"
workers = 3
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 50
preload_app = True
```

## Step 11: Create Systemd Service

```bash
# Create systemd service file
sudo nano /etc/systemd/system/gameboosters.service
```

Add the following content:

```ini
[Unit]
Description=Game Boosters Django Application
After=network.target

[Service]
Type=notify
User=django
Group=django
WorkingDirectory=/home/django/game-boosters-main
Environment=PATH=/home/django/game-boosters-main/venv/bin
ExecStart=/home/django/game-boosters-main/venv/bin/gunicorn --config gunicorn_config.py gameBoosterss.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

## Step 12: Configure Nginx

```bash
# Create nginx configuration
sudo nano /etc/nginx/sites-available/gameboosters
```

Add the following configuration:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com your-vps-ip;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

    # Static files
    location /static/ {
        alias /home/django/game-boosters-main/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Media files (if not using cloud storage)
    location /media/ {
        alias /home/django/game-boosters-main/media/;
        expires 30d;
    }

    # Proxy to Django
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied expired no-cache no-store private must-revalidate auth;
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss;
}
```

## Step 13: Enable and Start Services

```bash
# Enable nginx site
sudo ln -s /etc/nginx/sites-available/gameboosters /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default  # Remove default site

# Test nginx configuration
sudo nginx -t

# Start and enable services
sudo systemctl start gameboosters
sudo systemctl enable gameboosters
sudo systemctl restart nginx

# Check status
sudo systemctl status gameboosters
sudo systemctl status nginx
```

## Step 14: Set Up SSL with Let's Encrypt

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Set up auto-renewal
sudo crontab -e
```

Add this line for auto-renewal:
```
0 12 * * * /usr/bin/certbot renew --quiet
```

## Step 15: Configure Firewall

```bash
# Install ufw if not installed
sudo apt install ufw

# Configure firewall
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

## Step 16: Set Up Logging

```bash
# Create log directory
sudo mkdir -p /var/log/gameboosters
sudo chown django:django /var/log/gameboosters

# Update gunicorn config to include logging
nano gunicorn_config.py
```

Add logging configuration:

```python
# gunicorn_config.py
bind = "127.0.0.1:8000"
workers = 3
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 50
preload_app = True

# Logging
accesslog = "/var/log/gameboosters/access.log"
errorlog = "/var/log/gameboosters/error.log"
loglevel = "info"
```

## Step 17: Set Up Database Backup

```bash
# Create backup script
nano /home/django/backup.sh
```

Add the following content:

```bash
#!/bin/bash
BACKUP_DIR="/home/django/backups"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="gameboosters_db01"
DB_USER="gameboosters_user"

# Create backup directory
mkdir -p $BACKUP_DIR

# Create database backup
pg_dump -h localhost -U $DB_USER $DB_NAME > $BACKUP_DIR/backup_$DATE.sql

# Compress backup
gzip $BACKUP_DIR/backup_$DATE.sql

# Keep only last 7 days of backups
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +7 -delete
```

```bash
# Make script executable
chmod +x /home/django/backup.sh

# Add to crontab for daily backups
crontab -e
```

Add this line:
```
0 2 * * * /home/django/backup.sh
```

## Step 18: Monitor and Maintenance

### Check Application Status
```bash
# Check service status
sudo systemctl status gameboosters

# Check nginx status
sudo systemctl status nginx

# Check logs
sudo tail -f /var/log/gameboosters/error.log
sudo tail -f /var/log/nginx/error.log
```

### Update Application
```bash
# Pull latest changes
cd /home/django/game-boosters-main
git pull

# Activate virtual environment
source venv/bin/activate

# Install new dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart service
sudo systemctl restart gameboosters
```

## Troubleshooting

### Common Issues:

1. **Permission Denied**: Make sure the django user owns the project directory
   ```bash
   sudo chown -R django:django /home/django/game-boosters-main
   ```

2. **Database Connection**: Check PostgreSQL is running and accessible
   ```bash
   sudo systemctl status postgresql
   ```

3. **Static Files Not Loading**: Ensure static files are collected and nginx can access them
   ```bash
   python manage.py collectstatic --noinput
   sudo chown -R www-data:www-data /home/django/game-boosters-main/staticfiles
   ```

4. **WebSocket Issues**: Ensure nginx is configured for WebSocket support (already included in the config above)

## Security Considerations

1. **Keep system updated**: Regularly update your VPS
2. **Use strong passwords**: For database, Django admin, and SSH
3. **Regular backups**: Ensure database backups are working
4. **Monitor logs**: Check for suspicious activity
5. **Use HTTPS**: Always use SSL certificates
6. **Firewall**: Keep firewall rules strict

## Performance Optimization

1. **Database**: Consider using connection pooling with PgBouncer for high traffic
2. **Caching**: Implement Redis for caching if needed
3. **CDN**: Use a CDN for static files
4. **Monitoring**: Set up monitoring tools like New Relic or DataDog

Your Django application should now be successfully deployed on Hostinger VPS! 