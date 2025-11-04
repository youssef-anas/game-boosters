# 🐳 Docker Deployment Guide for GameBoosterss

## 📋 Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- Git
- Hostinger VPS with Ubuntu 20.04+ or similar

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/youssef-anas/game-boosters.git
cd game-boosters
```

### 2. Create `.env` File

Copy the example and configure:

```bash
# Create .env from template
cat > .env << 'EOF'
# Django Settings
DEBUG=False
SECRET_KEY=your-very-secure-secret-key-here
DOMAIN_NAME=your-domain.com

# Database Configuration
DB_NAME=gameboosters_db01
DB_USER=postgres
DB_PASSWORD=your-strong-database-password
DB_HOST=db
DB_PORT=5432

# Redis Configuration
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

# Edit the .env file with your actual values
nano .env
```

### 3. Build and Start Services

```bash
# Build and start all services
docker-compose -f docker-compose.prod.yml up -d --build

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Check service status
docker-compose -f docker-compose.prod.yml ps
```

### 4. Run Initial Setup

```bash
# Create superuser (optional)
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

# Run migrations (already done in entrypoint, but can run manually)
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# Collect static files (already done in entrypoint)
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
```

## 🔧 Service Management

### Start Services
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Stop Services
```bash
docker-compose -f docker-compose.prod.yml down
```

### Restart Services
```bash
docker-compose -f docker-compose.prod.yml restart
```

### View Logs
```bash
# All services
docker-compose -f docker-compose.prod.yml logs -f

# Specific service
docker-compose -f docker-compose.prod.yml logs -f web
docker-compose -f docker-compose.prod.yml logs -f db
docker-compose -f docker-compose.prod.yml logs -f redis
docker-compose -f docker-compose.prod.yml logs -f nginx
```

### Execute Commands in Container
```bash
# Django shell
docker-compose -f docker-compose.prod.yml exec web python manage.py shell

# Run migrations
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# Create superuser
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

# Access container shell
docker-compose -f docker-compose.prod.yml exec web bash
```

## 📁 Project Structure

```
game-boosters/
├── Dockerfile                 # Production Docker image
├── docker-compose.prod.yml    # Production compose file
├── docker-entrypoint.sh       # Container entrypoint script
├── .env                       # Environment variables (create this)
├── .dockerignore             # Files to exclude from build
├── nginx.conf                # Nginx configuration for Docker
├── requirements.txt          # Python dependencies
└── manage.py                 # Django management script
```

## 🔒 Security Checklist

- [ ] Change `SECRET_KEY` in `.env`
- [ ] Use strong database password
- [ ] Set `DEBUG=False` in production
- [ ] Configure proper `ALLOWED_HOSTS` in settings
- [ ] Set up SSL/HTTPS (use Certbot with nginx)
- [ ] Secure email credentials
- [ ] Review `.env` file permissions (should be 600)

## 🌐 Nginx & SSL Setup

### Install Certbot (on host)

```bash
sudo apt update
sudo apt install certbot python3-certbot-nginx
```

### Get SSL Certificate

```bash
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

### Update Nginx Config

The nginx config in `nginx.conf` is for Docker. For production with SSL, you may need to:

1. Mount SSL certificates as volumes
2. Update nginx.conf to use SSL
3. Or use host nginx with reverse proxy to Docker

## 📊 Monitoring & Maintenance

### Check Container Health
```bash
docker-compose -f docker-compose.prod.yml ps
```

### View Resource Usage
```bash
docker stats
```

### Backup Database
```bash
docker-compose -f docker-compose.prod.yml exec db pg_dump -U postgres gameboosters_db01 > backup_$(date +%Y%m%d).sql
```

### Restore Database
```bash
docker-compose -f docker-compose.prod.yml exec -T db psql -U postgres gameboosters_db01 < backup.sql
```

## 🐛 Troubleshooting

### Container won't start
```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs web

# Check if database is ready
docker-compose -f docker-compose.prod.yml exec db pg_isready -U postgres
```

### Database connection issues
- Verify `DB_HOST=db` in `.env`
- Check database container is running: `docker-compose ps`
- Verify database credentials in `.env`

### Static files not loading
```bash
# Re-collect static files
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

# Check nginx volume mounts
docker-compose -f docker-compose.prod.yml exec nginx ls -la /app/staticfiles
```

### WebSocket issues
- Verify Redis is running: `docker-compose ps redis`
- Check `REDIS_HOST=redis` in `.env`
- Verify nginx WebSocket configuration

## 🚀 Production Deployment on Hostinger VPS

1. **SSH into your VPS**
   ```bash
   ssh user@your-vps-ip
   ```

2. **Install Docker**
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo usermod -aG docker $USER
   ```

3. **Install Docker Compose**
   ```bash
   sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```

4. **Clone and deploy**
   ```bash
   git clone https://github.com/youssef-anas/game-boosters.git
   cd game-boosters
   # Create .env file
   nano .env
   # Build and start
   docker-compose -f docker-compose.prod.yml up -d --build
   ```

5. **Set up firewall**
   ```bash
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw allow 22/tcp
   sudo ufw enable
   ```

## 📝 Notes

- The application runs on port 8000 inside the container
- Nginx proxies traffic from ports 80/443 to the web container
- Static and media files are served via Docker volumes
- Database and Redis data persist in Docker volumes
- Logs are stored in `./logs` directory (mounted as volume)

## 🔄 Updates

To update the application:

```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose -f docker-compose.prod.yml up -d --build

# Run migrations if needed
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
```

