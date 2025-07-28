#!/usr/bin/env python3
"""
Example usage of PDF Table Grid Mapper
This script demonstrates how to use the PDFTableGridMapper programmatically
"""

import json
from PIL import Image, ImageDraw
from app import PDFTableGridMapper

def create_sample_table_image():
    """Create a sample image with a table structure for demonstration"""
    # Create a white background image
    img = Image.new('RGB', (1200, 800), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw table borders
    table_x, table_y = 100, 150
    table_width, table_height = 1000, 500
    
    # Draw outer border
    draw.rectangle([table_x, table_y, table_x + table_width, table_y + table_height], 
                   outline='black', width=3)
    
    # Draw grid lines
    rows, cols = 5, 4
    row_height = table_height // rows
    col_width = table_width // cols
    
    # Horizontal lines
    for i in range(1, rows):
        y = table_y + i * row_height
        draw.line([(table_x, y), (table_x + table_width, y)], fill='black', width=2)
    
    # Vertical lines
    for j in range(1, cols):
        x = table_x + j * col_width
        draw.line([(x, table_y), (x, table_y + table_height)], fill='black', width=2)
    
    # Add some sample text
    sample_data = [
        ["Header 1", "Header 2", "Header 3", "Header 4"],
        ["Row 1 Col 1", "Row 1 Col 2", "Row 1 Col 3", "Row 1 Col 4"],
        ["Row 2 Col 1", "Row 2 Col 2", "Row 2 Col 3", "Row 2 Col 4"],
        ["Row 3 Col 1", "Row 3 Col 2", "Row 3 Col 3", "Row 3 Col 4"],
        ["Row 4 Col 1", "Row 4 Col 2", "Row 4 Col 3", "Row 4 Col 4"]
    ]
    
    for i, row in enumerate(sample_data):
        for j, cell_text in enumerate(row):
            x = table_x + j * col_width + 10
            y = table_y + i * row_height + 20
            draw.text((x, y), cell_text, fill='black')
    
    return img

def main():
    """Demonstrate the PDF Table Grid Mapper functionality"""
    print("📊 PDF Table Grid Mapper - Example Usage")
    print("=" * 50)
    
    # Create mapper instance
    mapper = PDFTableGridMapper()
    print("✅ Created PDFTableGridMapper instance")
    
    # Create sample table image
    print("🖼️  Creating sample table image...")
    sample_image = create_sample_table_image()
    print("✅ Sample table image created")
    
    # Detect table regions
    print("\n🔍 Detecting table regions...")
    table_regions = mapper.detect_table_regions(sample_image)
    print(f"✅ Found {len(table_regions)} table region(s)")
    
    if table_regions:
        for i, (x, y, w, h) in enumerate(table_regions):
            print(f"   Region {i+1}: x={x}, y={y}, width={w}, height={h}")
    
    # Create grid overlay
    print("\n🎯 Creating grid overlay...")
    rows, cols = 5, 4
    
    # Use detected region if available, otherwise use full image
    region = table_regions[0] if table_regions else None
    
    grid_image, grid_coords = mapper.create_grid_overlay(
        sample_image, rows, cols, region
    )
    print(f"✅ Grid overlay created with {len(grid_coords)} cells")
    
    # Display grid statistics
    print(f"\n📊 Grid Statistics:")
    print(f"   Rows: {rows}")
    print(f"   Columns: {cols}")
    print(f"   Total cells: {len(grid_coords)}")
    
    # Show sample cell coordinates
    print(f"\n📋 Sample Cell Coordinates:")
    for i, (cell_key, cell_data) in enumerate(list(grid_coords.items())[:3]):
        print(f"   {cell_key}:")
        print(f"      Position: ({cell_data['x']:.1f}, {cell_data['y']:.1f})")
        print(f"      Size: {cell_data['width']:.1f} × {cell_data['height']:.1f}")
        print(f"      Center: ({cell_data['center_x']:.1f}, {cell_data['center_y']:.1f})")
        print(f"      Row: {cell_data['row']}, Column: {cell_data['col']}")
    
    # Export to JSON
    print(f"\n💾 Exporting coordinates to JSON...")
    json_output = json.dumps(grid_coords, indent=2)
    
    # Save to file
    with open('sample_grid_coordinates.json', 'w') as f:
        f.write(json_output)
    
    print("✅ Coordinates exported to 'sample_grid_coordinates.json'")
    
    # Save images
    print(f"\n🖼️  Saving images...")
    sample_image.save('sample_table.png')
    grid_image.save('sample_table_with_grid.png')
    print("✅ Images saved:")
    print("   - sample_table.png (original)")
    print("   - sample_table_with_grid.png (with grid overlay)")
    
    print(f"\n🎉 Example completed successfully!")
    print(f"\nFiles created:")
    print(f"   📄 sample_grid_coordinates.json - Grid coordinates in JSON format")
    print(f"   🖼️  sample_table.png - Original table image")
    print(f"   🖼️  sample_table_with_grid.png - Table with grid overlay")
    
    print(f"\n🌐 To use the interactive Streamlit interface:")
    print(f"   streamlit run app.py")

if __name__ == "__main__":
    main()