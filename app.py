import streamlit as st
import json
import numpy as np
from PIL import Image, ImageDraw
import pdf2image
import pdfplumber
import cv2
import pandas as pd
from streamlit_drawable_canvas import st_canvas
import io
import base64

def convert_pdf_to_image(pdf_file, page_num=0, dpi=200):
    """Convert PDF page to image"""
    try:
        images = pdf2image.convert_from_bytes(
            pdf_file.read(),
            first_page=page_num + 1,
            last_page=page_num + 1,
            dpi=dpi
        )
        return images[0] if images else None
    except Exception as e:
        st.error(f"Error converting PDF to image: {str(e)}")
        return None

def detect_table_structure(image):
    """Detect table structure using OpenCV"""
    # Convert PIL image to OpenCV format
    opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
    
    # Apply threshold to get binary image
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    
    # Detect horizontal lines
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
    horizontal_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    
    # Detect vertical lines
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
    vertical_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
    
    # Combine horizontal and vertical lines
    table_mask = cv2.addWeighted(horizontal_lines, 0.5, vertical_lines, 0.5, 0.0)
    
    return table_mask, horizontal_lines, vertical_lines

def extract_table_coordinates(pdf_file, page_num=0):
    """Extract table coordinates using pdfplumber"""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            if page_num < len(pdf.pages):
                page = pdf.pages[page_num]
                tables = page.find_tables()
                
                table_data = []
                for i, table in enumerate(tables):
                    bbox = table.bbox  # (x0, top, x1, bottom)
                    
                    # Extract table cells
                    cells = []
                    if hasattr(table, 'cells') and table.cells:
                        for row_idx, row in enumerate(table.cells):
                            for col_idx, cell in enumerate(row):
                                if cell:
                                    cells.append({
                                        'row': row_idx,
                                        'col': col_idx,
                                        'bbox': cell,
                                        'text': ''
                                    })
                    
                    # If cells not available, create grid based on table bbox
                    if not cells:
                        # Try to extract table data
                        table_data_extracted = table.extract()
                        if table_data_extracted:
                            rows = len(table_data_extracted)
                            cols = len(table_data_extracted[0]) if table_data_extracted[0] else 0
                            
                            # Calculate cell dimensions
                            cell_width = (bbox[2] - bbox[0]) / cols if cols > 0 else 0
                            cell_height = (bbox[3] - bbox[1]) / rows if rows > 0 else 0
                            
                            for row_idx in range(rows):
                                for col_idx in range(cols):
                                    x0 = bbox[0] + col_idx * cell_width
                                    y0 = bbox[1] + row_idx * cell_height
                                    x1 = x0 + cell_width
                                    y1 = y0 + cell_height
                                    
                                    cell_text = ''
                                    if (row_idx < len(table_data_extracted) and 
                                        col_idx < len(table_data_extracted[row_idx]) and 
                                        table_data_extracted[row_idx][col_idx]):
                                        cell_text = str(table_data_extracted[row_idx][col_idx])
                                    
                                    cells.append({
                                        'row': row_idx,
                                        'col': col_idx,
                                        'bbox': (x0, y0, x1, y1),
                                        'text': cell_text
                                    })
                    
                    table_data.append({
                        'table_id': i,
                        'table_bbox': bbox,
                        'cells': cells
                    })
                
                return table_data
    except Exception as e:
        st.error(f"Error extracting table coordinates: {str(e)}")
        return []

def draw_grid_on_image(image, table_data, show_text=True):
    """Draw grid overlay on the image"""
    draw_image = image.copy()
    draw = ImageDraw.Draw(draw_image)
    
    colors = ['red', 'blue', 'green', 'orange', 'purple']
    
    for table_idx, table_info in enumerate(table_data):
        color = colors[table_idx % len(colors)]
        
        # Draw table boundary
        bbox = table_info['table_bbox']
        draw.rectangle(bbox, outline=color, width=3)
        
        # Draw cells
        for cell in table_info['cells']:
            cell_bbox = cell['bbox']
            draw.rectangle(cell_bbox, outline=color, width=1)
            
            # Add cell coordinates as text
            if show_text:
                text = f"({cell['row']},{cell['col']})"
                text_bbox = draw.textbbox((0, 0), text)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                
                # Position text in center of cell
                text_x = cell_bbox[0] + (cell_bbox[2] - cell_bbox[0] - text_width) / 2
                text_y = cell_bbox[1] + (cell_bbox[3] - cell_bbox[1] - text_height) / 2
                
                draw.text((text_x, text_y), text, fill=color)
    
    return draw_image

def main():
    st.set_page_config(
        page_title="PDF Table Grid Mapper",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 PDF Table Grid Mapper")
    st.markdown("Upload a PDF with tables and extract grid coordinates as JSON")
    
    # Sidebar for settings
    st.sidebar.header("Settings")
    dpi = st.sidebar.slider("Image DPI", 100, 300, 200, help="Higher DPI = better quality but slower processing")
    show_coordinates = st.sidebar.checkbox("Show cell coordinates on image", True)
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type="pdf",
        help="Upload a PDF file containing tables"
    )
    
    if uploaded_file is not None:
        # Reset file pointer
        uploaded_file.seek(0)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📄 Original PDF Page")
            
            # Convert PDF to image
            with st.spinner("Converting PDF to image..."):
                pdf_image = convert_pdf_to_image(uploaded_file, dpi=dpi)
            
            if pdf_image:
                st.image(pdf_image, caption="Original PDF Page", use_column_width=True)
                
                # Page selection (if needed for multi-page PDFs)
                page_num = st.number_input("Page Number", min_value=0, value=0, help="Page to process (0-indexed)")
        
        with col2:
            st.subheader("🔍 Table Detection & Grid")
            
            if pdf_image:
                # Reset file pointer for table extraction
                uploaded_file.seek(0)
                
                with st.spinner("Extracting table coordinates..."):
                    table_data = extract_table_coordinates(uploaded_file, page_num)
                
                if table_data:
                    # Draw grid on image
                    grid_image = draw_grid_on_image(pdf_image, table_data, show_coordinates)
                    st.image(grid_image, caption="Table Grid Overlay", use_column_width=True)
                    
                    # Display table information
                    st.subheader("📊 Detected Tables")
                    for i, table_info in enumerate(table_data):
                        with st.expander(f"Table {i + 1} ({len(table_info['cells'])} cells)"):
                            st.write(f"**Table Boundary:** {table_info['table_bbox']}")
                            
                            # Show cells in a dataframe
                            if table_info['cells']:
                                cells_df = pd.DataFrame([
                                    {
                                        'Row': cell['row'],
                                        'Col': cell['col'],
                                        'X0': round(cell['bbox'][0], 2),
                                        'Y0': round(cell['bbox'][1], 2),
                                        'X1': round(cell['bbox'][2], 2),
                                        'Y1': round(cell['bbox'][3], 2),
                                        'Width': round(cell['bbox'][2] - cell['bbox'][0], 2),
                                        'Height': round(cell['bbox'][3] - cell['bbox'][1], 2),
                                        'Text': cell['text'][:50] + '...' if len(cell['text']) > 50 else cell['text']
                                    }
                                    for cell in table_info['cells']
                                ])
                                st.dataframe(cells_df, use_container_width=True)
                    
                    # JSON Output
                    st.subheader("📋 JSON Output")
                    
                    # Prepare JSON data
                    json_data = {
                        'pdf_info': {
                            'filename': uploaded_file.name,
                            'page': page_num,
                            'image_size': {
                                'width': pdf_image.width,
                                'height': pdf_image.height
                            },
                            'dpi': dpi
                        },
                        'tables': []
                    }
                    
                    for table_info in table_data:
                        table_json = {
                            'table_id': table_info['table_id'],
                            'bbox': {
                                'x0': table_info['table_bbox'][0],
                                'y0': table_info['table_bbox'][1],
                                'x1': table_info['table_bbox'][2],
                                'y1': table_info['table_bbox'][3]
                            },
                            'cells': []
                        }
                        
                        for cell in table_info['cells']:
                            cell_json = {
                                'row': cell['row'],
                                'col': cell['col'],
                                'bbox': {
                                    'x0': cell['bbox'][0],
                                    'y0': cell['bbox'][1],
                                    'x1': cell['bbox'][2],
                                    'y1': cell['bbox'][3]
                                },
                                'dimensions': {
                                    'width': cell['bbox'][2] - cell['bbox'][0],
                                    'height': cell['bbox'][3] - cell['bbox'][1]
                                },
                                'text': cell['text']
                            }
                            table_json['cells'].append(cell_json)
                        
                        json_data['tables'].append(table_json)
                    
                    # Display JSON
                    json_str = json.dumps(json_data, indent=2)
                    st.code(json_str, language='json')
                    
                    # Download button
                    st.download_button(
                        label="📥 Download JSON",
                        data=json_str,
                        file_name=f"{uploaded_file.name.replace('.pdf', '')}_table_coordinates.json",
                        mime="application/json"
                    )
                    
                else:
                    st.warning("No tables detected in the PDF. Try adjusting the DPI or check if the PDF contains table structures.")
    
    # Instructions
    with st.expander("ℹ️ How to use"):
        st.markdown("""
        1. **Upload a PDF**: Choose a PDF file that contains tables
        2. **Adjust Settings**: Use the sidebar to modify DPI and display options
        3. **View Results**: 
           - Left panel shows the original PDF page
           - Right panel shows the detected table grid overlay
        4. **Examine Tables**: Expand the table sections to see detailed cell information
        5. **Export Data**: Copy or download the JSON with exact coordinates
        
        **JSON Structure**:
        - `pdf_info`: Metadata about the PDF and processing settings
        - `tables`: Array of detected tables
        - Each table contains `bbox` (boundary) and `cells` array
        - Each cell has `row`, `col`, `bbox` coordinates, `dimensions`, and extracted `text`
        
        **Coordinate System**: 
        - Origin (0,0) is at the top-left corner
        - X increases rightward, Y increases downward
        - All coordinates are in PDF points (1/72 inch)
        """)

if __name__ == "__main__":
    main()