@echo off
REM ========================================
REM Quick Start Script - No Virtual Environment Needed
REM Since packages are already installed globally
REM ========================================

echo.
echo ========================================
echo   Quick Start - Real-Time Order Sync
echo ========================================
echo.

echo Step 1: Verifying setup...
python verify_realtime_setup.py
echo.

echo Step 2: Applying migrations...
python manage.py migrate --noinput
if %errorlevel% neq 0 (
    echo ERROR: Migrations failed!
    pause
    exit /b 1
)
echo ✓ Migrations applied
echo.

echo Step 3: (Optional) Starting Redis...
docker compose up -d redis >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Redis started (or already running)
) else (
    echo ℹ️  Redis not started (will use InMemoryChannelLayer)
)
echo.

echo ========================================
echo   Starting Daphne Server
echo ========================================
echo.
echo 📝 Access URLs:
echo    - Test Page: http://localhost:8000/realtime/test/
echo    - Admin Dashboard: http://localhost:8000/admin/dashboard/
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

daphne -b 0.0.0.0 -p 8000 gameBoosterss.asgi:application

pause


