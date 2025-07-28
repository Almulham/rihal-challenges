# PDF Table Grid Mapper - Usage Guide

## Quick Start

### 1. Setup and Installation

The application is ready to run! All dependencies are installed in the virtual environment.

```bash
# Make the startup script executable (if not already done)
chmod +x run.sh

# Start the application
./run.sh
```

Or manually:
```bash
source pdf_table_env/bin/activate
streamlit run app.py
```

### 2. Access the Application

Once started, open your web browser and navigate to:
- **Local**: http://localhost:8501
- **Network**: http://0.0.0.0:8501 (accessible from other devices on the same network)

### 3. Using the Application

1. **Upload PDF**: Click "Choose a PDF file" and select your PDF containing tables
2. **Adjust Settings**: Use the sidebar to modify:
   - **Image DPI**: Higher values = better quality but slower processing
   - **Show cell coordinates**: Toggle coordinate labels on grid overlay
3. **View Results**: 
   - Left panel shows the original PDF page
   - Right panel shows detected table grids with overlays
4. **Examine Tables**: Expand table sections to see detailed cell information
5. **Export Data**: Copy or download the JSON with exact coordinates

## Sample PDF

A sample PDF (`sample_table.pdf`) has been created for testing. It contains:
- A product invoice table with headers, data, and totals
- A quarterly sales data table with regions and periods

Upload this file to test the application's functionality.

## Features

### ✅ What the Application Does

- **PDF Upload**: Supports PDF files with table content
- **Table Detection**: Automatically detects table structures using pdfplumber
- **Grid Visualization**: Shows visual overlay with detected table grids
- **Coordinate Extraction**: Provides precise x,y coordinates for each cell
- **JSON Export**: Structured data output with complete coordinate information
- **Multi-table Support**: Handles multiple tables on a single page
- **Cell Information**: Extracts text content from each cell
- **Responsive UI**: Clean, modern interface optimized for usability

### 📊 JSON Output Format

```json
{
  "pdf_info": {
    "filename": "example.pdf",
    "page": 0,
    "image_size": {"width": 612, "height": 792},
    "dpi": 200
  },
  "tables": [
    {
      "table_id": 0,
      "bbox": {"x0": 100.0, "y0": 150.0, "x1": 500.0, "y1": 400.0},
      "cells": [
        {
          "row": 0, "col": 0,
          "bbox": {"x0": 100.0, "y0": 150.0, "x1": 200.0, "y1": 200.0},
          "dimensions": {"width": 100.0, "height": 50.0},
          "text": "Header 1"
        }
      ]
    }
  ]
}
```

### 🎯 Coordinate System

- **Origin**: Top-left corner (0, 0)
- **X-axis**: Increases rightward
- **Y-axis**: Increases downward  
- **Units**: PDF points (1/72 inch)

## Troubleshooting

### Common Issues

1. **No tables detected**:
   - Ensure PDF contains actual table structures with borders
   - Try adjusting the DPI setting (increase for better detection)
   - Check that tables have visible grid lines

2. **Poor image quality**:
   - Increase DPI setting in sidebar (200-300 recommended)
   - Ensure original PDF has good quality

3. **Application won't start**:
   - Ensure virtual environment is activated
   - Check that all dependencies are installed
   - Verify poppler-utils is installed on system

### Performance Tips

- Use DPI 150-200 for optimal balance of quality and speed
- Process one page at a time for large documents
- Close other resource-intensive applications if memory usage is high

## Technical Details

### Dependencies
- **Streamlit**: Web application framework
- **pdfplumber**: PDF text and table extraction
- **pdf2image**: PDF to image conversion
- **Pillow**: Image processing and drawing
- **OpenCV**: Computer vision for table structure detection
- **pandas**: Data manipulation and display
- **numpy**: Numerical operations

### File Structure
```
/workspace/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── run.sh                # Startup script
├── create_sample_pdf.py  # Sample PDF generator
├── sample_table.pdf      # Test PDF file
├── README.md             # Project documentation
├── USAGE.md              # This usage guide
└── pdf_table_env/        # Virtual environment
```

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify all dependencies are properly installed
3. Test with the provided sample PDF first
4. Ensure your PDF contains properly formatted tables with visible borders

---

**Enjoy using the PDF Table Grid Mapper!** 🎉