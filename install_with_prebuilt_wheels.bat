@echo off
REM ========================================
REM Install with Pre-built Wheels
REM This avoids compilation issues
REM ========================================

echo.
echo ========================================
echo   Installing with Pre-built Wheels
echo ========================================
echo.

REM Activate virtual environment
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

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo ✓ Pip upgraded
echo.

REM Install with pre-built wheels only
echo Installing packages with pre-built wheels...
echo This may take a few minutes...
echo.

pip install --only-binary :all: -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo ⚠️  Some packages failed to install with pre-built wheels
    echo Trying alternative installation method...
    echo.
    
    REM Try installing core packages manually
    echo Installing core packages manually...
    pip install django==5.0.10
    pip install channels==4.1.0
    pip install channels-redis==4.1.0
    pip install daphne==4.1.2
    pip install asgiref
    pip install twisted
    pip install autobahn
    pip install psycopg2-binary
    pip install django-cors-headers
    pip install python-dotenv
    pip install django-simple-history
    pip install whitenoise
    pip install djangorestframework
    
    echo.
    echo ✓ Core packages installed
    echo.
    echo ⚠️  Some optional packages may not be installed
    echo You can install them later if needed
)

echo.
echo ========================================
echo   Installation Complete!
echo ========================================
echo.
echo Verifying installation...
python verify_realtime_setup.py
echo.
pause


