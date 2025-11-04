# 🔧 Solution Guide - Real-Time Order Sync Setup

## Quick Solution

Follow these steps **in order**:

### Step 1: Activate Virtual Environment

**In PowerShell, run:**
```powershell
venv\Scripts\activate
```

**You should see `(venv)` in your prompt:**
```
(venv) PS E:\youssef_anas\game-boosters-main>
```

---

### Step 2: Verify Setup (Recommended)

**Run the verification script:**
```powershell
python verify_realtime_setup.py
```

This will check all components and tell you what needs to be fixed.

---

### Step 3: Apply Migrations

**Run:**
```powershell
python manage.py migrate --noinput
```

**If you get "ModuleNotFoundError: No module named 'django'":**
- Make sure virtual environment is activated (see Step 1)
- Install dependencies: `pip install -r requirements.txt`

---

### Step 4: Start Redis (Optional - Can Skip)

**If you want to use Redis:**
```powershell
docker compose up -d redis
```

**If Redis is not running:**
- That's OK! The server will use InMemoryChannelLayer automatically
- This works for single-server development

---

### Step 5: Start Daphne Server

**Run:**
```powershell
daphne -b 0.0.0.0 -p 8000 gameBoosterss.asgi:application
```

**You should see:**
```
2024-XX-XX XX:XX:XX [INFO] Starting server at tcp:port=8000:interface=0.0.0.0
2024-XX-XX XX:XX:XX [INFO] Listening on TCP address 0.0.0.0:8000
```

---

## Access the Test Page

Once server is running:
- **Test Page**: http://localhost:8000/realtime/test/
- **Admin Dashboard**: http://localhost:8000/admin/dashboard/

---

## Common Problems & Solutions

### Problem 1: "ModuleNotFoundError: No module named 'django'"

**Solution:**
```powershell
# 1. Activate virtual environment
venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Try again
python manage.py migrate --noinput
```

---

### Problem 2: "Port 8000 already in use"

**Solution:**
```powershell
# Option 1: Find and stop the process using port 8000
netstat -ano | findstr :8000
# Then kill the process ID shown

# Option 2: Use a different port
daphne -b 0.0.0.0 -p 8001 gameBoosterss.asgi:application
```

---

### Problem 3: "ERR_EMPTY_RESPONSE" or "Connection refused"

**Solution:**
1. Make sure Daphne is actually running (check terminal for "Listening on TCP address")
2. Check if port 8000 is accessible
3. Try accessing: http://localhost:8000/admin/
4. If that works, the server is running - try the test page again

---

### Problem 4: "Redis connection failed"

**Solution:**
- This is OK for development! The server will automatically use InMemoryChannelLayer
- Check server logs - you should see: "Falling back to InMemoryChannelLayer"
- If you want Redis, start it: `docker compose up -d redis`

---

### Problem 5: "ASGI application not found"

**Solution:**
1. Check file exists: `gameBoosterss/asgi.py`
2. Verify in `settings.py`: `ASGI_APPLICATION = 'gameBoosterss.asgi.application'`
3. Make sure you're in the project root directory

---

### Problem 6: "Database connection error"

**Solution:**
1. Check PostgreSQL is running
2. Check database settings in `settings.py`
3. Verify database credentials in `.env` file
4. Try: `python manage.py dbshell` (to test database connection)

---

## Easiest Solution: Use the Batch Script

**Just run:**
```powershell
.\start_realtime_server_full.bat
```

This script will:
1. ✅ Activate virtual environment automatically
2. ✅ Apply migrations
3. ✅ Start Redis (if using Docker)
4. ✅ Start Daphne server

---

## Step-by-Step Checklist

Copy and paste these commands one by one:

```powershell
# 1. Activate virtual environment
venv\Scripts\activate

# 2. Verify everything is set up
python verify_realtime_setup.py

# 3. Apply migrations
python manage.py migrate --noinput

# 4. (Optional) Start Redis
docker compose up -d redis

# 5. Start Daphne server
daphne -b 0.0.0.0 -p 8000 gameBoosterss.asgi:application
```

---

## Still Having Issues?

1. **Run the verification script:**
   ```powershell
   python verify_realtime_setup.py
   ```
   This will tell you exactly what's wrong.

2. **Check the error message:**
   - Copy the full error message
   - Look for it in `STEP_BY_STEP_CHECK.md`

3. **Check server logs:**
   - Look at the terminal output when starting Daphne
   - Check for error messages

4. **Verify all files exist:**
   - `gameBoosterss/asgi.py`
   - `realtime/apps.py`
   - `realtime/consumers.py`
   - `realtime/routing.py`
   - `realtime/signals.py`

---

## Success Indicators

You'll know everything is working when:

1. ✅ Virtual environment shows `(venv)` in prompt
2. ✅ Migrations run without errors
3. ✅ Daphne shows "Listening on TCP address 0.0.0.0:8000"
4. ✅ You can access http://localhost:8000/realtime/test/
5. ✅ Test page loads and shows connection interface


