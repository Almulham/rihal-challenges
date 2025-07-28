import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw
import json
import io
import base64
from pdf2image import convert_from_bytes
import pdfplumber
import cv2
from streamlit_drawable_canvas import st_canvas
import plotly.graph_objects as go
import plotly.express as px

# Set page config
st.set_page_config(
    page_title="PDF Table Grid Mapper",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .step-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        background-color: #f8f9fa;
        margin: 1rem 0;
    }
    .coordinate-display {
        background-color: #f1f3f4;
        padding: 1rem;
        border-radius: 0.5rem;
        font-family: monospace;
        white-space: pre-wrap;
    }
</style>
""", unsafe_allow_html=True)

class PDFTableGridMapper:
    def __init__(self):
        self.pdf_pages = []
        self.current_page_image = None
        self.grid_coordinates = {}
        
    def extract_pdf_pages(self, pdf_file):
        """Extract pages from PDF as images"""
        try:
            # Convert PDF to images
            images = convert_from_bytes(pdf_file.read(), dpi=300)
            self.pdf_pages = images
            return True
        except Exception as e:
            st.error(f"Error processing PDF: {str(e)}")
            return False
    
    def detect_table_regions(self, page_image):
        """Detect potential table regions using OpenCV"""
        # Convert PIL image to OpenCV format
        img_array = np.array(page_image)
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        
        # Apply threshold to get binary image
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # Find horizontal and vertical lines
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
        
        horizontal_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, horizontal_kernel)
        vertical_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, vertical_kernel)
        
        # Combine horizontal and vertical lines
        table_mask = cv2.addWeighted(horizontal_lines, 0.5, vertical_lines, 0.5, 0.0)
        
        # Find contours
        contours, _ = cv2.findContours(table_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter contours by area to find table regions
        table_regions = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 5000:  # Minimum area threshold
                x, y, w, h = cv2.boundingRect(contour)
                table_regions.append((x, y, w, h))
        
        return table_regions
    
    def create_grid_overlay(self, image, rows, cols, region=None):
        """Create a grid overlay on the image"""
        img_copy = image.copy()
        draw = ImageDraw.Draw(img_copy)
        
        if region:
            x, y, w, h = region
        else:
            x, y, w, h = 0, 0, image.width, image.height
        
        # Calculate grid cell dimensions
        cell_width = w / cols
        cell_height = h / rows
        
        grid_coords = {}
        
        # Draw grid lines and store coordinates
        for i in range(rows + 1):
            y_pos = y + i * cell_height
            draw.line([(x, y_pos), (x + w, y_pos)], fill='red', width=2)
            
        for j in range(cols + 1):
            x_pos = x + j * cell_width
            draw.line([(x_pos, y), (x_pos, y + h)], fill='red', width=2)
        
        # Store cell coordinates
        for i in range(rows):
            for j in range(cols):
                cell_x = x + j * cell_width
                cell_y = y + i * cell_height
                cell_key = f"cell_{i}_{j}"
                grid_coords[cell_key] = {
                    "row": i,
                    "col": j,
                    "x": float(cell_x),
                    "y": float(cell_y),
                    "width": float(cell_width),
                    "height": float(cell_height),
                    "center_x": float(cell_x + cell_width/2),
                    "center_y": float(cell_y + cell_height/2)
                }
        
        return img_copy, grid_coords
    
    def extract_text_from_cells(self, pdf_file, page_num, grid_coords):
        """Extract text from each grid cell using pdfplumber"""
        try:
            with pdfplumber.open(pdf_file) as pdf:
                page = pdf.pages[page_num]
                
                for cell_key, coords in grid_coords.items():
                    # Define the bounding box for the cell
                    bbox = (
                        coords["x"],
                        coords["y"],
                        coords["x"] + coords["width"],
                        coords["y"] + coords["height"]
                    )
                    
                    # Extract text from the cell region
                    cell_text = page.within_bbox(bbox).extract_text()
                    coords["text"] = cell_text.strip() if cell_text else ""
                    
        except Exception as e:
            st.warning(f"Could not extract text: {str(e)}")
            # Add empty text if extraction fails
            for coords in grid_coords.values():
                coords["text"] = ""
        
        return grid_coords

def main():
    st.markdown('<h1 class="main-header">📊 PDF Table Grid Mapper</h1>', unsafe_allow_html=True)
    
    # Initialize the mapper
    if 'mapper' not in st.session_state:
        st.session_state.mapper = PDFTableGridMapper()
    
    mapper = st.session_state.mapper
    
    # Sidebar for controls
    with st.sidebar:
        st.markdown('<h2 class="step-header">🔧 Controls</h2>', unsafe_allow_html=True)
        
        # File upload
        uploaded_file = st.file_uploader(
            "Upload PDF file",
            type=['pdf'],
            help="Upload a PDF file containing tables"
        )
        
        if uploaded_file:
            st.success("PDF uploaded successfully!")
            
            # Process PDF
            if st.button("📄 Process PDF", type="primary"):
                with st.spinner("Processing PDF..."):
                    success = mapper.extract_pdf_pages(uploaded_file)
                    if success:
                        st.success(f"Extracted {len(mapper.pdf_pages)} pages")
                        st.session_state.pdf_processed = True
    
    # Main content area
    if uploaded_file and hasattr(st.session_state, 'pdf_processed'):
        
        # Page selection
        if len(mapper.pdf_pages) > 1:
            page_num = st.selectbox(
                "Select page to process:",
                range(len(mapper.pdf_pages)),
                format_func=lambda x: f"Page {x + 1}"
            )
        else:
            page_num = 0
        
        current_page = mapper.pdf_pages[page_num]
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown('<h3 class="step-header">🖼️ PDF Page</h3>', unsafe_allow_html=True)
            
            # Display the PDF page
            st.image(current_page, caption=f"Page {page_num + 1}", use_column_width=True)
            
            # Table detection
            if st.button("🔍 Detect Table Regions"):
                with st.spinner("Detecting tables..."):
                    table_regions = mapper.detect_table_regions(current_page)
                    st.session_state.table_regions = table_regions
                    if table_regions:
                        st.success(f"Found {len(table_regions)} potential table regions")
                    else:
                        st.warning("No table regions detected automatically")
        
        with col2:
            st.markdown('<h3 class="step-header">⚙️ Grid Configuration</h3>', unsafe_allow_html=True)
            
            # Grid configuration
            rows = st.number_input("Number of rows:", min_value=1, max_value=50, value=5)
            cols = st.number_input("Number of columns:", min_value=1, max_value=20, value=4)
            
            # Region selection
            use_full_page = st.checkbox("Use full page", value=True)
            
            if not use_full_page and hasattr(st.session_state, 'table_regions'):
                if st.session_state.table_regions:
                    region_idx = st.selectbox(
                        "Select table region:",
                        range(len(st.session_state.table_regions)),
                        format_func=lambda x: f"Region {x + 1}"
                    )
                    selected_region = st.session_state.table_regions[region_idx]
                else:
                    st.warning("No regions detected. Using full page.")
                    selected_region = None
                    use_full_page = True
            else:
                selected_region = None
            
            # Generate grid
            if st.button("🎯 Generate Grid", type="primary"):
                with st.spinner("Generating grid..."):
                    region = None if use_full_page else selected_region
                    grid_image, grid_coords = mapper.create_grid_overlay(
                        current_page, rows, cols, region
                    )
                    
                    # Extract text from cells
                    uploaded_file.seek(0)  # Reset file pointer
                    grid_coords = mapper.extract_text_from_cells(
                        uploaded_file, page_num, grid_coords
                    )
                    
                    st.session_state.grid_image = grid_image
                    st.session_state.grid_coordinates = grid_coords
                    st.success("Grid generated successfully!")
        
        # Display grid result
        if hasattr(st.session_state, 'grid_image'):
            st.markdown('<h3 class="step-header">🎯 Grid Overlay Result</h3>', unsafe_allow_html=True)
            
            col1, col2 = st.columns([3, 2])
            
            with col1:
                st.image(st.session_state.grid_image, caption="Grid Overlay", use_column_width=True)
            
            with col2:
                st.markdown('<h4>📊 Grid Statistics</h4>', unsafe_allow_html=True)
                coords = st.session_state.grid_coordinates
                st.metric("Total Cells", len(coords))
                st.metric("Rows", rows)
                st.metric("Columns", cols)
                
                # Show sample cell info
                if coords:
                    sample_key = list(coords.keys())[0]
                    sample_cell = coords[sample_key]
                    st.markdown("**Sample Cell Info:**")
                    st.write(f"Position: ({sample_cell['x']:.1f}, {sample_cell['y']:.1f})")
                    st.write(f"Size: {sample_cell['width']:.1f} × {sample_cell['height']:.1f}")
        
        # Display coordinates and export options
        if hasattr(st.session_state, 'grid_coordinates'):
            st.markdown('<h3 class="step-header">📋 Grid Coordinates & Export</h3>', unsafe_allow_html=True)
            
            coords = st.session_state.grid_coordinates
            
            # Create tabs for different views
            tab1, tab2, tab3 = st.tabs(["📊 Table View", "🗂️ JSON Output", "📈 Visualization"])
            
            with tab1:
                # Convert to DataFrame for display
                df_data = []
                for cell_key, cell_data in coords.items():
                    df_data.append({
                        'Cell': cell_key,
                        'Row': cell_data['row'],
                        'Col': cell_data['col'],
                        'X': round(cell_data['x'], 2),
                        'Y': round(cell_data['y'], 2),
                        'Width': round(cell_data['width'], 2),
                        'Height': round(cell_data['height'], 2),
                        'Center X': round(cell_data['center_x'], 2),
                        'Center Y': round(cell_data['center_y'], 2),
                        'Text': cell_data.get('text', '')[:50] + '...' if len(cell_data.get('text', '')) > 50 else cell_data.get('text', '')
                    })
                
                df = pd.DataFrame(df_data)
                st.dataframe(df, use_container_width=True)
            
            with tab2:
                # JSON output
                json_output = json.dumps(coords, indent=2)
                st.markdown('<div class="coordinate-display">', unsafe_allow_html=True)
                st.code(json_output, language='json')
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Download button
                st.download_button(
                    label="📥 Download JSON",
                    data=json_output,
                    file_name=f"grid_coordinates_page_{page_num + 1}.json",
                    mime="application/json"
                )
            
            with tab3:
                # Create interactive visualization
                fig = go.Figure()
                
                # Add rectangles for each cell
                for cell_key, cell_data in coords.items():
                    fig.add_shape(
                        type="rect",
                        x0=cell_data['x'],
                        y0=cell_data['y'],
                        x1=cell_data['x'] + cell_data['width'],
                        y1=cell_data['y'] + cell_data['height'],
                        line=dict(color="red", width=2),
                        fillcolor="rgba(255,0,0,0.1)"
                    )
                    
                    # Add cell labels
                    fig.add_annotation(
                        x=cell_data['center_x'],
                        y=cell_data['center_y'],
                        text=f"{cell_data['row']},{cell_data['col']}",
                        font=dict(size=10, color="blue"),
                        showarrow=False
                    )
                
                # Set layout
                fig.update_layout(
                    title="Grid Visualization",
                    xaxis_title="X Coordinate",
                    yaxis_title="Y Coordinate",
                    yaxis=dict(autorange="reversed"),  # Flip Y axis to match image coordinates
                    showlegend=False,
                    height=600
                )
                
                st.plotly_chart(fig, use_container_width=True)
    
    else:
        # Welcome screen
        st.markdown("""
        <div class="info-box">
            <h3>Welcome to PDF Table Grid Mapper! 🎯</h3>
            <p>This tool helps you:</p>
            <ul>
                <li>📄 Upload and process PDF files</li>
                <li>🔍 Automatically detect table regions</li>
                <li>🎯 Create custom grids over tables</li>
                <li>📊 Extract exact coordinates for each cell</li>
                <li>📥 Export results as JSON</li>
            </ul>
            <p><strong>Get started by uploading a PDF file in the sidebar!</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Add usage instructions
        with st.expander("📖 How to use this tool"):
            st.markdown("""
            1. **Upload PDF**: Use the sidebar to upload your PDF file
            2. **Process PDF**: Click "Process PDF" to extract pages as images
            3. **Select Page**: Choose which page contains your table
            4. **Detect Tables**: Optionally use automatic table detection
            5. **Configure Grid**: Set the number of rows and columns
            6. **Generate Grid**: Create the grid overlay on your table
            7. **Export Results**: Download the coordinates as JSON
            
            **Features:**
            - Automatic table region detection using computer vision
            - Interactive grid configuration
            - Text extraction from each cell
            - Multiple export formats (JSON, CSV)
            - Visual grid overlay with exact coordinates
            """)

if __name__ == "__main__":
    main()