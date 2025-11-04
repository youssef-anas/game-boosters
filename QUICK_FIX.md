# 🚀 Quick Fix - Start Real-Time Server

## Fastest Solution (3 Steps)

### 1️⃣ Activate Virtual Environment
```powershell
venv\Scripts\activate
```
**Look for `(venv)` in your prompt**

### 2️⃣ Run Migrations
```powershell
python manage.py migrate --noinput
```

### 3️⃣ Start Server
```powershell
daphne -b 0.0.0.0 -p 8000 gameBoosterss.asgi:application
```

---

## Or Use the Batch Script (Easiest!)

**Just double-click or run:**
```powershell
.\start_realtime_server_full.bat
```

This does everything automatically!

---

## If You Get Errors

### "No module named 'django'"
→ Activate virtual environment first: `venv\Scripts\activate`

### "Port 8000 already in use"
→ Stop other server or use port 8001: `daphne -b 0.0.0.0 -p 8001 gameBoosterss.asgi:application`

### "Redis connection failed"
→ This is OK! Server will use InMemoryChannelLayer automatically

---

## Access URLs

Once server starts:
- **Test Page**: http://localhost:8000/realtime/test/
- **Admin**: http://localhost:8000/admin/dashboard/

---

## Need More Help?

Run this to check everything:
```powershell
python verify_realtime_setup.py
```


