import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
ASSETS_DIR = BASE_DIR / "assets"
LOGS_DIR = OUTPUT_DIR / "logs"
CHARTS_DIR = OUTPUT_DIR / "charts"

# Core Files
MASTER_EXCEL_PATH = DATA_DIR / "Annual_Report_Master_V2_2026.xlsx"
FONTS_DIR = ASSETS_DIR / "fonts"

# System Initialization
def initialize_system():
    """Ensure all required directories exist"""
    directories = [
        DATA_DIR,
        OUTPUT_DIR / "preview",
        OUTPUT_DIR / "final",
        OUTPUT_DIR / "html",
        LOGS_DIR,
        CHARTS_DIR,
        ASSETS_DIR / "images" / "events",
        ASSETS_DIR / "images" / "directors",
        ASSETS_DIR / "images" / "signatures",
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
    
    return True

# Validation Rules
VALIDATION_RULES = {
    "DIV_01_SCORECARDS": {
        "required_columns": ["MONTH", "RECRUITMENT_ACTUAL", "ANNUAL_COLLECTION", "FIRST_PREMIUM"],
        "numeric_ranges": {
            "RECRUITMENT_ACTUAL": (0, 100000),
            "ANNUAL_COLLECTION": (0.0, 2000.0),
            "FIRST_PREMIUM": (0.0, 1000.0)
        },
        "date_format": "YYYY-MM"
    },
    "DIV_02_DISTRICTS": {
        "required_rows": 25,  
        "required_columns": ["DISTRICT", "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC", "TOTAL", "RANK"],
        "district_names": [
            "නුවරඑළිය", "කුරුණෑගල", "යාපනය", "අනුරාධපුරය", "මඩකලපුව",
            "මහනුවර", "බදුල්ල", "කෑගල්ල", "ත්‍රිකුණාමලය", "පුත්තලම",
            "මාතර", "ගාල්ල", "වව්නියාව", "කිලිනොච්චිය", "මොනරාගල",
            "රත්නපුර", "මන්නාරම", "කළුතර", "ගම්පහ", "හම්බන්තොට",
            "පොළොන්නරුව", "කොළඹ", "මාතලේ", "අම්පාර", "මුලතිව්"
        ],
        "numeric_ranges": {
            "JAN": (0, 50000),
            "FEB": (0, 50000),
            "MAR": (0, 50000),
            "APR": (0, 50000),
            "MAY": (0, 50000),
            "JUN": (0, 50000),
            "JUL": (0, 50000),
            "AUG": (0, 50000),
            "SEP": (0, 50000),
            "OCT": (0, 50000),
            "NOV": (0, 50000),
            "DEC": (0, 50000),
        }
    },
    "DIV_03_FINANCIALS": {
        "required_columns": ["LINE_ITEM", "CATEGORY", "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC", "ANNUAL_TOTAL"]
    },
    "DIV_04_BOARD": {
        "required_columns": ["NAME_SINHALA", "NAME_ENGLISH", "POSITION", "BIO", "PHOTO_FILENAME", "ORDER"],
        "character_limits": {"BIO": 300}
    },
    "DIV_05_EVENTS": {
        "max_rows": 15,
        "required_columns": ["EVENT_DATE", "EVENT_TITLE", "DESCRIPTION", "LOCATION", "PARTICIPANTS", "PHOTO_FOLDER"],
        "character_limits": {
            "DESCRIPTION": 500,
            "EVENT_TITLE": 100
        },
        "date_format": "^\\d{4}-\\d{2}-\\d{2}$",
        "photo_validation": True
    },
    "DIV_06_HR": {
        "required_columns": ["MONTH", "TOTAL_STAFF", "NEW_HIRES", "RESIGNATIONS", "PROMOTIONS", "TRAINING_HOURS"]
    },
    "DIV_07_TRAINING": {
        "required_columns": ["DATE", "PROGRAM_NAME", "PARTICIPANTS", "DURATION_DAYS", "LOCATION", "COST"]
    },
    "DIV_08_PENSIONS": {
        "required_columns": ["MONTH", "PENSIONERS_COUNT", "TOTAL_AMOUNT", "DEATH_BENEFITS", "PARTIAL_REFUNDS"]
    },
    "DIV_09_IT": {
        "required_columns": ["PROJECT_NAME", "STATUS", "START_DATE", "COMPLETION_PCT", "BUDGET", "DESCRIPTION"]
    },
    "DIV_10_AUDIT": {
        "required_columns": ["AUDIT_DATE", "DIVISION", "FINDING", "SEVERITY", "STATUS", "ACTION_PLAN"]
    }
}

# Image Processing Specs
IMAGE_SPECS = {
    "event": {"width": 800, "height": 600, "aspect_ratio": 4/3, "quality": 85, "dpi": 300},
    "director": {"width": 400, "height": 400, "aspect_ratio": 1/1, "quality": 90, "dpi": 300},
    "signature": {"width": 300, "height": 100, "aspect_ratio": 3/1, "quality": 95, "format": "PNG"}
}

FONTS = {
    "sinhala_regular": {"path": FONTS_DIR / "NotoSansSinhala-Regular.ttf"},
    "sinhala_bold": {"path": FONTS_DIR / "NotoSansSinhala-Bold.ttf"}
}
