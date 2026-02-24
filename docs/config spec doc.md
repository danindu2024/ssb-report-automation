# **Configuration Specification Document**

**Version:** 1.0 **Date:** February 7, 2026 **Purpose:** Central configuration for SSB Report Automation System

## **1\. SYSTEM CONFIGURATION FILE**

**File:** /src/config.py

"""

SSB Report Automation - Configuration

All system settings, paths, and parameters

"""

import os

from pathlib import Path

\# ============================================================================

\# FILE PATHS

\# ============================================================================

\# Base directory (project root)

BASE_DIR = Path(\_\_file\_\_).parent.parent

\# Data directories

DATA_DIR = BASE_DIR / "data"

MASTER_EXCEL = DATA_DIR / "master_sheet.xlsx"

DIVISION_TEMPLATES_DIR = DATA_DIR / "division_templates"

\# Asset directories

ASSETS_DIR = BASE_DIR / "assets"

IMAGES_DIR = ASSETS_DIR / "images"

FONTS_DIR = ASSETS_DIR / "fonts"

\# Image subdirectories

EVENTS_RAW_DIR = IMAGES_DIR / "events" / "raw"

EVENTS_PROCESSED_DIR = IMAGES_DIR / "events" / "processed"

DIRECTORS_RAW_DIR = IMAGES_DIR / "directors" / "raw"

DIRECTORS_PROCESSED_DIR = IMAGES_DIR / "directors" / "processed"

SIGNATURES_DIR = IMAGES_DIR / "signatures"

\# Output directories

OUTPUT_DIR = BASE_DIR / "output"

PREVIEW_DIR = OUTPUT_DIR / "preview"

FINAL_DIR = OUTPUT_DIR / "final"

LOGS_DIR = OUTPUT_DIR / "logs"

CHARTS_DIR = OUTPUT_DIR / "charts"

PROOF_SHEETS_DIR = OUTPUT_DIR / "proof_sheets"

\# ============================================================================

\# EXCEL CONFIGURATION

\# ============================================================================

\# Division sheet mapping (Master Excel)

DIVISION_SHEETS = {

    1: "DIV_01_SCORECARDS",

    2: "DIV_02_DISTRICTS",

    3: "DIV_03_FINANCIALS",

    4: "DIV_04_BOARD",

    5: "DIV_05_EVENTS",

    6: "DIV_06_HR",

    7: "DIV_07_TRAINING",

    8: "DIV_08_PENSIONS",

    9: "DIV_09_IT",

    10: "DIV_10_AUDIT"

}

\# Division names (Sinhala)

DIVISION_NAMES_SI = {

    1: "සමාජ ආරක්ෂණ අංශය",

    2: "දිස්ත්‍රික් කාර්යාල",

    3: "මූල්‍ය අංශය",

    4: "පරිපාලන අංශය",

    5: "මහජන සම්බන්ධතා අංශය",

    6: "මානව සම්පත් අංශය",

    7: "පුහුණු ඒකකය",

    8: "විශ්‍රාම වැටුප් අංශය",

    9: "තොරතුරු තාක්ෂණ අංශය",

    10: "අභ්‍යන්තර විගණන අංශය"

}

\# Metadata cell locations (consistent across all templates)

METADATA_CELLS = {

    "division_code": "A1",

    "division_name": "B1",

    "report_month": "A2",

    "status": "B2",

    "last_updated": "A3",

    "officer": "B3"

}

\# Status values

VALID_STATUS_VALUES = \["DRAFT", "VALIDATED", "APPROVED"\]

\# ============================================================================

\# IMAGE PROCESSING CONFIGURATION

\# ============================================================================

\# Image dimension specifications

IMAGE_SPECS = {

    "event": {

        "width": 800,

        "height": 600,

        "aspect_ratio": 4/3,

        "quality": 85,

        "dpi": 300

    },

    "director": {

        "width": 400,

        "height": 400,

        "aspect_ratio": 1/1,

        "quality": 90,

        "dpi": 300

    },

    "signature": {

        "width": 300,

        "height": 100,

        "aspect_ratio": 3/1,

        "quality": 95,

        "format": "PNG"  # Preserve transparency

    }

}

\# Image validation rules

IMAGE_VALIDATION = {

    "min_width": 1024,

    "min_height": 768,

    "max_aspect_ratio": 2.5,

    "min_aspect_ratio": 0.4,

    "min_file_size_mb": 0.1,

    "max_file_size_mb": 20.0,

    "supported_formats": \[".jpg", ".jpeg", ".png", ".heic"\]

}

\# Photo naming convention

PHOTO_NAMING = {

    "event_folder_pattern": r"^\\d{4}-\\d{2}-\\d{2}\_\[A-Z0-9\\-\]{1,20}$",  # 2026-02-18_AWARDS-KUR

    "processed_photo_pattern": r"^\\d{2}\\.jpg$",  # 01.jpg, 02.jpg

    "director_photo_pattern": r"^DIRECTOR\_\[A-Z\]+\\.jpg$"  # DIRECTOR_DISSANAYAKE.jpg

}

\# ============================================================================

\# PDF GENERATION CONFIGURATION

\# ============================================================================

\# Page settings

PDF_PAGE_SIZE = "A4"  CSS: @page { size: A4; }

\# Note: WeasyPrint uses CSS for page setup, not Python constants

PDF_MARGINS = {

    "top": 2.54,     # cm

    "bottom": 2.54,

    "left": 2.54,

    "right": 2.54

}

\# Convert to points (1 cm = 28.35 points)

PDF_MARGINS_POINTS = {k: v \* 28.35 for k, v in PDF_MARGINS.items()}

\# Brand colors (SSB style guide)

BRAND_COLORS = {

    "deep_maroon": "#800000",      # Primary brand color

    "royal_navy": "#002366",       # Secondary brand color

    "official_gold": "#D4AF37",    # Accent color

    "light_grey": "#F8F9FA",       # Scorecard backgrounds

    "medium_grey": "#DEE2E6",      # Borders

    "success_green": "#198754",    # Positive metrics

    "info_blue": "#0D6EFD"         # Neutral metrics

}

\# Font configuration

FONTS = {

    "sinhala_regular": {

        "family_name": "Noto Sans Sinhala",  # CSS font-family

        "file": "NotoSansSinhala-Regular.ttf",

        "path": FONTS_DIR / "NotoSansSinhala-Regular.ttf",

        "weight": "normal",  # CSS font-weight

        "style": "normal"    # CSS font-style

    },

    "sinhala_bold": {

        "family_name": "Noto Sans Sinhala",

        "file": "NotoSansSinhala-Bold.ttf",

        "path": FONTS_DIR / "NotoSansSinhala-Bold.ttf",

        "weight": "bold",

        "style": "normal"

    }

}

\# Typography settings

FONT_SIZES = {

    "cover_title": 24,

    "section_heading": 18,

    "subsection_heading": 14,

    "body_text": 11,

    "caption": 9,

    "page_number": 10

}

\# Line spacing

LINE_SPACING = {

    "body": 14,      # 11pt font × 1.27 leading

    "heading": 22,   # 18pt font × 1.22 leading

    "tight": 12      # For tables

}

\# ============================================================================

\# CONTENT LIMITS

\# ============================================================================

\# Maximum content per section (prevent infinite pages)

CONTENT_LIMITS = {

    "events_per_month": 15,

    "event_title_chars": 100,

    "event_description_chars": 500,

    "director_bio_chars": 300,

    "chairman_message_chars": 2000,

    "district_table_rows": 25,  # Fixed (all districts)

    "photos_per_event": 5

}

\# ============================================================================

\# VALIDATION RULES

\# ============================================================================

VALIDATION_RULES = {

    "DIV_01_SCORECARDS": {

        "required_columns": \["MONTH", "RECRUITMENT_ACTUAL", "ANNUAL_COLLECTION", "FIRST_PREMIUM"\],

        "numeric_ranges": {

            "RECRUITMENT_ACTUAL": (0, 100000),

            "ANNUAL_COLLECTION": (0.0, 2000.0),

            "FIRST_PREMIUM": (0.0, 1000.0),

            "GROWTH_PCT": (-100.0, 500.0)

        },

        "date_format": r"^\\d{4}-\\d{2}$"  # YYYY-MM

    },

    "DIV_02_DISTRICTS": {

        "required_rows": 25,

        "district_names": \[

            "නුවරඑළිය", "කුරුණෑගල", "යාපනය", "අනුරාධපුරය", "මඩකලපුව",

            "මහනුවර", "බදුල්ල", "කෑගල්ල", "ත්‍රිකුණාමලය", "පුත්තලම",

            "මාතර", "ගාල්ල", "වව්නියාව", "කිලිනොච්චිය", "මොනරාගල",

            "රත්නපුර", "මන්නාරම", "කළුතර", "ගම්පහ", "හම්බන්තොට",

            "පොළොන්නරුව", "කොළඹ", "මාතලේ", "අම්පාර", "මුලතිව්"

        \],

        "numeric_ranges": {

            "monthly_count": (0, 50000)

        }

    },

    "DIV_03_FINANCIALS": {

        "required_columns": \["LINE_ITEM", "CATEGORY", "ANNUAL_TOTAL"\],

        "category_values": \["INCOME", "INCOME_SUB", "EXPENSE", "EXPENSE_SUB"\],

        "numeric_ranges": {

            "monthly_amounts": (0.0, 10000000000.0)  # Max 10 billion per line item

        }

    },

    "DIV_04_BOARD": {

        "required_rows": 7,  # 7 board members

        "required_columns": \["NAME_SINHALA", "POSITION", "BIO", "PHOTO_FILENAME"\],

        "character_limits": {

            "BIO": 300

        }

    },

    "DIV_05_EVENTS": {

        "max_rows": 15,

        "required_columns": \["EVENT_DATE", "EVENT_TITLE", "DESCRIPTION", "PHOTO_FOLDER"\],

        "character_limits": {

            "EVENT_TITLE": 100,

            "DESCRIPTION": 500

        },

        "date_format": r"^\\d{4}-\\d{2}-\\d{2}$",  # YYYY-MM-DD

        "photo_validation": True

    }

}

\# ============================================================================

\# CHART CONFIGURATION

\# ============================================================================

CHART_SETTINGS = {

    "default_dpi": 300,

    "default_format": "PNG",

    "figsize": (10, 6),  # inches

    "colors": {

        "primary": BRAND_COLORS\["deep_maroon"\],

        "secondary": BRAND_COLORS\["royal_navy"\],

        "accent": BRAND_COLORS\["official_gold"\]

    }

}

\# Chart-specific settings

CHART_TYPES = {

    "district_performance": {

        "type": "bar",

        "figsize": (12, 6),

        "color": BRAND_COLORS\["deep_maroon"\],

        "xlabel": "දිස්ත්‍රික්කය",

        "ylabel": "සාමාජිකයින්",

        "rotation": 45

    },

    "financial_trend": {

        "type": "line",

        "figsize": (10, 5),

        "color": BRAND_COLORS\["royal_navy"\],

        "marker": "o",

        "xlabel": "වර්ෂය",

        "ylabel": "එකතුව (මිලියන)"

    },

    "recruitment_growth": {

        "type": "bar",

        "figsize": (10, 5),

        "color": BRAND_COLORS\["info_blue"\],

        "xlabel": "මාසය",

        "ylabel": "බඳවා ගැනීම්"

    }

}

# 

\============================================================================

\# HTML_TEMPLATES configuration

\# ============================================================================

HTML_TEMPLATES = {

    "base": "base.html",

    "cover": "cover_page.html",

    "scorecards": "section_scorecards.html",

    "districts": "section_districts.html",

    "board": "section_board.html",

    "events": "section_events.html",

    "financials": "section_financials.html"

}

\============================================================================

\# GENERATION MODES

\# ============================================================================

GENERATION_MODES = {

    "preview": {

        "watermark": True,

        "watermark_css": """

            @page {

                background: url('data:image/svg+xml;utf8,DRAFT') center center no-repeat;

            }

        """,

        "include_validation_warnings": True,

        "save_html": True,  # NEW: Save HTML for debugging

        "output_dir": PREVIEW_DIR

    },

    "final": {

        "watermark": False,

        "include_validation_warnings": False,

        "save_html": False,

        "output_dir": FINAL_DIR,

        "embed_fonts": True

    }

}

\# ============================================================================

\# PERFORMANCE SETTINGS

\# ============================================================================

PERFORMANCE = {

    "image_processing_threads": 4,

    "chart_cache_enabled": True,

    "pdf_compression": True,

    "max_generation_time_seconds": 90,  # Increased for WeasyPrint

    "embed_images_as_base64": True,     # NEW: Faster than file refs

    "inline_css": True,                  # NEW: Faster than external CSS

    "optimize_fonts": True               # NEW: Subset fonts

}

\# ============================================================================

\# LOGGING CONFIGURATION

\# ============================================================================

LOGGING = {

    "level": "INFO",  # DEBUG, INFO, WARNING, ERROR

    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",

    "date_format": "%Y-%m-%d %H:%M:%S",

    "log_file": LOGS_DIR / "ssb_automation.log",

    "max_log_size_mb": 10,

    "backup_count": 5

}

\# ============================================================================

\# NOTIFICATION SETTINGS

\# ============================================================================

NOTIFICATIONS = {

    "email_enabled": False,  # Set to True when email configured

    "email_smtp_server": "smtp.example.com",

    "email_port": 587,

    "email_from": "ssb.automation@ssb.gov.lk",

    "coordinator_email": "coordinator@ssb.gov.lk"

}

\# ============================================================================

\# ERROR HANDLING

\# ============================================================================

ERROR_HANDLING = {

    "on_missing_data": "block",  # Options: "block", "warn", "use_placeholder"

    "on_missing_image": "placeholder",  # Options: "error", "placeholder", "skip"

    "placeholder_image": ASSETS_DIR / "placeholders" / "no-image.png",

    "strict_validation": True  # If True, any validation error blocks generation

}

\# ============================================================================

\# BACKUP CONFIGURATION

\# ============================================================================

BACKUP = {

    "enabled": True,

    "backup_dir": DATA_DIR / "backups",

    "retention_months": 6,

    "auto_backup_before_generation": True

}

\# ============================================================================

\# HELPER FUNCTIONS

\# ============================================================================

def get_division_name(division_number, language="si"):

    """Get division name by number"""

    if language == "si":

        return DIVISION_NAMES_SI.get(division_number, f"Division {division_number}")

    else:

        return f"Division {division_number}"

def get_sheet_name(division_number):

    """Get Excel sheet name for division"""

    return DIVISION_SHEETS.get(division_number)

def get_month_name_sinhala(month_number):

    """Convert month number to Sinhala name"""

    months = {

        1: "ජනවාරි", 2: "පෙබරවාරි", 3: "මාර්තු", 4: "අප්‍රේල්",

        5: "මැයි", 6: "ජූනි", 7: "ජූලි", 8: "අගෝස්තු",

        9: "සැප්තැම්බර්", 10: "ඔක්තෝබර්", 11: "නොවැම්බර්", 12: "දෙසැම්බර්"

    }

    return months.get(month_number, "")

def create_output_directories():

    """Create all necessary output directories if they don't exist"""

    directories = \[

        OUTPUT_DIR, PREVIEW_DIR, FINAL_DIR, LOGS_DIR, 

        CHARTS_DIR, PROOF_SHEETS_DIR,

        EVENTS_PROCESSED_DIR, DIRECTORS_PROCESSED_DIR

    \]

    for directory in directories:

        directory.mkdir(parents=True, exist_ok=True)

def validate_configuration():

    """Validate that all required files and directories exist"""

    errors = \[\]

    # Check master Excel exists

    if not MASTER_EXCEL.exists():

        errors.append(f"Master Excel not found: {MASTER_EXCEL}")

    # Check fonts exist

    for font_config in FONTS.values():

        if font_config\["file"\]:

            if not font_config\["path"\].exists():

                errors.append(f"Font file not found: {font_config\['path'\]}")

    # Check placeholder image exists

    if not ERROR_HANDLING\["placeholder_image"\].exists():

        errors.append(f"Placeholder image not found: {ERROR_HANDLING\['placeholder_image'\]}")

    return errors

\# ============================================================================

\# INITIALIZATION

\# ============================================================================

def initialize_system():

    """

    Initialize the system on first run

    Call this from main.py before any processing

    """

    # Create directories

    create_output_directories()

    # Validate configuration

    errors = validate_configuration()

    if errors:

        print("CONFIGURATION ERRORS:")

        for error in errors:

            print(f"  - {error}")

        return False

    print("✓ System configuration validated")

    return True

\# ============================================================================

\# EXPORT

\# ============================================================================

\_\_all\_\_ = \[

    'BASE_DIR', 'DATA_DIR', 'MASTER_EXCEL', 'OUTPUT_DIR',

    'DIVISION_SHEETS', 'DIVISION_NAMES_SI', 'IMAGE_SPECS',

    'BRAND_COLORS', 'FONTS', 'CONTENT_LIMITS', 'VALIDATION_RULES',

    'CHART_SETTINGS', 'GENERATION_MODES', 'LOGGING',

    'get_division_name', 'get_sheet_name', 'get_month_name_sinhala',

    'initialize_system'

\]

## **2\. ENVIRONMENT VARIABLES (Optional)**

**File:** .env (for sensitive configuration)

\# Email Configuration (if notifications enabled)

EMAIL_SMTP_SERVER=smtp.gmail.com

EMAIL_PORT=587

EMAIL_USERNAME=ssb.automation@ssb.gov.lk

EMAIL_PASSWORD=your_password_here

\# Database (if future integration needed)

DB_HOST=localhost

DB_PORT=5432

DB_NAME=ssb_reports

DB_USER=ssb_user

DB_PASSWORD=your_password_here

\# API Keys (if external services used)

CLOUD_STORAGE_API_KEY=your_api_key_here

**Loading environment variables:**

\# In main.py

from dotenv import load_dotenv

import os

load_dotenv()  # Load .env file

EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")

EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

## **3\. REQUIREMENTS FILE**

**File:** requirements.txt

\# Core PDF Generation (UPDATED)

weasyprint==61.0

cairocffi==1.6.1

tinycss2==1.2.1

cssselect2==0.7.0

\# Excel Processing

openpyxl==3.1.2

\# Image Processing

Pillow==10.1.0

pillow-heif==0.14.0

\# Charts

matplotlib==3.8.2

\# Templating

jinja2==3.1.2

\# Utilities

python-dateutil==2.8.2

## **4\. COMMAND-LINE INTERFACE**

**File:** /src/cli_config.py

"""

Command-line argument configuration

"""

import argparse

from datetime import datetime

def parse_arguments():

    """Parse command-line arguments"""

    parser = argparse.ArgumentParser(

        description="SSB Monthly Report Automation System",

        formatter_class=argparse.RawDescriptionHelpFormatter,

        epilog="""

Examples:

  # Generate preview for February 2026

  python main.py --month 2026-02 --mode preview

  # Generate final report

  python main.py --month 2026-02 --mode final

  # Validate data only (no PDF generation)

  python main.py --month 2026-02 --validate-only

  # Process images only

  python process_images.py --event 2026-02-18_AWARDS

        """

    )

    # Required arguments

    parser.add_argument(

        '--month',

        type=str,

        required=True,

        help='Report month in YYYY-MM format (e.g., 2026-02)'

    )

    # Optional arguments

    parser.add_argument(

        '--mode',

        type=str,

        choices=\['preview', 'final'\],

        default='preview',

        help='Generation mode (default: preview)'

    )

    parser.add_argument(

        '--validate-only',

        action='store_true',

        help='Run validation only, do not generate PDF'

    )

    parser.add_argument(

        '--skip-validation',

        action='store_true',

        help='Skip validation checks (not recommended)'

    )

    parser.add_argument(

        '--skip-images',

        action='store_true',

        help='Skip image processing (use existing processed images)'

    )

    parser.add_argument(

        '--output-dir',

        type=str,

        help='Custom output directory (overrides config)'

    )

    parser.add_argument(

        '--verbose',

        action='store_true',

        help='Enable verbose logging'

    )

    parser.add_argument(

        '--dry-run',

        action='store_true',

        help='Simulate generation without creating files'

    )

    args = parser.parse_args()

    # Validate month format

    try:

        datetime.strptime(args.month, "%Y-%m")

    except ValueError:

        parser.error("Month must be in YYYY-MM format (e.g., 2026-02)")

    return args

\# Image processing CLI

def parse_image_arguments():

    """Parse arguments for image processing script"""

    parser = argparse.ArgumentParser(

        description="SSB Image Processing Script"

    )

    parser.add_argument(

        '--event',

        type=str,

        help='Process specific event folder (e.g., 2026-02-18_AWARDS)'

    )

    parser.add_argument(

        '--batch',

        action='store_true',

        help='Process all events for a given month'

    )

    parser.add_argument(

        '--month',

        type=str,

        help='Month to process (required with --batch)'

    )

    parser.add_argument(

        '--type',

        type=str,

        choices=\['event', 'director', 'signature'\],

        default='event',

        help='Image type to process'

    )

    parser.add_argument(

        '--proof-sheet',

        action='store_true',

        help='Generate proof sheet PDF'

    )

    return parser.parse_args()

## **6\. CUSTOMIZATION GUIDE**

### **Changing Brand Colors**

**Edit:** config.py → BRAND_COLORS

BRAND_COLORS = {

    "deep_maroon": "#990000",  # Changed from #800000

    # ... rest unchanged

}

### **Adjusting Content Limits**

**Edit:** config.py → CONTENT_LIMITS

CONTENT_LIMITS = {

    "events_per_month": 20,  # Increased from 15

    "event_description_chars": 700,  # Increased from 500

}

### **Adding New Division**

**Edit:** config.py → DIVISION_SHEETS & DIVISION_NAMES_SI

DIVISION_SHEETS = {

    # ... existing divisions

    11: "DIV_11_LEGAL"  # New division

}

DIVISION_NAMES_SI = {

    # ... existing names

    11: "නීති අංශය"

}

**Document Version:** 1.0 **Last Updated:** February 7, 2026 **Configuration Schema:** v1.0
