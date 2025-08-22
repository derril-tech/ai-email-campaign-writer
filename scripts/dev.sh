#!/bin/bash

# 🚀 Development Script for AI Email Campaign Writer
# This script starts both frontend and backend in development mode

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if required tools are installed
check_dependencies() {
    print_status "Checking dependencies..."
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        print_error "Node.js is not installed. Please install Node.js 18+"
        exit 1
    fi
    
    # Check npm
    if ! command -v npm &> /dev/null; then
        print_error "npm is not installed. Please install npm"
        exit 1
    fi
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python 3.9+"
        exit 1
    fi
    
    # Check pip
    if ! command -v pip3 &> /dev/null; then
        print_error "pip3 is not installed. Please install pip3"
        exit 1
    fi
    
    print_success "All dependencies are installed"
}

# Setup frontend
setup_frontend() {
    print_status "Setting up frontend..."
    
    cd frontend
    
    # Check if node_modules exists
    if [ ! -d "node_modules" ]; then
        print_status "Installing frontend dependencies..."
        npm install
    fi
    
    # Check if .env.local exists
    if [ ! -f ".env.local" ]; then
        print_warning ".env.local not found. Creating from example..."
        cp env.example .env.local
        print_warning "Please edit .env.local with your configuration"
    fi
    
    cd ..
    print_success "Frontend setup complete"
}

# Setup backend
setup_backend() {
    print_status "Setting up backend..."
    
    cd backend
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        print_status "Creating Python virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install dependencies
    print_status "Installing backend dependencies..."
    pip install -r requirements.txt
    
    # Check if .env exists
    if [ ! -f ".env" ]; then
        print_warning ".env not found. Creating from example..."
        cp env.example .env
        print_warning "Please edit .env with your configuration"
    fi
    
    cd ..
    print_success "Backend setup complete"
}

# Start frontend
start_frontend() {
    print_status "Starting frontend development server..."
    cd frontend
    npm run dev &
    FRONTEND_PID=$!
    cd ..
    print_success "Frontend started on http://localhost:3000 (PID: $FRONTEND_PID)"
}

# Start backend
start_backend() {
    print_status "Starting backend development server..."
    cd backend
    source venv/bin/activate
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
    BACKEND_PID=$!
    cd ..
    print_success "Backend started on http://localhost:8000 (PID: $BACKEND_PID)"
}

# Start Redis (if available)
start_redis() {
    if command -v redis-server &> /dev/null; then
        print_status "Starting Redis server..."
        redis-server --daemonize yes
        print_success "Redis started"
    else
        print_warning "Redis not found. Please install Redis for full functionality"
    fi
}

# Start Celery (if Redis is available)
start_celery() {
    if command -v redis-server &> /dev/null; then
        print_status "Starting Celery worker..."
        cd backend
        source venv/bin/activate
        celery -A app.core.celery worker --loglevel=info &
        CELERY_PID=$!
        cd ..
        print_success "Celery worker started (PID: $CELERY_PID)"
    else
        print_warning "Skipping Celery worker (Redis not available)"
    fi
}

# Cleanup function
cleanup() {
    print_status "Shutting down development servers..."
    
    # Kill background processes
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
        print_status "Frontend stopped"
    fi
    
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
        print_status "Backend stopped"
    fi
    
    if [ ! -z "$CELERY_PID" ]; then
        kill $CELERY_PID 2>/dev/null || true
        print_status "Celery worker stopped"
    fi
    
    # Stop Redis if we started it
    if command -v redis-server &> /dev/null; then
        redis-cli shutdown 2>/dev/null || true
        print_status "Redis stopped"
    fi
    
    print_success "All development servers stopped"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Main execution
main() {
    echo "🚀 Starting AI Email Campaign Writer Development Environment"
    echo "=========================================================="
    
    # Check dependencies
    check_dependencies
    
    # Setup frontend and backend
    setup_frontend
    setup_backend
    
    # Start services
    start_redis
    start_frontend
    start_backend
    start_celery
    
    echo ""
    echo "🎉 Development environment is ready!"
    echo "=================================="
    echo "Frontend: http://localhost:3000"
    echo "Backend API: http://localhost:8000"
    echo "API Docs: http://localhost:8000/docs"
    echo ""
    echo "Press Ctrl+C to stop all servers"
    echo ""
    
    # Wait for user to stop
    wait
}

# Run main function
main "$@"
