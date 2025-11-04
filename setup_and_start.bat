@echo off
REM ========================================
REM Complete Setup and Start Script
REM This will activate venv, install dependencies, and start server
REM ========================================

echo.
echo ========================================
echo   Complete Setup and Start Script
echo ========================================
echo.

REM Step 1: Activate virtual environment
echo [1/5] Activating virtual environment...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo ✓ Virtual environment activated
) else (
    echo ✗ Virtual environment not found!
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo ✓ Virtual environment created and activated
)
echo.

REM Step 2: Upgrade pip
echo [2/5] Upgrading pip...
python -m pip install --upgrade pip
echo ✓ Pip upgraded
echo.

REM Step 3: Install dependencies
echo [3/5] Installing dependencies from requirements.txt...
echo This may take a few minutes...
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies!
    echo Please check requirements.txt and try again.
    pause
    exit /b 1
)
echo ✓ Dependencies installed
echo.

REM Step 4: Apply migrations
echo [4/5] Applying migrations...
python manage.py migrate --noinput
if %errorlevel% neq 0 (
    echo ERROR: Migrations failed!
    pause
    exit /b 1
)
echo ✓ Migrations applied
echo.

REM Step 5: Start Redis (optional)
echo [5/5] Starting Redis (optional)...
docker compose up -d redis >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Redis started (or already running)
) else (
    echo ℹ️  Redis not started (will use InMemoryChannelLayer)
)
echo.

REM Start Daphne server
echo ========================================
echo   Starting Daphne ASGI Server
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


