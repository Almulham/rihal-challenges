#!/bin/bash

# PDF Table Grid Mapper - Setup Script
# This script sets up the environment for the PDF table grid mapper

echo "🛠️  PDF Table Grid Mapper - Setup"
echo "================================="

# Check Python version
echo "🐍 Checking Python version..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check system dependencies
echo "📦 Checking system dependencies..."

# Check for poppler-utils (required for pdf2image)
if ! command -v pdftoppm &> /dev/null; then
    echo "⚠️  poppler-utils not found. Installing..."
    
    # Detect OS and install accordingly
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v apt-get &> /dev/null; then
            sudo apt-get update
            sudo apt-get install -y poppler-utils python3-venv
        elif command -v yum &> /dev/null; then
            sudo yum install -y poppler-utils python3-venv
        else
            echo "❌ Please install poppler-utils manually for your Linux distribution"
            exit 1
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install poppler
        else
            echo "❌ Please install Homebrew and then run: brew install poppler"
            exit 1
        fi
    else
        echo "❌ Unsupported operating system. Please install poppler-utils manually."
        exit 1
    fi
fi

echo "✅ System dependencies verified"

# Create virtual environment
echo "🏗️  Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists. Removing old one..."
    rm -rf venv
fi

python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "❌ Failed to create virtual environment"
    exit 1
fi

echo "✅ Virtual environment created"

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed successfully"

# Run tests
echo "🧪 Running tests..."
python test_app.py

if [ $? -ne 0 ]; then
    echo "⚠️  Tests failed, but setup may still work"
else
    echo "✅ All tests passed"
fi

# Generate example files
echo "📄 Generating example files..."
python example_usage.py > /dev/null 2>&1

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "   1. To start the application:"
echo "      ./start_app.sh"
echo "   or"
echo "      source venv/bin/activate && streamlit run app.py"
echo ""
echo "   2. Upload a PDF with tables and start mapping grids!"
echo ""
echo "📁 Generated files:"
echo "   - sample_table.png (example table image)"
echo "   - sample_table_with_grid.png (example with grid overlay)"
echo "   - sample_grid_coordinates.json (example JSON output)"
echo ""
echo "📖 For more information, see README.md"