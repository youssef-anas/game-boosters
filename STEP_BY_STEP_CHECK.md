# Step-by-Step Verification Guide

## Overview

This guide will help you verify each step before starting the real-time order sync server.

## Step 1: Apply Migrations

### Check if migrations are needed:
```bash
python manage.py showmigrations
```

### Apply migrations:
```bash
python manage.py migrate --noinput
```

### Expected Output:
```
Operations to perform:
  Apply all migrations: accounts, admin, auth, ...
Running migrations:
  Applying accounts.0001_initial... OK
  ...
```

### If Error:
- **ModuleNotFoundError: No module named 'django'**
  → Activate virtual environment: `venv\Scripts\activate`
- **Database connection error**
  → Check database settings in `settings.py`
  → Make sure PostgreSQL is running

---

## Step 2: Start Redis (Optional)

### Check if Redis is running:
```bash
docker compose ps redis
```

### Start Redis:
```bash
docker compose up -d redis
```

### Verify Redis is running:
```bash
redis-cli ping
```
Should return: `PONG`

### Expected Output:
```
Starting game-boosters-main_redis_1 ... done
```

### If Error:
- **Redis not found**
  → This is OK! Server will use InMemoryChannelLayer
  → For production, install Redis: `docker compose up -d redis`
- **Port 6379 already in use**
  → Another Redis instance is running
  → Use that instance or stop it

### Note:
If Redis is not running, the server will automatically use `InMemoryChannelLayer` which works for single-server development.

---

## Step 3: Start Daphne ASGI Server

### Start server:
```bash
daphne -b 0.0.0.0 -p 8000 gameBoosterss.asgi:application
```

### Expected Output:
```
2024-XX-XX XX:XX:XX [INFO] Starting server at tcp:port=8000:interface=0.0.0.0
2024-XX-XX XX:XX:XX [INFO] HTTP/2 support not enabled (install the http2 and tls Twisted extras)
2024-XX-XX XX:XX:XX [INFO] Configuring endpoint tcp:port=8000:interface=0.0.0.0
2024-XX-XX XX:XX:XX [INFO] Listening on TCP address 0.0.0.0:8000
```

### If Error:
- **ModuleNotFoundError: No module named 'daphne'**
  → Install: `pip install daphne`
  → Or: `pip install -r requirements.txt`
- **ModuleNotFoundError: No module named 'channels'**
  → Install: `pip install channels channels-redis`
- **Redis connection error**
  → This is OK! Server will use InMemoryChannelLayer
  → Check logs for: "Falling back to InMemoryChannelLayer"
- **Port 8000 already in use**
  → Stop the process using port 8000
  → Or use a different port: `daphne -b 0.0.0.0 -p 8001 gameBoosterss.asgi:application`
- **ASGI application not found**
  → Check `gameBoosterss/asgi.py` exists
  → Verify: `ASGI_APPLICATION = 'gameBoosterss.asgi.application'` in settings.py

---

## Verification Script

Run this script to check everything:

```bash
python verify_realtime_setup.py
```

This will check:
1. ✓ Virtual environment
2. ✓ Django installation
3. ✓ Required dependencies (channels, daphne, channels-redis)
4. ✓ Database connection
5. ✓ Migrations status
6. ✓ Redis availability
7. ✓ Channel layer configuration
8. ✓ ASGI application
9. ✓ Realtime app configuration

---

## Quick Start Commands

Once everything is verified:

```bash
# 1. Activate virtual environment
venv\Scripts\activate

# 2. Apply migrations
python manage.py migrate --noinput

# 3. Start Redis (optional)
docker compose up -d redis

# 4. Start Daphne
daphne -b 0.0.0.0 -p 8000 gameBoosterss.asgi:application
```

---

## Access URLs

Once server is running:

- **Test Page**: http://localhost:8000/realtime/test/
- **Admin Dashboard**: http://localhost:8000/admin/dashboard/

---

## Troubleshooting

### Server won't start
1. Check virtual environment is activated
2. Run verification script: `python verify_realtime_setup.py`
3. Check error messages in terminal
4. Verify all dependencies are installed

### ERR_EMPTY_RESPONSE
1. Check if server is actually running (look for "Listening on TCP address")
2. Check port 8000 is not in use by another process
3. Check firewall settings
4. Try restarting the server

### WebSocket connection fails
1. Verify server is running with Daphne (not runserver)
2. Check Redis is running (or InMemoryChannelLayer is being used)
3. Check browser console for WebSocket errors
4. Verify WebSocket URL: `ws://localhost:8000/ws/orders/<order_id>/`


