# Quick Start Guide - Real-Time Order Sync

## Problem: ERR_EMPTY_RESPONSE

If you're getting `ERR_EMPTY_RESPONSE`, the Daphne server likely crashed due to Redis connection issues.

## Solution Options

### Option 1: Use InMemoryChannelLayer (Quick Fix - No Redis Needed)

1. **Set environment variable** (or edit `settings.py`):
   ```bash
   set USE_REDIS=False
   ```

2. **Or temporarily edit `settings.py`**:
   - Change `USE_REDIS = True` to `USE_REDIS = False`
   - Or comment out the Redis channel layer and uncomment InMemory

3. **Start Daphne**:
   ```bash
   daphne -b 0.0.0.0 -p 8000 gameBoosterss.asgi:application
   ```

### Option 2: Start Redis First (Recommended for Production)

1. **Start Redis using Docker**:
   ```bash
   docker compose up -d redis
   ```

2. **Verify Redis is running**:
   ```bash
   docker compose ps redis
   redis-cli ping
   ```
   Should return: `PONG`

3. **Start Daphne**:
   ```bash
   daphne -b 0.0.0.0 -p 8000 gameBoosterss.asgi:application
   ```

### Option 3: Use Django's runserver (For Quick Testing)

For quick testing without WebSocket support, you can use:
```bash
python manage.py runserver 0.0.0.0:8000
```

**Note:** This won't support WebSockets, but you can test the HTTP endpoints.

## Verify Server is Running

1. **Check if port 8000 is in use**:
   ```bash
   netstat -ano | findstr :8000
   ```

2. **Check Daphne logs** for errors:
   - Look for Redis connection errors
   - Look for import errors
   - Look for ASGI application errors

## Testing the Real-Time Page

Once server is running:

1. **Access test page**: `http://localhost:8000/realtime/test/`
2. **Or from Admin Dashboard**: Click "🔄 Test Realtime Sync" button

## Common Issues

### Issue: "Connection refused" or "Redis connection failed"
**Solution**: Use Option 1 (InMemoryChannelLayer) or start Redis (Option 2)

### Issue: "Module not found: channels_redis"
**Solution**: Install dependencies:
```bash
pip install channels-redis
```

### Issue: "ASGI application not found"
**Solution**: Make sure you're in the project root directory and running:
```bash
daphne -b 0.0.0.0 -p 8000 gameBoosterss.asgi:application
```

### Issue: Port 8000 already in use
**Solution**: Kill the process using port 8000 or use a different port:
```bash
daphne -b 0.0.0.0 -p 8001 gameBoosterss.asgi:application
```

## Manual Start Commands

```bash
# 1. Apply migrations
python manage.py migrate --noinput

# 2. Start Redis (if using Docker)
docker compose up -d redis

# 3. Start Daphne
daphne -b 0.0.0.0 -p 8000 gameBoosterss.asgi:application
```

## Check Server Status

Open a new terminal and run:
```bash
curl http://localhost:8000/realtime/test/
```

If you get HTML back, the server is running. If you get connection refused, the server isn't running.



