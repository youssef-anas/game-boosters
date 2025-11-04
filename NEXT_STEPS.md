# ✅ Next Steps - After Installing Packages

## Important Note

You've successfully installed the packages! However, they were installed in your **global Python** installation, not in the virtual environment.

## Recommended Next Steps

### Option 1: Continue with Global Python (Quickest)

Since packages are already installed globally, you can proceed:

**1. Verify setup:**
```powershell
python verify_realtime_setup.py
```

**2. Apply migrations:**
```powershell
python manage.py migrate --noinput
```

**3. Start server:**
```powershell
daphne -b 0.0.0.0 -p 8000 gameBoosterss.asgi:application
```

---

### Option 2: Use Virtual Environment (Recommended)

**If you want to use virtual environment:**

**Option A: Use Command Prompt (CMD) - Easiest!**
1. Open **Command Prompt** (not PowerShell)
2. Navigate: `cd E:\youssef_anas\game-boosters-main`
3. Activate: `venv\Scripts\activate.bat`
4. Install packages in venv:
   ```cmd
   pip install django==5.0.10 channels==4.1.0 channels-redis==4.1.0 daphne==4.1.2
   pip install asgiref twisted autobahn psycopg2-binary
   pip install django-cors-headers python-dotenv django-simple-history whitenoise
   pip install djangorestframework
   ```

**Option B: Fix PowerShell Execution Policy**
1. Run PowerShell as Administrator
2. Run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
3. Then activate: `venv\Scripts\activate`

---

## Complete Checklist

### Step 1: Verify Installation
```powershell
python verify_realtime_setup.py
```

**Expected output:**
- ✓ Django is installed
- ✓ channels is installed
- ✓ channels-redis is installed
- ✓ daphne is installed
- ✓ Database connection is working
- ✓ Migrations status
- ✓ Channel layer configuration
- ✓ ASGI application
- ✓ Realtime app configuration

### Step 2: Apply Migrations
```powershell
python manage.py migrate --noinput
```

**Expected output:**
```
Operations to perform:
  Apply all migrations: accounts, admin, auth, ...
Running migrations:
  Applying accounts.0001_initial... OK
  ...
```

### Step 3: (Optional) Start Redis
```powershell
docker compose up -d redis
```

**Note:** If Redis is not running, the server will use InMemoryChannelLayer automatically.

### Step 4: Start Daphne Server
```powershell
daphne -b 0.0.0.0 -p 8000 gameBoosterss.asgi:application
```

**Expected output:**
```
2024-XX-XX XX:XX:XX [INFO] Starting server at tcp:port=8000:interface=0.0.0.0
2024-XX-XX XX:XX:XX [INFO] Listening on TCP address 0.0.0.0:8000
```

### Step 5: Access Test Page
- **Test Page**: http://localhost:8000/realtime/test/
- **Admin Dashboard**: http://localhost:8000/admin/dashboard/

---

## Quick Commands (Copy & Paste)

**If packages are installed globally (your current situation):**

```powershell
# 1. Verify setup
python verify_realtime_setup.py

# 2. Apply migrations
python manage.py migrate --noinput

# 3. (Optional) Start Redis
docker compose up -d redis

# 4. Start server
daphne -b 0.0.0.0 -p 8000 gameBoosterss.asgi:application
```

---

## Troubleshooting

### If "python" command not found:
- Make sure Python is in your PATH
- Try: `python3` or `py` instead of `python`

### If "daphne" command not found:
- Make sure Daphne is installed: `pip install daphne==4.1.2`
- Check installation: `pip list | findstr daphne`

### If database connection fails:
- Check PostgreSQL is running
- Check database settings in `settings.py`
- Check `.env` file for database credentials

---

## Success Indicators

You'll know everything is working when:

1. ✅ `verify_realtime_setup.py` shows most checks passing
2. ✅ Migrations apply without errors
3. ✅ Daphne shows "Listening on TCP address 0.0.0.0:8000"
4. ✅ You can access http://localhost:8000/realtime/test/
5. ✅ Test page loads and shows connection interface


