#!/bin/bash

# PDF Table Grid Mapper - Startup Script
# This script activates the virtual environment and starts the Streamlit application

echo "📊 Starting PDF Table Grid Mapper..."
echo "=================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first:"
    echo "   python3 -m venv venv"
    echo "   source venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if required packages are installed
echo "📦 Checking dependencies..."
python -c "import streamlit, cv2, pdfplumber, plotly" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Some dependencies are missing. Installing..."
    pip install -r requirements.txt
fi

echo "✅ Dependencies verified"

# Start the Streamlit application
echo "🚀 Starting Streamlit application..."
echo ""
echo "🌐 The application will open in your default web browser"
echo "📍 URL: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

# Run Streamlit with optimized settings
streamlit run app.py \
    --server.port 8501 \
    --server.address localhost \
    --browser.gatherUsageStats false \
    --theme.base light