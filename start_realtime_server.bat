@echo off
REM Script to start Django ASGI server for realtime testing (Windows)

echo 🚀 Starting Real-Time Order Sync Server
echo ========================================

REM 1. Apply migrations
echo 📦 Applying migrations...
python manage.py migrate --noinput

REM 2. Start Redis if using Docker
echo 🔴 Starting Redis...
docker compose up -d redis

REM Wait for Redis to be ready
echo ⏳ Waiting for Redis to be ready...
timeout /t 3 /nobreak >nul

REM 3. Start Daphne ASGI server
echo 🌐 Starting Daphne ASGI server on port 8000...
echo.
echo ✅ Server starting...
echo 📝 Access the test page at: http://localhost:8000/realtime/test/
echo 📝 Or from Admin Dashboard: http://localhost:8000/admin/dashboard/
echo.
echo Press Ctrl+C to stop the server
echo.

daphne -b 0.0.0.0 -p 8000 gameBoosterss.asgi:application



