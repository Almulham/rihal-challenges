# 📊 PDF Table Grid Mapper

A powerful Streamlit application that allows you to upload PDF files containing tables, overlay custom grids on them, and extract exact coordinates for each grid cell as JSON data.

## 🌟 Features

- **PDF Processing**: Upload and convert PDF pages to high-resolution images
- **Automatic Table Detection**: Use computer vision to automatically detect table regions
- **Custom Grid Overlay**: Create grids with configurable rows and columns
- **Exact Coordinates**: Extract precise pixel coordinates for each grid cell
- **Text Extraction**: Automatically extract text content from each cell
- **Multiple Export Formats**: Download results as JSON with detailed coordinate information
- **Interactive Visualization**: View grid overlays with Plotly visualizations
- **Multi-page Support**: Process PDFs with multiple pages

## 🚀 Quick Start

### Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

### System Requirements

You may need to install additional system dependencies for PDF processing:

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install poppler-utils
sudo apt-get install libgl1-mesa-glx
```

**macOS:**
```bash
brew install poppler
```

**Windows:**
- Download poppler for Windows and add it to your PATH
- Or use conda: `conda install -c conda-forge poppler`

### Running the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## 📖 How to Use

### Step 1: Upload PDF
- Use the sidebar file uploader to select your PDF file
- Click "Process PDF" to convert pages to images

### Step 2: Configure Grid
- Select the page you want to process (if multi-page PDF)
- Optionally click "Detect Table Regions" for automatic table detection
- Set the number of rows and columns for your grid
- Choose whether to use the full page or a specific detected region

### Step 3: Generate Grid
- Click "Generate Grid" to create the overlay
- The application will draw red grid lines over your PDF page
- Text will be automatically extracted from each cell

### Step 4: Export Results
- View results in three different formats:
  - **Table View**: Spreadsheet-like display of all coordinates
  - **JSON Output**: Raw JSON data with complete coordinate information
  - **Visualization**: Interactive Plotly chart showing the grid layout
- Download the JSON file with exact coordinates

## 📊 Output JSON Structure

The exported JSON contains detailed information for each grid cell:

```json
{
  "cell_0_0": {
    "row": 0,
    "col": 0,
    "x": 45.5,
    "y": 123.2,
    "width": 150.0,
    "height": 75.0,
    "center_x": 120.5,
    "center_y": 160.7,
    "text": "Header 1"
  },
  "cell_0_1": {
    "row": 0,
    "col": 1,
    "x": 195.5,
    "y": 123.2,
    "width": 150.0,
    "height": 75.0,
    "center_x": 270.5,
    "center_y": 160.7,
    "text": "Header 2"
  }
}
```

### Coordinate System
- **x, y**: Top-left corner of the cell (in pixels)
- **width, height**: Dimensions of the cell (in pixels)
- **center_x, center_y**: Center point of the cell (in pixels)
- **row, col**: Grid position (0-indexed)
- **text**: Extracted text content from the cell

## 🛠️ Technical Details

### Libraries Used
- **Streamlit**: Web application framework
- **pdf2image**: PDF to image conversion
- **OpenCV**: Computer vision for table detection
- **PIL/Pillow**: Image processing
- **pdfplumber**: Text extraction from PDFs
- **Plotly**: Interactive visualizations
- **Pandas**: Data manipulation

### Table Detection Algorithm
The automatic table detection uses OpenCV to:
1. Convert the image to grayscale
2. Apply binary thresholding
3. Detect horizontal and vertical lines using morphological operations
4. Find contours and filter by area to identify table regions

### Grid Generation
The grid overlay system:
1. Calculates cell dimensions based on the specified rows/columns
2. Draws red grid lines over the image
3. Stores exact pixel coordinates for each cell
4. Extracts text content using PDF text extraction

## 🎯 Use Cases

- **Data Entry**: Create templates for manual data entry from scanned documents
- **Document Analysis**: Analyze the structure of tabular data in PDFs
- **OCR Preprocessing**: Prepare coordinate data for OCR systems
- **Form Processing**: Extract field positions from PDF forms
- **Research**: Analyze document layouts for academic research

## 🔧 Customization

### Adjusting Table Detection
You can modify the table detection sensitivity by changing the area threshold in the `detect_table_regions` method:

```python
if area > 5000:  # Adjust this value
```

### Grid Styling
Modify the grid line appearance in the `create_grid_overlay` method:

```python
draw.line([(x, y_pos), (x + w, y_pos)], fill='red', width=2)  # Change color/width
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📄 License

This project is open source and available under the MIT License.

## 🐛 Troubleshooting

### Common Issues

1. **PDF not loading**: Ensure poppler is installed correctly
2. **Text extraction failing**: Some PDFs may have text as images - consider adding OCR functionality
3. **Memory issues with large PDFs**: Try reducing the DPI in the `convert_from_bytes` function
4. **Grid not aligned**: Adjust the detected table region or use manual region selection

### Performance Tips

- Use lower DPI (150-200) for faster processing of large PDFs
- Process one page at a time for very large documents
- Close the application and restart if memory usage becomes high

## 📞 Support

If you encounter any issues or have questions, please open an issue on the repository or contact the maintainers.
