#!/bin/bash

echo "🚀 Starting PDF Table Grid Mapper..."
echo "📦 Activating virtual environment..."

# Activate virtual environment
source pdf_table_env/bin/activate

echo "🌐 Starting Streamlit application..."
echo "📍 Application will be available at: http://localhost:8501"
echo "⏹️  Press Ctrl+C to stop the application"
echo ""

# Start Streamlit
streamlit run app.py --server.port 8501 --server.address 0.0.0.0