@echo off
REM Simple script to start Daphne server for realtime testing
REM This will automatically fall back to InMemoryChannelLayer if Redis is not available

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

REM Check if Redis is available (optional)
echo Checking Redis availability...
docker compose ps redis >nul 2>&1
if %errorlevel% equ 0 (
    echo Redis is running via Docker
) else (
    echo Redis not running via Docker - will use InMemoryChannelLayer
)
echo.

REM Start Daphne
echo Starting Daphne ASGI server on port 8000...
echo.
echo Access the test page at: http://localhost:8000/realtime/test/
echo Or from Admin Dashboard: http://localhost:8000/admin/dashboard/
echo.
echo Press Ctrl+C to stop the server
echo.

daphne -b 0.0.0.0 -p 8000 gameBoosterss.asgi:application

