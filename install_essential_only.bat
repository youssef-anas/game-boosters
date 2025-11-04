@echo off
REM ========================================
REM Install Essential Packages Only
REM This skips packages that need compilation
REM ========================================

echo.
echo ========================================
echo   Installing Essential Packages Only
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

REM Install essential packages
echo Installing essential packages for real-time sync...
echo.

REM Core Django and Channels
echo Installing Django and Channels...
pip install django==5.0.10
pip install channels==4.1.0
pip install channels-redis==4.1.0
pip install daphne==4.1.2
pip install asgiref
pip install twisted
pip install autobahn
echo ✓ Core packages installed
echo.

REM Database
echo Installing database packages...
pip install psycopg2-binary
echo ✓ Database packages installed
echo.

REM Django essentials
echo Installing Django essentials...
pip install django-cors-headers
pip install python-dotenv
pip install django-simple-history
pip install whitenoise
pip install django-cleanup
echo ✓ Django essentials installed
echo.

REM Additional packages
echo Installing additional packages...
pip install djangorestframework
pip install django-jazzmin
pip install django-phonenumber-field
pip install django-countries
pip install pillow
pip install social-auth-app-django
echo ✓ Additional packages installed
echo.

REM Optional packages (try to install, but don't fail if they don't work)
echo Installing optional packages...
pip install firebase-admin 2>nul
pip install google-cloud-storage 2>nul
pip install google-cloud-firestore 2>nul
pip install faker 2>nul
pip install captcha 2>nul
pip install paypalrestsdk 2>nul
pip install cryptomus 2>nul
echo ✓ Optional packages installed (some may have failed, that's OK)
echo.

REM Try to install cffi with pre-built wheel
echo Attempting to install cffi with pre-built wheel...
pip install cffi --only-binary :all: 2>nul
if %errorlevel% equ 0 (
    echo ✓ cffi installed
) else (
    echo ⚠️  cffi installation failed (may not be needed)
)
echo.

echo ========================================
echo   Installation Complete!
echo ========================================
echo.
echo Verifying installation...
python verify_realtime_setup.py
echo.
echo If verification shows errors, you may need:
echo 1. Install Visual C++ Build Tools
echo 2. Or use Python 3.11/3.12 instead of 3.13
echo.
pause


