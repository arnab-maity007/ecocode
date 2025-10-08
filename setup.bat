@echo off
REM Quick setup script for Windows
echo ========================================
echo Hyperlocal Urban Flood Forecaster Setup
echo ========================================
echo.

echo Step 1: Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment created

echo.
echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat
echo ✓ Virtual environment activated

echo.
echo Step 3: Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed

echo.
echo Step 4: Checking if .env file exists...
if not exist .env (
    echo .env file not found. Copying from .env.example...
    copy .env.example .env
    echo.
    echo ⚠️  IMPORTANT: Please edit .env file with your configuration:
    echo    - DATABASE_URL
    echo    - OPENWEATHERMAP_API_KEY
    echo    - SECRET_KEY
    echo.
    echo Press any key after editing .env file...
    pause
)
echo ✓ .env file exists

echo.
echo Step 5: Running setup check...
python setup_check.py

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the server, run:
echo   python main.py
echo.
echo Or:
echo   uvicorn main:app --reload
echo.
echo API Documentation will be at: http://localhost:8000/docs
echo.
pause
