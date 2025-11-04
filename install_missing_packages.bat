@echo off
REM ========================================
REM Install Missing Packages
REM Installs packages needed for Django to run
REM ========================================

echo.
echo ========================================
echo   Installing Missing Packages
echo ========================================
echo.

echo Installing essential packages...
pip install django-jazzmin
pip install django-cleanup
pip install django-phonenumber-field
pip install django-countries
pip install social-auth-app-django
pip install pillow
pip install firebase-admin 2>nul
pip install paypalrestsdk 2>nul

echo.
echo ========================================
echo   Installation Complete!
echo ========================================
echo.
echo Now try running:
echo python manage.py migrate --noinput
echo.
pause


