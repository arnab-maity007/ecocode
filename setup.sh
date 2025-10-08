#!/bin/bash
# Quick setup script for Linux/Mac

echo "========================================"
echo "Hyperlocal Urban Flood Forecaster Setup"
echo "========================================"
echo ""

echo "Step 1: Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi
echo "✓ Virtual environment created"

echo ""
echo "Step 2: Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

echo ""
echo "Step 3: Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
echo "✓ Dependencies installed"

echo ""
echo "Step 4: Checking if .env file exists..."
if [ ! -f .env ]; then
    echo ".env file not found. Copying from .env.example..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env file with your configuration:"
    echo "   - DATABASE_URL"
    echo "   - OPENWEATHERMAP_API_KEY"
    echo "   - SECRET_KEY"
    echo ""
    echo "Press Enter after editing .env file..."
    read
fi
echo "✓ .env file exists"

echo ""
echo "Step 5: Running setup check..."
python setup_check.py

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "To start the server, run:"
echo "  python main.py"
echo ""
echo "Or:"
echo "  uvicorn main:app --reload"
echo ""
echo "API Documentation will be at: http://localhost:8000/docs"
echo ""
