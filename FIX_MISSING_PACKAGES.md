# 🔧 Fix: Missing Packages

## Problem

Django settings requires several packages that aren't installed:
- `jazzmin` (django-jazzmin)
- `firebase_admin` (firebase-admin)
- `paypalrestsdk` (paypalrestsdk)
- And possibly others

## Quick Solution

### Option 1: Install Missing Packages (Recommended)

**Run this command:**
```powershell
pip install django-jazzmin django-cleanup django-phonenumber-field django-countries social-auth-app-django pillow
```

**Or use the batch script:**
```powershell
.\install_missing_packages.bat
```

---

### Option 2: Install All Optional Packages

**Install packages that might be needed:**
```powershell
pip install django-jazzmin
pip install django-cleanup
pip install django-phonenumber-field
pip install django-countries
pip install social-auth-app-django
pip install pillow
pip install firebase-admin
pip install paypalrestsdk
pip install cryptomus
pip install faker
pip install captcha
```

---

### Option 3: Install Only Essential for Real-Time Sync

**If you just want to test real-time sync, install minimum:**
```powershell
pip install django-jazzmin
pip install django-cleanup
pip install django-phonenumber-field
pip install django-countries
pip install social-auth-app-django
pip install pillow
```

**Note:** Firebase and PayPal are now optional - they won't break Django if not installed.

---

## After Installing Packages

**Run these commands:**

```powershell
# 1. Verify setup
python verify_realtime_setup.py

# 2. Apply migrations
python manage.py migrate --noinput

# 3. Start server
daphne -b 0.0.0.0 -p 8000 gameBoosterss.asgi:application
```

---

## Quick Fix Commands

**Copy and paste these:**

```powershell
# Install missing packages
pip install django-jazzmin django-cleanup django-phonenumber-field django-countries social-auth-app-django pillow

# Verify
python verify_realtime_setup.py

# Apply migrations
python manage.py migrate --noinput

# Start server
daphne -b 0.0.0.0 -p 8000 gameBoosterss.asgi:application
```


