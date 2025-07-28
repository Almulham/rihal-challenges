# PDF Table Grid Mapper

A Streamlit application that extracts table structures from PDF files and returns precise grid coordinates in JSON format.

## Features

- 📄 **PDF Upload**: Support for PDF files with table content
- 🔍 **Table Detection**: Automatic detection of table structures using pdfplumber
- 📊 **Grid Visualization**: Visual overlay showing detected table grids
- 📋 **JSON Export**: Precise coordinate data in structured JSON format
- ⚙️ **Customizable Settings**: Adjustable DPI and display options
- 📱 **Responsive UI**: Clean, modern interface with wide layout

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. For PDF to image conversion, you may also need to install `poppler-utils`:

**Ubuntu/Debian:**
```bash
sudo apt-get install poppler-utils
```

**macOS:**
```bash
brew install poppler
```

**Windows:**
Download and install poppler from: https://poppler.freedesktop.org/

## Usage

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. Open your browser and navigate to the displayed URL (typically `http://localhost:8501`)

3. Upload a PDF file containing tables

4. Adjust settings in the sidebar:
   - **Image DPI**: Higher values provide better quality but slower processing
   - **Show cell coordinates**: Toggle coordinate labels on the grid overlay

5. View the results:
   - **Left panel**: Original PDF page
   - **Right panel**: Table detection with grid overlay

6. Examine detected tables in the expandable sections

7. Copy or download the JSON output with exact coordinates

## JSON Output Structure

```json
{
  "pdf_info": {
    "filename": "example.pdf",
    "page": 0,
    "image_size": {
      "width": 612,
      "height": 792
    },
    "dpi": 200
  },
  "tables": [
    {
      "table_id": 0,
      "bbox": {
        "x0": 100.0,
        "y0": 150.0,
        "x1": 500.0,
        "y1": 400.0
      },
      "cells": [
        {
          "row": 0,
          "col": 0,
          "bbox": {
            "x0": 100.0,
            "y0": 150.0,
            "x1": 200.0,
            "y1": 200.0
          },
          "dimensions": {
            "width": 100.0,
            "height": 50.0
          },
          "text": "Header 1"
        }
      ]
    }
  ]
}
```

## Coordinate System

- **Origin**: Top-left corner (0, 0)
- **X-axis**: Increases rightward
- **Y-axis**: Increases downward
- **Units**: PDF points (1/72 inch)

## Supported File Types

- PDF files (.pdf)
- Multi-page PDFs (specify page number)

## Technical Details

### Libraries Used

- **Streamlit**: Web application framework
- **pdfplumber**: PDF text and table extraction
- **pdf2image**: PDF to image conversion
- **Pillow**: Image processing and drawing
- **OpenCV**: Computer vision for table structure detection
- **pandas**: Data manipulation and display
- **numpy**: Numerical operations

### Table Detection Methods

1. **Primary**: Uses pdfplumber's built-in table detection
2. **Fallback**: OpenCV-based line detection for complex tables
3. **Grid Generation**: Automatic cell coordinate calculation

## Troubleshooting

### Common Issues

1. **No tables detected**:
   - Ensure the PDF contains actual table structures (not just text formatted to look like tables)
   - Try adjusting the DPI setting
   - Check if the table has visible borders

2. **Poor image quality**:
   - Increase the DPI setting in the sidebar
   - Ensure the original PDF has good quality

3. **Installation issues**:
   - Make sure all dependencies are installed
   - Install poppler-utils for PDF to image conversion
   - Check Python version compatibility (3.7+)

### Performance Tips

- Use lower DPI (100-150) for faster processing of large PDFs
- Process one page at a time for multi-page documents
- Close other applications if memory usage is high

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the application.

## License

This project is open source and available under the MIT License.
