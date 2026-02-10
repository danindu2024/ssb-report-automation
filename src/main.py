import argparse
import sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from chart_generator import generate_district_chart

# Import your custom modules
from data_loader import DataLoader
from report_generator import render_report

# Setup Paths
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR / "templates"
OUTPUT_DIR = BASE_DIR / "output"

def main():
    # 1. Setup Command Line Arguments
    parser = argparse.ArgumentParser(description="SSB Monthly Report Generator (WeasyPrint)")
    parser.add_argument(
        '--input', 
        type=str, 
        default='Annual_Report_Master_2026.xlsx',
        help='Name of the Excel file in the project root'
    )
    parser.add_argument(
        '--output', 
        type=str, 
        default='SSB_Monthly_Report.pdf', 
        help='Name of the output PDF'
    )
    args = parser.parse_args()

    # Define full file paths
    excel_path = BASE_DIR / args.input
    output_pdf_path = OUTPUT_DIR / args.output

    # Ensure Output Directory Exists
    OUTPUT_DIR.mkdir(exist_ok=True)

    print(f"\n🚀 Starting Report Generation")
    print(f"   Input: {excel_path}")
    print(f"   Output: {output_pdf_path}")
    print("-" * 40)

    try:
        # 2. Load Data from Excel
        print("📥 Step 1: Loading Data...")
        if not excel_path.exists():
            raise FileNotFoundError(f"Excel file not found at: {excel_path}")
        
        loader = DataLoader(excel_path)
        data_context = loader.load_data()

        # 2.5 Generate Visualizations [NEW STEP]
        print("📊 Step 2.5: Generating Charts...")
        chart_filename = generate_district_chart(data_context['district_performance'])
        
        # Add the filename to the context so Jinja knows what to look for
        data_context['chart_district'] = chart_filename
        
        # 3. Render HTML with Jinja2
        print("📝 Step 2: Rendering HTML Template...")
        if not TEMPLATE_DIR.exists():
             raise FileNotFoundError(f"Templates folder missing at: {TEMPLATE_DIR}")

        # Create Jinja2 Environment
        env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
        template = env.get_template("report_template.html")
        
        # Inject data into template
        html_content = template.render(**data_context)

        # 4. Convert to PDF
        print("📄 Step 3: Generating PDF with WeasyPrint...")
        render_report(html_content, str(output_pdf_path))
        
        print("-" * 40)
        print(f"✅ Success! Report saved to:\n   {output_pdf_path}")

    except Exception as e:
        print("\n❌ Error detected:")
        print(f"   {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()