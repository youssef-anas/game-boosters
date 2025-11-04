# SSL/HTTPS Setup Guide for GameBoosters VPS

This guide will help you set up HTTPS with Let's Encrypt SSL certificates on your Hostinger VPS.

## Prerequisites

- Your Django application running on the VPS
- A domain name pointing to your VPS IP
- Docker and Docker Compose already installed
- Port 80 and 443 open in your firewall

## Method 1: Using Certbot with Docker (Recommended)

### Step 1: Stop Nginx Container Temporarily

```bash
# Navigate to your project directory
cd /home/django/game-boosters-main

# Stop the nginx container to free up port 80
docker-compose -f docker-compose.prod.yml stop nginx
```

### Step 2: Create SSL Directory

```bash
# Create SSL directory
mkdir -p ssl
```

### Step 3: Get SSL Certificate with Certbot

```bash
# Run certbot to get SSL certificate
docker run -it --rm \
  -v $(pwd)/ssl:/etc/letsencrypt \
  -v $(pwd)/ssl:/var/lib/letsencrypt \
  -p 80:80 \
  -p 443:443 \
  certbot/certbot certonly \
  --standalone \
  --email your-email@domain.com \
  --agree-tos \
  --no-eff-email \
  -d yourdomain.com \
  -d www.yourdomain.com
```

### Step 4: Copy Certificates

```bash
# Copy certificates to nginx SSL directory
cp ssl/live/yourdomain.com/fullchain.pem ssl/cert.pem
cp ssl/live/yourdomain.com/privkey.pem ssl/key.pem

# Set proper permissions
chmod 600 ssl/cert.pem ssl/key.pem
```

### Step 5: Update Nginx Configuration

Edit your `nginx.conf` file to enable HTTPS:

```bash
nano nginx.conf
```

Uncomment and update the HTTPS server block:

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

    # Redirect HTTP to HTTPS
    server {
        listen 80;
        server_name yourdomain.com www.yourdomain.com;
        return 301 https://$server_name$request_uri;
    }

    # HTTPS server
    server {
        listen 443 ssl http2;
        server_name yourdomain.com www.yourdomain.com;

        # SSL configuration
        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        
        # SSL security settings
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-SHA256:ECDHE-RSA-AES256-SHA384;
        ssl_prefer_server_ciphers off;
        ssl_session_cache shared:SSL:10m;
        ssl_session_timeout 10m;
        
        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header Referrer-Policy "no-referrer-when-downgrade" always;
        add_header Content-Security-Policy "default-src 'self' https: data: blob: 'unsafe-inline'" always;
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

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
}
```

### Step 6: Restart Services

```bash
# Start nginx container with new configuration
docker-compose -f docker-compose.prod.yml up -d nginx

# Check if everything is working
docker-compose -f docker-compose.prod.yml ps
docker-compose -f docker-compose.prod.yml logs nginx
```

## Method 2: Using Certbot with Nginx Plugin (Alternative)

If you prefer to use the nginx plugin, you can modify the approach:

### Step 1: Create a Temporary Nginx Container for Certbot

```bash
# Create a temporary nginx container for certbot
docker run -d --name nginx-temp \
  -p 80:80 \
  -v $(pwd)/nginx-temp.conf:/etc/nginx/nginx.conf:ro \
  nginx:alpine
```

### Step 2: Create Temporary Nginx Config

```bash
nano nginx-temp.conf
```

Add this content:

```nginx
events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    server {
        listen 80;
        server_name yourdomain.com www.yourdomain.com;
        
        location /.well-known/acme-challenge/ {
            root /var/www/certbot;
        }
        
        location / {
            return 301 https://$server_name$request_uri;
        }
    }
}
```

### Step 3: Get Certificate with Nginx Plugin

```bash
# Stop temporary nginx
docker stop nginx-temp
docker rm nginx-temp

# Get certificate using nginx plugin
docker run -it --rm \
  -v $(pwd)/ssl:/etc/letsencrypt \
  -v $(pwd)/ssl:/var/lib/letsencrypt \
  -v $(pwd)/nginx-temp.conf:/etc/nginx/nginx.conf:ro \
  -p 80:80 \
  certbot/certbot certonly \
  --nginx \
  --email your-email@domain.com \
  --agree-tos \
  --no-eff-email \
  -d yourdomain.com \
  -d www.yourdomain.com
```

## Method 3: Using Hostinger's Built-in SSL (If Available)

If your Hostinger VPS plan includes SSL certificates:

### Step 1: Access Hostinger Control Panel

1. Log in to your Hostinger control panel
2. Navigate to the SSL section
3. Generate a free SSL certificate for your domain

### Step 2: Download Certificates

Download the certificate files and place them in your `ssl` directory:

```bash
# Create ssl directory
mkdir -p ssl

# Copy your downloaded certificates
cp /path/to/your/certificate.crt ssl/cert.pem
cp /path/to/your/private.key ssl/key.pem

# Set proper permissions
chmod 600 ssl/cert.pem ssl/key.pem
```

## Auto-Renewal Setup

### Step 1: Create Renewal Script

```bash
nano ssl_renew.sh
```

Add this content:

```bash
#!/bin/bash

# SSL Certificate Renewal Script

set -e

echo "Starting SSL certificate renewal..."

# Navigate to project directory
cd /home/django/game-boosters-main

# Stop nginx container
docker-compose -f docker-compose.prod.yml stop nginx

# Renew certificate
docker run --rm \
  -v $(pwd)/ssl:/etc/letsencrypt \
  -v $(pwd)/ssl:/var/lib/letsencrypt \
  -p 80:80 \
  -p 443:443 \
  certbot/certbot renew \
  --standalone \
  --quiet

# Copy renewed certificates
cp ssl/live/yourdomain.com/fullchain.pem ssl/cert.pem
cp ssl/live/yourdomain.com/privkey.pem ssl/key.pem

# Set proper permissions
chmod 600 ssl/cert.pem ssl/key.pem

# Restart nginx
docker-compose -f docker-compose.prod.yml up -d nginx

echo "SSL certificate renewal completed!"
```

### Step 2: Make Script Executable

```bash
chmod +x ssl_renew.sh
```

### Step 3: Add to Crontab

```bash
# Add to crontab for automatic renewal (runs twice daily)
crontab -e
```

Add this line:

```
0 12,18 * * * /home/django/game-boosters-main/ssl_renew.sh >> /home/django/ssl_renew.log 2>&1
```

## Testing SSL Setup

### Step 1: Test Certificate

```bash
# Test SSL certificate
openssl s_client -connect yourdomain.com:443 -servername yourdomain.com
```

### Step 2: Check SSL Grade

Visit [SSL Labs](https://www.ssllabs.com/ssltest/) and enter your domain to check your SSL grade.

### Step 3: Test HTTPS Redirect

```bash
# Test HTTP to HTTPS redirect
curl -I http://yourdomain.com
```

You should see a 301 redirect to HTTPS.

## Troubleshooting

### Common Issues:

1. **Certificate Not Found**: Make sure the certificate files exist and have correct permissions
   ```bash
   ls -la ssl/
   ```

2. **Nginx Won't Start**: Check nginx configuration
   ```bash
   docker-compose -f docker-compose.prod.yml logs nginx
   ```

3. **Port 80/443 Already in Use**: Stop other services using these ports
   ```bash
   sudo netstat -tlnp | grep :80
   sudo netstat -tlnp | grep :443
   ```

4. **Domain Not Resolving**: Ensure your domain points to your VPS IP
   ```bash
   nslookup yourdomain.com
   ```

### SSL Configuration Best Practices:

1. **Use Strong Ciphers**: The configuration includes modern, secure ciphers
2. **HSTS Header**: Includes HSTS header for additional security
3. **OCSP Stapling**: Consider enabling OCSP stapling for better performance
4. **Regular Renewal**: Set up automatic renewal to prevent certificate expiration

## Security Considerations

1. **Keep Certificates Secure**: Ensure certificate files have proper permissions (600)
2. **Monitor Expiration**: Set up monitoring for certificate expiration
3. **Backup Certificates**: Keep backups of your SSL certificates
4. **Update Regularly**: Keep certbot and nginx updated

Your Django application should now be accessible via HTTPS with a valid SSL certificate! 