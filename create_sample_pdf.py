#!/usr/bin/env python3
"""
Create a sample PDF with a table for testing the PDF Table Grid Mapper
"""
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch

def create_sample_pdf():
    """Create a sample PDF with a table"""
    filename = "sample_table.pdf"
    
    # Create document
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Content list
    content = []
    
    # Title
    title = Paragraph("Sample Table for PDF Grid Mapper Testing", styles['Title'])
    content.append(title)
    content.append(Spacer(1, 0.2*inch))
    
    # Description
    desc = Paragraph("This PDF contains a sample table to test the grid mapping functionality.", styles['Normal'])
    content.append(desc)
    content.append(Spacer(1, 0.3*inch))
    
    # Sample table data
    table_data = [
        ['Product', 'Quantity', 'Price', 'Total'],
        ['Laptop', '2', '$999.99', '$1,999.98'],
        ['Mouse', '5', '$29.99', '$149.95'],
        ['Keyboard', '3', '$79.99', '$239.97'],
        ['Monitor', '1', '$299.99', '$299.99'],
        ['', '', 'Subtotal:', '$2,689.89'],
        ['', '', 'Tax (8%):', '$215.19'],
        ['', '', 'Total:', '$2,905.08']
    ]
    
    # Create table
    table = Table(table_data, colWidths=[2*inch, 1*inch, 1*inch, 1*inch])
    
    # Table style
    table.setStyle(TableStyle([
        # Header row
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        
        # Data rows
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),  # Right align numbers
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),    # Left align product names
        
        # Grid
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        
        # Totals section
        ('BACKGROUND', (0, -3), (-1, -1), colors.lightgrey),
        ('FONTNAME', (0, -3), (-1, -1), 'Helvetica-Bold'),
    ]))
    
    content.append(table)
    content.append(Spacer(1, 0.3*inch))
    
    # Additional table for more complex testing
    complex_table_data = [
        ['Region', 'Q1', 'Q2', 'Q3', 'Q4', 'Total'],
        ['North', '1,200', '1,350', '1,100', '1,450', '5,100'],
        ['South', '980', '1,120', '1,300', '1,200', '4,600'],
        ['East', '1,450', '1,200', '1,350', '1,500', '5,500'],
        ['West', '1,100', '1,400', '1,250', '1,300', '5,050'],
        ['Total', '4,730', '5,070', '5,000', '5,450', '20,250']
    ]
    
    desc2 = Paragraph("Second table with quarterly sales data:", styles['Normal'])
    content.append(desc2)
    content.append(Spacer(1, 0.2*inch))
    
    complex_table = Table(complex_table_data, colWidths=[1*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch, 1*inch])
    complex_table.setStyle(TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        
        # Data
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        
        # Total row
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightblue),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        
        # Grid
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    content.append(complex_table)
    
    # Build PDF
    doc.build(content)
    print(f"✅ Created sample PDF: {filename}")
    return filename

if __name__ == "__main__":
    try:
        create_sample_pdf()
        print("📄 Sample PDF created successfully!")
        print("📁 You can now upload 'sample_table.pdf' to test the application.")
    except ImportError:
        print("⚠️  ReportLab not installed. Installing...")
        import subprocess
        subprocess.check_call(["pip", "install", "reportlab"])
        create_sample_pdf()
        print("📄 Sample PDF created successfully!")
        print("📁 You can now upload 'sample_table.pdf' to test the application.")
    except Exception as e:
        print(f"❌ Error creating sample PDF: {e}")
        print("💡 You can still test the application with any PDF containing tables.")