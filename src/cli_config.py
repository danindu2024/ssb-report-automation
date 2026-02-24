import argparse
from datetime import datetime

def parse_arguments():
    """
    Parse command-line arguments for the report generator.
    """
    parser = argparse.ArgumentParser(description="SSB Monthly Report Generator (WeasyPrint)")
    
    # Required/Primary Arguments
    parser.add_argument(
        '--month',
        type=str,
        default=datetime.now().strftime("%Y-%m"),
        help='Report month in YYYY-MM format (e.g., 2026-02)'
    )
    
    parser.add_argument(
        '--mode',
        type=str,
        choices=['preview', 'final'],
        default='preview',
        help="Generate draft preview (with watermark) or final print-ready PDF"
    )

    # Optional Overrides
    parser.add_argument(
        '--input', 
        type=str, 
        default='Annual_Report_Master_2026.xlsx',
        help='Name of the input master Excel file in the data/ directory'
    )
    
    # Development/Debugging Flags
    parser.add_argument(
        '--skip-validation',
        action='store_true',
        help='Skip strict data validation rules (use for debugging only)'
    )
    
    parser.add_argument(
        '--skip-images',
        action='store_true',
        help='Skip processing new images (use if images are already processed)'
    )
    
    parser.add_argument(
        '--validate-only',
        action='store_true',
        help='Run validation rules and exit without generating PDF'
    )

    return parser.parse_args()
