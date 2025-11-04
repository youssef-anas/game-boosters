# 🟢 Starting Django ASGI Server for Realtime Testing

## Quick Start

Run the batch script:
```bash
start_realtime_server_full.bat
```

Or run the commands manually:

## Manual Steps

### 1️⃣ Apply Migrations
```bash
python manage.py migrate --noinput
```

### 2️⃣ Start Redis (Optional - if using Docker)
```bash
docker compose up -d redis
```

**Note:** If Redis is not running, the server will automatically use `InMemoryChannelLayer` which works for single-server development.

### 3️⃣ Start Daphne ASGI Server
```bash
daphne -b 0.0.0.0 -p 8000 gameBoosterss.asgi:application
```

## Access URLs

Once the server is running:

- **Test Page**: `http://localhost:8000/realtime/test/`
- **Admin Dashboard**: `http://localhost:8000/admin/dashboard/` (click "🔄 Test Realtime Sync" button)

## Troubleshooting

### Port 8000 Already in Use
If port 8000 is already in use, either:
1. Stop the process using port 8000
2. Use a different port:
   ```bash
   daphne -b 0.0.0.0 -p 8001 gameBoosterss.asgi:application
   ```

### Redis Connection Error
This is OK for development! The server will automatically fall back to `InMemoryChannelLayer`.

To use Redis:
1. Start Redis: `docker compose up -d redis`
2. Verify: `redis-cli ping` (should return PONG)

### Module Not Found Errors
Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Django Setup Errors
Check Django configuration:
```bash
python manage.py check
```

## Expected Output

When Daphne starts successfully, you should see:
```
2024-XX-XX XX:XX:XX [INFO] Starting server at tcp:port=8000:interface=0.0.0.0
2024-XX-XX XX:XX:XX [INFO] HTTP/2 support not enabled (install the http2 and tls Twisted extras)
2024-XX-XX XX:XX:XX [INFO] Configuring endpoint tcp:port=8000:interface=0.0.0.0
2024-XX-XX XX:XX:XX [INFO] Listening on TCP address 0.0.0.0:8000
```

## Testing

1. Open the test page: `http://localhost:8000/realtime/test/`
2. Enter an order ID
3. Click "Connect"
4. Update the order from Django Admin
5. Watch real-time updates appear!

## Stopping the Server

Press `Ctrl+C` in the terminal running Daphne.



