from weasyprint import HTML, CSS
from pathlib import Path

# define base path
BASE_DIR = Path(__file__).parent.parent # specific to where this script is located
ASSETS_DIR = BASE_DIR / "assets"

def render_report(html_content, output_filename):
    # 1. Load CSS explicitly
    css_path = ASSETS_DIR / "styles" / "report_style.css"
    
    # 2. Prepare HTML with base_url
    # The base_url is critical! It tells WeasyPrint that when CSS says "../fonts",
    # it should look relative to the assets folder.
    
    print("Rendering PDF...")
    
    HTML(string=html_content, base_url=str(ASSETS_DIR)).write_pdf(
        output_filename,
        stylesheets=[CSS(css_path)]
    )
    print(f"Success! Report saved to {output_filename}")