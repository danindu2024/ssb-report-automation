"""
PDF Generation Engine for SSB Monthly Report.
Converts HTML string to PDF using WeasyPrint with custom font configurations.
"""
from weasyprint import HTML
from weasyprint.text.fonts import FontConfiguration
from pathlib import Path

from config import ASSETS_DIR, BASE_DIR

class PDFGenerator:
    def __init__(self, mode='preview'):
        self.mode = mode
        self.font_config = FontConfiguration()

    def generate_pdf(self, html_content, output_path):
        """
        Generates the PDF from HTML content.
        Uses FontConfiguration to ensure Sinhala fonts are loaded and embedded correctly.
        """
        print("📄 Rendering PDF with WeasyPrint...")
        
        try:
            # base_url is set to BASE_DIR so WeasyPrint can resolve any
            # relative paths (e.g. images linked from templates) correctly.
            HTML(string=html_content, base_url=str(BASE_DIR)).write_pdf(
                target=output_path,
                font_config=self.font_config
            )
            print(f"   ✓ Success! Report saved to:\n   {output_path}")
            return True
        except Exception as e:
            print(f"   ❌ Error generating PDF: {str(e)}")
            return False