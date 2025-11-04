@echo off
REM ========================================
REM Start Django ASGI Server for Realtime Testing
REM ========================================

echo.
echo ========================================
echo   Starting Real-Time Order Sync Server
echo ========================================
echo.

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
    echo ✓ Virtual environment activated
) else if exist "venv\activate.bat" (
    echo Activating virtual environment...
    call venv\activate.bat
    echo ✓ Virtual environment activated
) else (
    echo WARNING: Virtual environment not found
    echo Make sure Django and dependencies are installed
)
echo.

REM Step 1: Apply migrations
echo [1/3] Applying migrations...
python manage.py migrate --noinput
if %errorlevel% neq 0 (
    echo ERROR: Migrations failed!
    pause
    exit /b 1
)
echo ✓ Migrations applied successfully
echo.

REM Step 2: Start Redis if using Docker
echo [2/3] Starting Redis (Docker)...
docker compose up -d redis
if %errorlevel% neq 0 (
    echo WARNING: Could not start Redis via Docker
    echo This is OK - the server will use InMemoryChannelLayer
) else (
    echo ✓ Redis started (or already running)
    echo Waiting for Redis to be ready...
    timeout /t 3 /nobreak >nul
)
echo.

REM Step 3: Start Daphne ASGI server
echo [3/3] Starting Daphne ASGI server on port 8000...
echo.
echo ========================================
echo   Server Starting...
echo ========================================
echo.
echo 📝 Access URLs:
echo    - Test Page: http://localhost:8000/realtime/test/
echo    - Admin Dashboard: http://localhost:8000/admin/dashboard/
echo.
echo 💡 Tips:
echo    - If Redis is not running, InMemoryChannelLayer will be used
echo    - This works for single-server development
echo    - For production, ensure Redis is running
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

daphne -b 0.0.0.0 -p 8000 gameBoosterss.asgi:application

pause

