#!/bin/bash

# Mini-Survey Application - Development Startup Script
# This script helps with starting both backend and frontend servers

set -e

echo "================================================"
echo "Mini-Survey Application - Development Startup"
echo "================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Parse arguments
if [ "$1" == "backend" ] || [ "$1" == "" ]; then
    echo -e "${BLUE}Starting Backend...${NC}"
    cd backend
    
    if [ ! -d "venv" ] && [ ! -d ".venv" ]; then
        echo "Python dependencies not found. Installing..."
        pip install -q -r requirements.txt
    fi
    
    echo -e "${GREEN}✓ Starting FastAPI server on port 8000${NC}"
    echo "Navigate to http://localhost:8000/docs for API documentation"
    echo ""
    python main.py
fi

if [ "$1" == "frontend" ] || [ "$1" == "" ]; then
    echo -e "${BLUE}Starting Frontend...${NC}"
    cd frontend
    
    if [ ! -d "node_modules" ]; then
        echo "Node dependencies not found. Installing..."
        npm install --legacy-peer-deps --silent
    fi
    
    echo -e "${GREEN}✓ Starting React development server on port 3000${NC}"
    echo "Browser will open automatically..."
    echo ""
    npm start
fi

if [ "$1" == "help" ]; then
    echo "Usage: ./start.sh [backend|frontend|all|help]"
    echo ""
    echo "Options:"
    echo "  backend      - Start only backend (FastAPI on :8000)"
    echo "  frontend     - Start only frontend (React on :3000)"
    echo "  help         - Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./start.sh backend    # Start backend in current terminal"
    echo "  ./start.sh frontend   # Start frontend in current terminal"
    echo ""
    echo "Recommended: Run in separate terminals"
    echo "  Terminal 1: ./start.sh backend"
    echo "  Terminal 2: ./start.sh frontend"
fi
