"""
Data validation module for SSB Monthly Report Automation.
Applies validation rules from config.VALIDATION_RULES against loaded data.

Based on: DSD.md Section 4 and config spec doc.md VALIDATION_RULES
"""
import re
import os
from datetime import datetime
from pathlib import Path

from config import VALIDATION_RULES, LOGS_DIR, ASSETS_DIR


# Mapping from data_loader dict keys → sheet names used in VALIDATION_RULES
_DATA_KEY_TO_SHEET = {
    "scorecards":   "DIV_01_SCORECARDS",
    "districts":    "DIV_02_DISTRICTS",
    "financials":   "DIV_03_FINANCIALS",
    "board":        "DIV_04_BOARD",
    "events":       "DIV_05_EVENTS",
    "hr_stats":     "DIV_06_HR",
    "training":     "DIV_07_TRAINING",
    "pensions":     "DIV_08_PENSIONS",
    "it_projects":  "DIV_09_IT",
    "audit":        "DIV_10_AUDIT",
}


def _clean_number(value):
    """Safely coerce a cell value to float. Returns None if not parseable."""
    if value is None:
        return None
    try:
        return float(str(value).replace(',', '').strip())
    except (ValueError, TypeError):
        return None


def validate_data(data):
    """
    Validate all division data against VALIDATION_RULES from config.py.
    Returns a list of human-readable error strings.
    Warnings (non-blocking) are also collected separately.
    """
    errors = []
    warnings = []

    for data_key, sheet_name in _DATA_KEY_TO_SHEET.items():
        rows = data.get(data_key, [])
        rules = VALIDATION_RULES.get(sheet_name, {})

        if not rules:
            continue

        # ── 1. Required Columns ───────────────────────────────────────────────
        required_cols = rules.get("required_columns", [])
        if rows and required_cols:
            present_cols = set(rows[0].keys())
            for col in required_cols:
                if col not in present_cols:
                    errors.append(f"{sheet_name}: Missing required column '{col}'")

        # ── 2. Required Row Count (DIV_02_DISTRICTS only) ──────────────────────
        required_rows = rules.get("required_rows")
        if required_rows and len(rows) != required_rows:
            errors.append(
                f"{sheet_name}: Expected {required_rows} rows, found {len(rows)}"
            )

        # ── 3. Max Rows (DIV_05_EVENTS) ────────────────────────────────────────
        max_rows = rules.get("max_rows")
        if max_rows and len(rows) > max_rows:
            errors.append(
                f"{sheet_name}: Too many rows ({len(rows)} > max {max_rows})"
            )
        elif max_rows and len(rows) >= max_rows - 1:
            warnings.append(
                f"{sheet_name}: Row count ({len(rows)}) approaching limit ({max_rows})"
            )

        # ── 4. District Name Validation ────────────────────────────────────────
        expected_districts = rules.get("district_names")
        if expected_districts and rows:
            actual_districts = [r.get("DISTRICT") for r in rows if r.get("DISTRICT")]
            for expected in expected_districts:
                if expected not in actual_districts:
                    errors.append(f"{sheet_name}: Missing district '{expected}'")

        # ── 5. Numeric Range Checks ────────────────────────────────────────────
        numeric_ranges = rules.get("numeric_ranges", {})
        for col, (min_val, max_val) in numeric_ranges.items():
            for row_idx, row in enumerate(rows, start=5):
                raw_value = row.get(col)
                if raw_value is None:
                    continue
                value = _clean_number(raw_value)
                if value is None:
                    errors.append(
                        f"{sheet_name} Row {row_idx}: '{col}' value '{raw_value}' is not a number"
                    )
                elif not (min_val <= value <= max_val):
                    errors.append(
                        f"{sheet_name} Row {row_idx}: '{col}' = {value} out of range [{min_val}, {max_val}]"
                    )

        # ── 6. Character Limit Checks ──────────────────────────────────────────
        char_limits = rules.get("character_limits", {})
        for col, limit in char_limits.items():
            for row_idx, row in enumerate(rows, start=5):
                value = row.get(col)
                if value and len(str(value)) > limit:
                    errors.append(
                        f"{sheet_name} Row {row_idx}: '{col}' exceeds {limit} character limit "
                        f"({len(str(value))} chars)"
                    )

        # ── 7. Date Format ───────────────────────────────────────────────────
        date_pattern = rules.get("date_format")
        if date_pattern and date_pattern != "YYYY-MM":
            for row_idx, row in enumerate(rows, start=5):
                date_value = row.get("EVENT_DATE") or row.get("DATE") or row.get("MONTH")
                
                if isinstance(date_value, datetime):
                    date_str = date_value.strftime('%Y-%m-%d')
                else:
                    date_str = str(date_value) if date_value else ""
                    
                if date_value and not re.match(date_pattern, date_str):
                    errors.append(
                        f"{sheet_name} Row {row_idx}: Date '{date_value}' does not match required format"
                    )

        # ── 8. Photo Folder Existence (DIV_05_EVENTS) ─────────────────────────
        if rules.get("photo_validation"):
            raw_events_root = ASSETS_DIR / "images" / "events" / "raw"
            for row_idx, row in enumerate(rows, start=5):
                folder = row.get("PHOTO_FOLDER")
                if folder:
                    folder_path = raw_events_root / str(folder)
                    if not folder_path.exists():
                        errors.append(
                            f"{sheet_name} Row {row_idx}: Photo folder missing: '{folder}'"
                        )

    return errors, warnings


def write_validation_report(errors, warnings, month):
    """
    Write a structured validation report to /output/logs/validation_report_YYYY-MM.txt
    Returns the path to the written report.
    """
    report_path = LOGS_DIR / f"validation_report_{month}.txt"

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("SSB MONTHLY REPORT VALIDATION\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Month: {month}\n")
        f.write("=" * 80 + "\n\n")

        if errors:
            f.write("DATA VALIDATION ERRORS\n")
            f.write("=" * 80 + "\n")
            for error in errors:
                f.write(f"ERROR: {error}\n")
            f.write("\n")

        if warnings:
            f.write("WARNINGS\n")
            f.write("=" * 80 + "\n")
            for warning in warnings:
                f.write(f"WARNING: {warning}\n")
            f.write("\n")

        f.write("=" * 80 + "\n")
        total_errors = len(errors)
        total_warnings = len(warnings)
        f.write(f"Total Errors: {total_errors}\n")
        f.write(f"Total Warnings: {total_warnings}\n")

        if errors:
            f.write("Generation Status: BLOCKED (fix errors first)\n")
            f.write("\nNext Steps:\n")
            for i, error in enumerate(errors, 1):
                f.write(f"  {i}. {error}\n")
        else:
            f.write("Generation Status: READY\n")

    return report_path
