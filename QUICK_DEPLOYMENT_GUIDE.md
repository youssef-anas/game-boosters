# 🚀 Quick Deployment Guide for Hostinger VPS

## Your VPS Details

- **VPS IP**: `46.202.131.43`
- **SSH Port**: `22`
- **Username**: `root`
- **Domain**: `madboost.gg`
- **SSH Key**: `C:\Users\youss\.ssh\id_rsa`

## 🎯 Option 1: Automated Deployment (Recommended)

### Using Git Bash (Windows)

1. **Open Git Bash** on your Windows machine

2. **Navigate to project directory**:
   ```bash
   cd /e/youssef_anas/game-boosters-main
   ```

3. **Make script executable and run**:
   ```bash
   chmod +x deploy-to-hostinger.sh
   ./deploy-to-hostinger.sh
   ```

   **Note**: You may need to install `sshpass` first:
   ```bash
   # On Windows, you might need to use WSL or install sshpass
   # Or use the manual method below
   ```

### Manual Deployment (Step-by-Step)

If automated script doesn't work, follow these steps manually:

#### Step 1: Connect to VPS

```bash
# In Git Bash
ssh -i /c/Users/youss/.ssh/id_rsa root@46.202.131.43
# Enter passphrase: 123456789
```

#### Step 2: Install Docker and Dependencies

Once connected to VPS, run:

```bash
# Update system
apt update && apt upgrade -y

# Install required packages
apt install -y curl git python3-pip nginx certbot python3-certbot-nginx

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
rm get-docker.sh

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Verify installation
docker --version
docker-compose --version
```

#### Step 3: Clone Repository

```bash
# Navigate to /opt
cd /opt

# Clone repository
git clone https://github.com/youssef-anas/game-boosters.git
cd game-boosters

# Verify you're in the right directory
ls -la
```

#### Step 4: Create .env File

```bash
nano .env
```

**Paste this content** (press `Ctrl+Shift+V` in nano, then `Ctrl+O` to save, `Enter` to confirm, `Ctrl+X` to exit):

```bash
# Django Settings
DEBUG=False
SECRET_KEY=your-django-secret-key-here
DOMAIN_NAME=madboost.gg

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
SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI=https://madboost.gg/social/complete/google-oauth2/

# Payment Configuration
PAYMENT_KEY=your-payment-key
MERCHANT_UUID=your-merchant-uuid
```

#### Step 5: Configure Firewall

```bash
# Allow necessary ports
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp

# Enable firewall
echo "y" | ufw enable

# Check status
ufw status
```

#### Step 6: Build and Start Docker Containers

```bash
# Make sure you're in the project directory
cd /opt/game-boosters

# Build and start containers
docker-compose -f docker-compose.prod.yml up -d --build

# Check status
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

Wait for all containers to start (check logs for any errors).

#### Step 7: Create Django Superuser

```bash
# Create admin user
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

# Follow prompts:
# Username: (your admin username)
# Email: (your email)
# Password: (strong password)
```

#### Step 8: Verify Deployment

```bash
# Check all containers are running
docker-compose -f docker-compose.prod.yml ps

# Test application
curl http://localhost:8000

# Check from outside (from your local machine)
curl http://46.202.131.43:8000
```

#### Step 9: Set Up SSL Certificate (After DNS is Configured)

**Important**: Make sure your domain `madboost.gg` DNS points to `46.202.131.43` before running this.

```bash
# Get SSL certificate
certbot certonly --standalone -d madboost.gg -d www.madboost.gg

# Certificates will be saved to:
# /etc/letsencrypt/live/madboost.gg/fullchain.pem
# /etc/letsencrypt/live/madboost.gg/privkey.pem
```

#### Step 10: Set Up Auto-Start on Reboot

```bash
# Create systemd service
cat > /etc/systemd/system/gameboosters.service << 'EOF'
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
EOF

# Enable and start service
systemctl daemon-reload
systemctl enable gameboosters.service
systemctl start gameboosters.service

# Verify service status
systemctl status gameboosters.service
```

## ✅ Verification Checklist

After deployment, verify:

- [ ] All containers are running: `docker-compose -f docker-compose.prod.yml ps`
- [ ] Application is accessible: `curl http://localhost:8000`
- [ ] Database is connected (check logs)
- [ ] Redis is running (check logs)
- [ ] Admin panel works: `https://madboost.gg/admin/`
- [ ] SSL certificate is installed (if DNS is configured)
- [ ] Auto-start service is enabled

## 🔧 Useful Commands

### View Logs
```bash
cd /opt/game-boosters
docker-compose -f docker-compose.prod.yml logs -f
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

## 🌐 Access Your Application

- **HTTP**: `http://46.202.131.43:8000`
- **HTTPS**: `https://madboost.gg` (after SSL setup)
- **Admin Panel**: `https://madboost.gg/admin/`

## 🔒 Security Notes

⚠️ **IMPORTANT**: 
- Change the `SECRET_KEY` in `.env` - generate a new one
- Change `DB_PASSWORD` to a stronger password
- Ensure `.env` file permissions: `chmod 600 .env`
- Set up firewall rules properly
- Keep SSH key secure

## 🆘 Troubleshooting

### Can't connect via SSH
- Verify SSH key path is correct
- Check passphrase is correct
- Verify VPS IP address
- Check firewall allows SSH (port 22)

### Containers not starting
```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs

# Check container status
docker ps -a
```

### Database connection issues
```bash
# Check database container
docker-compose -f docker-compose.prod.yml logs db

# Test database connection
docker-compose -f docker-compose.prod.yml exec db pg_isready -U postgres
```

---

## 📞 Need Help?

Refer to:
- `HOSTINGER_VPS_DEPLOYMENT.md` - Detailed deployment guide
- `DOCKER_DEPLOYMENT.md` - Docker-specific instructions

