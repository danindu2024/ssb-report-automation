import openpyxl
from pathlib import Path

def load_master_sheet(month, filepath):
    """
    Extract all division data from master Excel using the 10 sheets structure.
    Returns a unified dictionary mapping sheet names to list of dictionaries for each row.
    """
    excel_path = Path(filepath)
    if not excel_path.exists():
        raise FileNotFoundError(f"Excel file not found: {excel_path}")

    print(f"Loading data from: {excel_path.name}...")
    wb = openpyxl.load_workbook(excel_path, data_only=True)
    
    data = {
        "report_month": month,
        "scorecards": _extract_sheet(wb, "DIV_01_SCORECARDS", min_row=5),
        "districts": _extract_sheet(wb, "DIV_02_DISTRICTS", min_row=5),
        "financials": _extract_sheet(wb, "DIV_03_FINANCIALS", min_row=5),
        "board": _extract_sheet(wb, "DIV_04_BOARD", min_row=5),
        "events": _extract_sheet(wb, "DIV_05_EVENTS", min_row=5),
        "hr_stats": _extract_sheet(wb, "DIV_06_HR", min_row=5),
        "training": _extract_sheet(wb, "DIV_07_TRAINING", min_row=5),
        "pensions": _extract_sheet(wb, "DIV_08_PENSIONS", min_row=5),
        "it_projects": _extract_sheet(wb, "DIV_09_IT", min_row=5),
        "audit": _extract_sheet(wb, "DIV_10_AUDIT", min_row=5)
    }

    print("✓ Data successfully loaded.")
    return data

def _extract_sheet(wb, sheet_name, min_row):
    """
    Generic extractor: Reads the sheet (if exists).
    Row 4 is assumed to be the header based on DSD.md.
    """
    if sheet_name not in wb.sheetnames:
        print(f"⚠️ Warning: Sheet '{sheet_name}' not found.")
        return []

    sheet = wb[sheet_name]
    
    # 1. Read headers from Row 4 (0-indexed -> 3)
    header_row = [str(cell.value).strip() if cell.value else f"COL_{idx}" 
                  for idx, cell in enumerate(sheet[4], start=1)]
    
    # 2. Extract Data
    rows = []
    for row in sheet.iter_rows(min_row=min_row, values_only=True):
        # Skip if row is completely empty or the first cell is missing (which usually defines the row)
        if not any(row) or row[0] is None:
            continue
            
        row_dict = {}
        for col_idx, value in enumerate(row):
            if col_idx < len(header_row):
                key = header_row[col_idx]
                row_dict[key] = value
                
        rows.append(row_dict)
        
    return rows