#!/usr/bin/env python3
"""
Test script for PDF Table Grid Mapper functionality
"""

import sys
import os
from PIL import Image, ImageDraw
import json

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the main class from our app
try:
    from app import PDFTableGridMapper
    print("✅ Successfully imported PDFTableGridMapper")
except ImportError as e:
    print(f"❌ Failed to import PDFTableGridMapper: {e}")
    sys.exit(1)

def test_basic_functionality():
    """Test basic functionality without PDF processing"""
    print("\n🧪 Testing basic functionality...")
    
    # Create a test instance
    mapper = PDFTableGridMapper()
    print("✅ PDFTableGridMapper instance created")
    
    # Create a test image
    test_image = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(test_image)
    
    # Draw some test table-like structure
    for i in range(1, 6):
        y = i * 100
        draw.line([(50, y), (750, y)], fill='black', width=2)
    
    for j in range(1, 8):
        x = j * 100
        draw.line([(x, 50), (x, 550)], fill='black', width=2)
    
    print("✅ Test image created with table structure")
    
    # Test grid overlay
    try:
        grid_image, grid_coords = mapper.create_grid_overlay(test_image, 5, 7)
        print(f"✅ Grid overlay created with {len(grid_coords)} cells")
        
        # Test JSON serialization
        json_output = json.dumps(grid_coords, indent=2)
        print("✅ Grid coordinates successfully converted to JSON")
        
        # Display sample coordinates
        sample_key = list(grid_coords.keys())[0]
        sample_cell = grid_coords[sample_key]
        print(f"\n📊 Sample cell ({sample_key}):")
        print(f"   Position: ({sample_cell['x']:.1f}, {sample_cell['y']:.1f})")
        print(f"   Size: {sample_cell['width']:.1f} × {sample_cell['height']:.1f}")
        print(f"   Center: ({sample_cell['center_x']:.1f}, {sample_cell['center_y']:.1f})")
        
        return True
        
    except Exception as e:
        print(f"❌ Grid overlay test failed: {e}")
        return False

def test_table_detection():
    """Test table detection functionality"""
    print("\n🔍 Testing table detection...")
    
    mapper = PDFTableGridMapper()
    
    # Create a more complex test image with table structure
    test_image = Image.new('RGB', (1000, 800), color='white')
    draw = ImageDraw.Draw(test_image)
    
    # Draw a table with clear lines
    # Horizontal lines
    for i in range(6):
        y = 200 + i * 80
        draw.line([(100, y), (900, y)], fill='black', width=3)
    
    # Vertical lines
    for j in range(5):
        x = 100 + j * 200
        draw.line([(x, 200), (x, 600)], fill='black', width=3)
    
    try:
        table_regions = mapper.detect_table_regions(test_image)
        print(f"✅ Table detection completed, found {len(table_regions)} regions")
        
        if table_regions:
            for i, region in enumerate(table_regions):
                x, y, w, h = region
                print(f"   Region {i+1}: x={x}, y={y}, width={w}, height={h}")
        
        return True
        
    except Exception as e:
        print(f"❌ Table detection test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting PDF Table Grid Mapper Tests")
    print("=" * 50)
    
    # Test basic functionality
    test1_passed = test_basic_functionality()
    
    # Test table detection
    test2_passed = test_table_detection()
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Test Summary:")
    print(f"   Basic functionality: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"   Table detection: {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 All tests passed! The application is ready to use.")
        print("\n🌐 To start the Streamlit app, run:")
        print("   source venv/bin/activate && streamlit run app.py")
    else:
        print("\n⚠️  Some tests failed. Please check the error messages above.")
    
    return test1_passed and test2_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)