# Docker Deployment Guide for Hostinger VPS

This guide will help you deploy your Django game boosters application to Hostinger VPS using Docker and Docker Compose.

## Prerequisites

- Hostinger VPS with Ubuntu 20.04/22.04
- SSH access to your VPS
- Domain name (optional but recommended)
- Basic knowledge of Linux and Docker commands

## Step 1: Connect to Your VPS

```bash
ssh root@your-vps-ip
```

## Step 2: Update System and Install Docker

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y curl wget git unzip

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add current user to docker group
sudo usermod -aG docker $USER

# Start and enable Docker
sudo systemctl start docker
sudo systemctl enable docker

# Logout and login again to apply group changes, or run:
newgrp docker
```

## Step 3: Create a Non-Root User (Optional but Recommended)

```bash
# Create a new user
sudo adduser django
sudo usermod -aG sudo django
sudo usermod -aG docker django

# Switch to the new user
su - django
```

## Step 4: Clone Your Project

```bash
# Navigate to home directory
cd /home/django

# Clone your repository (replace with your actual repo URL)
git clone https://github.com/yourusername/game-boosters-main.git
cd game-boosters-main
```

## Step 5: Create Production Environment File

```bash
# Create .env file for production
nano .env
```

Add the following environment variables:

```env
DEBUG=False
SECRET_KEY=your_very_secure_secret_key_here
DB_NAME=gameboosters_db01
DB_USER=postgres
DB_PASSWORD=your_secure_password
DB_HOST=db
EMAIL_HOST_USER=your_email@domain.com
EMAIL_HOST_PASSWORD=your_email_password
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=your_google_oauth_key
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=your_google_oauth_secret
SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI=https://yourdomain.com/social/complete/google-oauth2/
PAYMENT_KEY=your_payment_key
MERCHANT_UUID=your_merchant_uuid
```

## Step 6: Update Docker Compose for Production

Create a production Docker Compose file:

```bash
nano docker-compose.prod.yml
```

Add the following content:

```yaml
version: '3.8'

services:
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: gameboosters_db01
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      PGDATA: /var/lib/postgresql/data/pgdata
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backup.sql:/docker-entrypoint-initdb.d/backup.sql:ro
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5
      start_period: 10s
    restart: unless-stopped
    networks:
      - gameboosters_network

  web:
    build: .
    command: >
      bash -c "set -e;
      while ! pg_isready -h db -U postgres -t 5; do
        echo 'Waiting for database...';
        sleep 2;
      done;
      python manage.py migrate;
      python manage.py collectstatic --noinput;
      gunicorn --bind 0.0.0.0:8000 --workers 3 --timeout 30 gameBoosterss.wsgi:application"
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy
    environment:
      - DB_HOST=db
      - DB_NAME=${DB_NAME}
      - DB_USER=${DB_USER}
      - DB_PASSWORD=${DB_PASSWORD}
      - DEBUG=${DEBUG}
      - SECRET_KEY=${SECRET_KEY}
      - EMAIL_HOST_USER=${EMAIL_HOST_USER}
      - EMAIL_HOST_PASSWORD=${EMAIL_HOST_PASSWORD}
      - SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=${SOCIAL_AUTH_GOOGLE_OAUTH2_KEY}
      - SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=${SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET}
      - SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI=${SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI}
      - PAYMENT_KEY=${PAYMENT_KEY}
      - MERCHANT_UUID=${MERCHANT_UUID}
    restart: unless-stopped
    networks:
      - gameboosters_network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - static_volume:/app/staticfiles
      - media_volume:/app/media
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - web
    restart: unless-stopped
    networks:
      - gameboosters_network

volumes:
  postgres_data:
  static_volume:
  media_volume:

networks:
  gameboosters_network:
    driver: bridge
```

## Step 7: Create Nginx Configuration for Docker

```bash
nano nginx.conf
```

Add the following content:

```nginx
events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Logging
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;
    error_log /var/log/nginx/error.log;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied expired no-cache no-store private must-revalidate auth;
    gzip_types 
        text/plain 
        text/css 
        text/xml 
        text/javascript 
        application/x-javascript 
        application/xml+rss 
        application/javascript 
        application/json 
        image/svg+xml;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=login:10m rate=1r/s;

    server {
        listen 80;
        server_name yourdomain.com www.yourdomain.com your-vps-ip;

        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header Referrer-Policy "no-referrer-when-downgrade" always;
        add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

        # Client max body size
        client_max_body_size 10M;

        # Static files
        location /static/ {
            alias /app/staticfiles/;
            expires 30d;
            add_header Cache-Control "public, immutable";
            access_log off;
        }

        # Media files
        location /media/ {
            alias /app/media/;
            expires 30d;
            add_header Cache-Control "public";
            access_log off;
        }

        # Rate limiting for API endpoints
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            proxy_pass http://web:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_redirect off;
        }

        # Rate limiting for login endpoints
        location ~ ^/(login|register|password-reset)/ {
            limit_req zone=login burst=5 nodelay;
            proxy_pass http://web:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_redirect off;
        }

        # WebSocket support
        location /ws/ {
            proxy_pass http://web:8000;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_read_timeout 86400;
        }

        # Main application
        location / {
            proxy_pass http://web:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_redirect off;
            
            # Timeouts
            proxy_connect_timeout 60s;
            proxy_send_timeout 60s;
            proxy_read_timeout 60s;
        }

        # Health check
        location /health/ {
            access_log off;
            return 200 "healthy\n";
            add_header Content-Type text/plain;
        }
    }

    # HTTPS configuration (uncomment after SSL setup)
    # server {
    #     listen 443 ssl http2;
    #     server_name yourdomain.com www.yourdomain.com;
    #     
    #     ssl_certificate /etc/nginx/ssl/cert.pem;
    #     ssl_certificate_key /etc/nginx/ssl/key.pem;
    #     
    #     # SSL configuration
    #     ssl_protocols TLSv1.2 TLSv1.3;
    #     ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;
    #     ssl_prefer_server_ciphers off;
    #     
    #     # Same location blocks as above...
    # }
}
```

## Step 8: Build and Start the Application

```bash
# Build the Docker images
docker-compose -f docker-compose.prod.yml build

# Start the services
docker-compose -f docker-compose.prod.yml up -d

# Check the status
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

## Step 9: Create Superuser

```bash
# Create superuser
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

## Step 10: Set Up SSL with Let's Encrypt (Optional)

If you want SSL, you can use Certbot with Docker:

```bash
# Create SSL directory
mkdir -p ssl

# Run certbot to get SSL certificate
docker run -it --rm \
  -v $(pwd)/ssl:/etc/letsencrypt \
  -v $(pwd)/ssl:/var/lib/letsencrypt \
  certbot/certbot certonly \
  --standalone \
  -d yourdomain.com \
  -d www.yourdomain.com

# Copy certificates to nginx SSL directory
cp ssl/live/yourdomain.com/fullchain.pem ssl/cert.pem
cp ssl/live/yourdomain.com/privkey.pem ssl/key.pem
```

Then uncomment the HTTPS server block in `nginx.conf` and restart:

```bash
docker-compose -f docker-compose.prod.yml restart nginx
```

## Step 11: Set Up Automatic Backups

Create a backup script:

```bash
nano backup.sh
```

Add the following content:

```bash
#!/bin/bash
BACKUP_DIR="/home/django/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Create database backup
docker-compose -f docker-compose.prod.yml exec -T db pg_dump -U postgres gameboosters_db01 > $BACKUP_DIR/backup_$DATE.sql

# Compress backup
gzip $BACKUP_DIR/backup_$DATE.sql

# Keep only last 7 days of backups
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +7 -delete

echo "Backup completed: backup_$DATE.sql.gz"
```

```bash
# Make script executable
chmod +x backup.sh

# Add to crontab for daily backups
crontab -e
```

Add this line:
```
0 2 * * * /home/django/game-boosters-main/backup.sh
```

## Step 12: Create Deployment Script

```bash
nano deploy.sh
```

Add the following content:

```bash
#!/bin/bash

# GameBoosters Docker Deployment Script

set -e

echo "Starting deployment..."

# Pull latest changes
git pull origin main || git pull origin master

# Create backup
./backup.sh

# Build and restart services
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

# Run migrations
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# Collect static files
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

echo "Deployment completed successfully!"
```

```bash
# Make script executable
chmod +x deploy.sh
```

## Step 13: Configure Firewall

```bash
# Install ufw if not installed
sudo apt install ufw

# Configure firewall
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

## Step 14: Monitor and Maintenance

### Check Application Status
```bash
# Check container status
docker-compose -f docker-compose.prod.yml ps

# Check logs
docker-compose -f docker-compose.prod.yml logs -f web
docker-compose -f docker-compose.prod.yml logs -f nginx

# Check resource usage
docker stats
```

### Update Application
```bash
# Run deployment script
./deploy.sh
```

### Database Operations
```bash
# Access database
docker-compose -f docker-compose.prod.yml exec db psql -U postgres -d gameboosters_db01

# Run Django management commands
docker-compose -f docker-compose.prod.yml exec web python manage.py shell
```

## Troubleshooting

### Common Issues:

1. **Permission Denied**: Make sure the user has proper permissions
   ```bash
   sudo chown -R $USER:$USER /home/django/game-boosters-main
   ```

2. **Database Connection**: Check if database container is running
   ```bash
   docker-compose -f docker-compose.prod.yml logs db
   ```

3. **Static Files Not Loading**: Ensure static files are collected
   ```bash
   docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
   ```

4. **Port Already in Use**: Check if port 80 is available
   ```bash
   sudo netstat -tlnp | grep :80
   ```

## Security Considerations

1. **Keep Docker updated**: Regularly update Docker and images
2. **Use strong passwords**: For database and Django admin
3. **Regular backups**: Ensure database backups are working
4. **Monitor logs**: Check for suspicious activity
5. **Use HTTPS**: Always use SSL certificates in production
6. **Firewall**: Keep firewall rules strict

## Performance Optimization

1. **Database**: Consider using connection pooling
2. **Caching**: Implement Redis for caching if needed
3. **CDN**: Use a CDN for static files
4. **Monitoring**: Set up monitoring tools

Your Django application should now be successfully deployed on Hostinger VPS using Docker! 