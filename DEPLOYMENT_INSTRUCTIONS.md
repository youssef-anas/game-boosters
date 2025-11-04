# 🚀 Quick Deployment Instructions

## Option 1: Use the Simple Script (Recommended)

The script `deploy-simple.sh` uses SSH directly and will prompt you for your passphrase when needed.

### Run the script:

```bash
# In Git Bash
cd /e/youssef_anas/game-boosters-main
chmod +x deploy-simple.sh
./deploy-simple.sh
```

**You'll be prompted for your SSH key passphrase (`123456789`) when connecting.**

---

## Option 2: Use SSH Agent (One-time passphrase entry)

If you want to enter the passphrase only once, use SSH agent:

```bash
# Start SSH agent
eval "$(ssh-agent -s)"

# Add your SSH key (enter passphrase: 123456789)
ssh-add /c/Users/youss/.ssh/id_rsa

# Now run the deployment script
chmod +x deploy-to-hostinger.sh
./deploy-to-hostinger.sh
```

---

## Option 3: Manual Deployment (Most Reliable)

If scripts don't work, follow these manual steps:

### Step 1: Connect to VPS

```bash
# In Git Bash
ssh -i /c/Users/youss/.ssh/id_rsa root@46.202.131.43
# Enter passphrase when prompted: 123456789
```

### Step 2: Once connected, run these commands on the VPS:

```bash
# 1. Install Docker and dependencies
apt update && apt upgrade -y
apt install -y curl git python3-pip nginx certbot python3-certbot-nginx
curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh && rm get-docker.sh
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# 2. Clone repository
cd /opt
git clone https://github.com/youssef-anas/game-boosters.git
cd game-boosters

# 3. Create .env file
nano .env
# Paste the content from QUICK_DEPLOYMENT_GUIDE.md

# 4. Configure firewall
ufw allow 22/tcp && ufw allow 80/tcp && ufw allow 443/tcp
echo "y" | ufw enable

# 5. Build and start containers
docker-compose -f docker-compose.prod.yml up -d --build

# 6. Check status
docker-compose -f docker-compose.prod.yml ps
docker-compose -f docker-compose.prod.yml logs -f

# 7. Create superuser
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

---

## Quick Test Connection

Before running the full script, test your SSH connection:

```bash
# In Git Bash
ssh -i /c/Users/youss/.ssh/id_rsa root@46.202.131.43
# Enter passphrase: 123456789
```

If this works, the deployment script should work too.

---

## Troubleshooting

### SSH key not found
- Make sure the path is correct: `/c/Users/youss/.ssh/id_rsa`
- In Git Bash, Windows paths start with `/c/`

### Passphrase prompt not working
- Try using SSH agent (Option 2 above)
- Or use manual deployment (Option 3)

### Connection refused
- Check VPS IP: `46.202.131.43`
- Verify SSH port: `22`
- Check Hostinger firewall allows SSH

---

## Recommended: Use Option 3 (Manual)

The manual deployment is the most reliable method. Just:
1. Connect via SSH
2. Copy-paste the commands one by one
3. Monitor the output

This gives you full control and visibility over each step.

