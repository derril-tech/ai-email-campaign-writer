@echo off
REM 🚀 Development Script for AI Email Campaign Writer (Windows)
REM This script starts both frontend and backend in development mode

setlocal enabledelayedexpansion

echo 🚀 Starting AI Email Campaign Writer Development Environment
echo ==========================================================

REM Check if Node.js is installed
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed. Please install Node.js 18+
    pause
    exit /b 1
)

REM Check if npm is installed
where npm >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] npm is not installed. Please install npm
    pause
    exit /b 1
)

REM Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed. Please install Python 3.9+
    pause
    exit /b 1
)

echo [SUCCESS] All dependencies are installed

REM Setup frontend
echo [INFO] Setting up frontend...
cd frontend

REM Check if node_modules exists
if not exist "node_modules" (
    echo [INFO] Installing frontend dependencies...
    call npm install
)

REM Check if .env.local exists
if not exist ".env.local" (
    echo [WARNING] .env.local not found. Creating from example...
    copy env.example .env.local
    echo [WARNING] Please edit .env.local with your configuration
)

cd ..
echo [SUCCESS] Frontend setup complete

REM Setup backend
echo [INFO] Setting up backend...
cd backend

REM Check if virtual environment exists
if not exist "venv" (
    echo [INFO] Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo [INFO] Installing backend dependencies...
pip install -r requirements.txt

REM Check if .env exists
if not exist ".env" (
    echo [WARNING] .env not found. Creating from example...
    copy env.example .env
    echo [WARNING] Please edit .env with your configuration
)

cd ..
echo [SUCCESS] Backend setup complete

REM Start Redis (if available)
where redis-server >nul 2>nul
if %errorlevel% equ 0 (
    echo [INFO] Starting Redis server...
    start /B redis-server
    echo [SUCCESS] Redis started
) else (
    echo [WARNING] Redis not found. Please install Redis for full functionality
)

REM Start frontend
echo [INFO] Starting frontend development server...
cd frontend
start "Frontend Dev Server" cmd /k "npm run dev"
cd ..

REM Start backend
echo [INFO] Starting backend development server...
cd backend
call venv\Scripts\activate.bat
start "Backend Dev Server" cmd /k "uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
cd ..

REM Start Celery (if Redis is available)
where redis-server >nul 2>nul
if %errorlevel% equ 0 (
    echo [INFO] Starting Celery worker...
    cd backend
    call venv\Scripts\activate.bat
    start "Celery Worker" cmd /k "celery -A app.core.celery worker --loglevel=info"
    cd ..
    echo [SUCCESS] Celery worker started
) else (
    echo [WARNING] Skipping Celery worker (Redis not available)
)

echo.
echo 🎉 Development environment is ready!
echo ==================================
echo Frontend: http://localhost:3000
echo Backend API: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo All servers are running in separate windows.
echo Close the windows to stop the servers.
echo.
pause
