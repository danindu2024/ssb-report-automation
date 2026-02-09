# SSB Monthly Report Automation

Automated PDF report generation system for the Sri Lanka Social Security Board.
Converts Excel data into professional Sinhala-language reports using Python and WeasyPrint.

## Features
- **Sinhala Font Support:** Uses Noto Sans Sinhala via WeasyPrint.
- **Data Processing:** Extracts KPI metrics from Excel Master Sheets.
- **Dynamic Styling:** Jinja2 templating with Conditional Formatting (Red/Black logic).
- **Visualization:** Grid layouts for event photos and KPI cards.

## Setup
1. Install GTK3 Runtime (Windows) or Pango/Cairo (Linux).
2. Install dependencies:
   ```bash
   pip install -r requirements.txt