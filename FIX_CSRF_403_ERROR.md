# 🔧 Fix CSRF 403 Error

## ❌ Why This Problem Happened

The **CSRF verification failed (403 Forbidden)** error occurred because:

1. **Missing `CSRF_TRUSTED_ORIGINS`**: Django requires this setting when accessing via IP address or domain
2. **IP Address Not in ALLOWED_HOSTS**: Your VPS IP `46.202.131.43` wasn't explicitly listed
3. **Syntax Errors**: Missing comma in `ALLOWED_HOSTS` list
4. **Wrong Format**: `ALLOWED_HOSTS` had URLs with `https://` which is incorrect (should be just domain names)

---

## ✅ What I Fixed

### 1. Fixed `ALLOWED_HOSTS`
- Added your VPS IP: `46.202.131.43`
- Fixed syntax errors (missing commas)
- Removed `https://` from domain names (should be just domain names)

### 2. Added `CSRF_TRUSTED_ORIGINS`
- Added `http://46.202.131.43` and `https://46.202.131.43`
- Added domain variants (with and without www)
- Added localhost for development

---

## 🚀 What You Need to Do Now

### Step 1: Push Changes to GitHub
```bash
# On your local machine
cd E:\youssef_anas\game-boosters-main
git add gameBoosterss/settings.py
git commit -m "Fix CSRF 403 error - add CSRF_TRUSTED_ORIGINS and fix ALLOWED_HOSTS"
git push origin main
```

### Step 2: Pull Changes on VPS
```bash
# SSH into VPS
ssh -i /c/Users/youss/.ssh/id_rsa root@46.202.131.43

# Navigate to project
cd /opt/game-boosters

# Pull latest changes
git pull origin main
```

### Step 3: Restart Docker Container
```bash
# Restart the web container to apply changes
docker-compose -f docker-compose.prod.yml restart web

# Or rebuild if needed
docker-compose -f docker-compose.prod.yml up -d --build web
```

### Step 4: Test Admin Login
- Go to: `http://46.202.131.43/admin/`
- You should now be able to log in without the 403 error!

---

## 🔧 Quick Fix (If You Can't Push to GitHub)

If you want to fix it directly on the VPS without pushing to GitHub:

### Option 1: Edit settings.py on VPS
```bash
# SSH into VPS
ssh -i /c/Users/youss/.ssh/id_rsa root@46.202.131.43
cd /opt/game-boosters

# Edit settings.py
nano gameBoosterss/settings.py
```

**Find this section (around line 238):**
```python
ALLOWED_HOSTS = [
    '8881-197-32-66-233.ngrok-free.app'
    'https://www.madboost.gg',
    ...
]
```

**Replace with:**
```python
# Get domain from environment or use defaults
DOMAIN_NAME = os.getenv('DOMAIN_NAME', 'madboost.gg')
VPS_IP = '46.202.131.43'  # Your VPS IP address

ALLOWED_HOSTS = [
    '8881-197-32-66-233.ngrok-free.app',
    'localhost',
    '127.0.0.1',
    VPS_IP,  # VPS IP address
    DOMAIN_NAME,
    f'www.{DOMAIN_NAME}',
    'www.madboost.gg',
    'madboost.gg',
    'gameboost-test-f25426e2eac4.herokuapp.com',
    'www.gameboost-test-f25426e2eac4.herokuapp.com',
    '*'  # Remove in production mode
]

# CSRF Trusted Origins - must include scheme (http:// or https://)
CSRF_TRUSTED_ORIGINS = [
    f'http://{VPS_IP}',
    f'https://{VPS_IP}',
    f'http://{DOMAIN_NAME}',
    f'https://{DOMAIN_NAME}',
    f'http://www.{DOMAIN_NAME}',
    f'https://www.{DOMAIN_NAME}',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]
```

**Save and exit** (Ctrl+O, Enter, Ctrl+X in nano)

**Restart container:**
```bash
docker-compose -f docker-compose.prod.yml restart web
```

---

## 🧪 Verify the Fix

### Test 1: Check if settings are correct
```bash
cd /opt/game-boosters
docker-compose -f docker-compose.prod.yml exec web python manage.py shell << 'PYEOF'
from django.conf import settings
print("ALLOWED_HOSTS:", settings.ALLOWED_HOSTS)
print("CSRF_TRUSTED_ORIGINS:", settings.CSRF_TRUSTED_ORIGINS)
PYEOF
```

**Expected output:**
```
ALLOWED_HOSTS: [..., '46.202.131.43', ...]
CSRF_TRUSTED_ORIGINS: ['http://46.202.131.43', 'https://46.202.131.43', ...]
```

### Test 2: Access Admin Panel
- Open: `http://46.202.131.43/admin/`
- You should see the login page (not 403 error)
- Try logging in with your admin credentials

---

## 📝 Summary

**Problem**: CSRF verification failed because:
- No `CSRF_TRUSTED_ORIGINS` configured
- IP address not in `ALLOWED_HOSTS`
- Syntax errors in `ALLOWED_HOSTS`

**Solution**: 
- Added `CSRF_TRUSTED_ORIGINS` with IP and domain
- Fixed `ALLOWED_HOSTS` to include IP address
- Fixed syntax errors

**Next Steps**:
1. Push changes to GitHub
2. Pull on VPS
3. Restart container
4. Test admin login

---

**Last Updated**: November 2024

