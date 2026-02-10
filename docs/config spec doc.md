**Configuration Specification Document**
========================================

**Version:** 1.0 **Date:** February 7, 2026 **Purpose:** Central configuration for SSB Report Automation System

**1\. SYSTEM CONFIGURATION FILE**
---------------------------------

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

BASE\_DIR = Path(\_\_file\_\_).parent.parent

\# Data directories

DATA\_DIR = BASE\_DIR / "data"

MASTER\_EXCEL = DATA\_DIR / "master\_sheet.xlsx"

DIVISION\_TEMPLATES\_DIR = DATA\_DIR / "division\_templates"

\# Asset directories

ASSETS\_DIR = BASE\_DIR / "assets"

IMAGES\_DIR = ASSETS\_DIR / "images"

FONTS\_DIR = ASSETS\_DIR / "fonts"

\# Image subdirectories

EVENTS\_RAW\_DIR = IMAGES\_DIR / "events" / "raw"

EVENTS\_PROCESSED\_DIR = IMAGES\_DIR / "events" / "processed"

DIRECTORS\_RAW\_DIR = IMAGES\_DIR / "directors" / "raw"

DIRECTORS\_PROCESSED\_DIR = IMAGES\_DIR / "directors" / "processed"

SIGNATURES\_DIR = IMAGES\_DIR / "signatures"

\# Output directories

OUTPUT\_DIR = BASE\_DIR / "output"

PREVIEW\_DIR = OUTPUT\_DIR / "preview"

FINAL\_DIR = OUTPUT\_DIR / "final"

LOGS\_DIR = OUTPUT\_DIR / "logs"

CHARTS\_DIR = OUTPUT\_DIR / "charts"

PROOF\_SHEETS\_DIR = OUTPUT\_DIR / "proof\_sheets"

\# ============================================================================

\# EXCEL CONFIGURATION

\# ============================================================================

\# Division sheet mapping (Master Excel)

DIVISION\_SHEETS = {

    1: "DIV\_01\_SCORECARDS",

    2: "DIV\_02\_DISTRICTS",

    3: "DIV\_03\_FINANCIALS",

    4: "DIV\_04\_BOARD",

    5: "DIV\_05\_EVENTS",

    6: "DIV\_06\_HR",

    7: "DIV\_07\_TRAINING",

    8: "DIV\_08\_PENSIONS",

    9: "DIV\_09\_IT",

    10: "DIV\_10\_AUDIT"

}

\# Division names (Sinhala)

DIVISION\_NAMES\_SI = {

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

METADATA\_CELLS = {

    "division\_code": "A1",

    "division\_name": "B1",

    "report\_month": "A2",

    "status": "B2",

    "last\_updated": "A3",

    "officer": "B3"

}

\# Status values

VALID\_STATUS\_VALUES = \["DRAFT", "VALIDATED", "APPROVED"\]

\# ============================================================================

\# IMAGE PROCESSING CONFIGURATION

\# ============================================================================

\# Image dimension specifications

IMAGE\_SPECS = {

    "event": {

        "width": 800,

        "height": 600,

        "aspect\_ratio": 4/3,

        "quality": 85,

        "dpi": 300

    },

    "director": {

        "width": 400,

        "height": 400,

        "aspect\_ratio": 1/1,

        "quality": 90,

        "dpi": 300

    },

    "signature": {

        "width": 300,

        "height": 100,

        "aspect\_ratio": 3/1,

        "quality": 95,

        "format": "PNG"  # Preserve transparency

    }

}

\# Image validation rules

IMAGE\_VALIDATION = {

    "min\_width": 1024,

    "min\_height": 768,

    "max\_aspect\_ratio": 2.5,

    "min\_aspect\_ratio": 0.4,

    "min\_file\_size\_mb": 0.1,

    "max\_file\_size\_mb": 20.0,

    "supported\_formats": \[".jpg", ".jpeg", ".png", ".heic"\]

}

\# Photo naming convention

PHOTO\_NAMING = {

    "event\_folder\_pattern": r"^\\d{4}-\\d{2}-\\d{2}\_\[A-Z0-9\\-\]{1,20}$",  # 2026-02-18\_AWARDS-KUR

    "processed\_photo\_pattern": r"^\\d{2}\\.jpg$",  # 01.jpg, 02.jpg

    "director\_photo\_pattern": r"^DIRECTOR\_\[A-Z\]+\\.jpg$"  # DIRECTOR\_DISSANAYAKE.jpg

}

\# ============================================================================

\# PDF GENERATION CONFIGURATION

\# ============================================================================

\# Page settings

PDF\_PAGE\_SIZE = "A4"  CSS: @page { size: A4; }

\# Note: WeasyPrint uses CSS for page setup, not Python constants

PDF\_MARGINS = {

    "top": 2.54,     # cm

    "bottom": 2.54,

    "left": 2.54,

    "right": 2.54

}

\# Convert to points (1 cm = 28.35 points)

PDF\_MARGINS\_POINTS = {k: v \* 28.35 for k, v in PDF\_MARGINS.items()}

\# Brand colors (SSB style guide)

BRAND\_COLORS = {

    "deep\_maroon": "#800000",      # Primary brand color

    "royal\_navy": "#002366",       # Secondary brand color

    "official\_gold": "#D4AF37",    # Accent color

    "light\_grey": "#F8F9FA",       # Scorecard backgrounds

    "medium\_grey": "#DEE2E6",      # Borders

    "success\_green": "#198754",    # Positive metrics

    "info\_blue": "#0D6EFD"         # Neutral metrics

}

\# Font configuration

FONTS = {

    "sinhala\_regular": {

        "family\_name": "Noto Sans Sinhala",  # CSS font-family

        "file": "NotoSansSinhala-Regular.ttf",

        "path": FONTS\_DIR / "NotoSansSinhala-Regular.ttf",

        "weight": "normal",  # CSS font-weight

        "style": "normal"    # CSS font-style

    },

    "sinhala\_bold": {

        "family\_name": "Noto Sans Sinhala",

        "file": "NotoSansSinhala-Bold.ttf",

        "path": FONTS\_DIR / "NotoSansSinhala-Bold.ttf",

        "weight": "bold",

        "style": "normal"

    }

}

\# Typography settings

FONT\_SIZES = {

    "cover\_title": 24,

    "section\_heading": 18,

    "subsection\_heading": 14,

    "body\_text": 11,

    "caption": 9,

    "page\_number": 10

}

\# Line spacing

LINE\_SPACING = {

    "body": 14,      # 11pt font × 1.27 leading

    "heading": 22,   # 18pt font × 1.22 leading

    "tight": 12      # For tables

}

\# ============================================================================

\# CONTENT LIMITS

\# ============================================================================

\# Maximum content per section (prevent infinite pages)

CONTENT\_LIMITS = {

    "events\_per\_month": 15,

    "event\_title\_chars": 100,

    "event\_description\_chars": 500,

    "director\_bio\_chars": 300,

    "chairman\_message\_chars": 2000,

    "district\_table\_rows": 25,  # Fixed (all districts)

    "photos\_per\_event": 5

}

\# ============================================================================

\# VALIDATION RULES

\# ============================================================================

VALIDATION\_RULES = {

    "DIV\_01\_SCORECARDS": {

        "required\_columns": \["MONTH", "RECRUITMENT\_ACTUAL", "ANNUAL\_COLLECTION", "FIRST\_PREMIUM"\],

        "numeric\_ranges": {

            "RECRUITMENT\_ACTUAL": (0, 100000),

            "ANNUAL\_COLLECTION": (0.0, 2000.0),

            "FIRST\_PREMIUM": (0.0, 1000.0),

            "GROWTH\_PCT": (-100.0, 500.0)

        },

        "date\_format": r"^\\d{4}-\\d{2}$"  # YYYY-MM

    },

    "DIV\_02\_DISTRICTS": {

        "required\_rows": 25,

        "district\_names": \[

            "නුවරඑළිය", "කුරුණෑගල", "යාපනය", "අනුරාධපුරය", "මඩකලපුව",

            "මහනුවර", "බදුල්ල", "කෑගල්ල", "ත්‍රිකුණාමලය", "පුත්තලම",

            "මාතර", "ගාල්ල", "වව්නියාව", "කිලිනොච්චිය", "මොනරාගල",

            "රත්නපුර", "මේගමුව", "කළුතර", "ගම්පහ", "හම්බන්තොට",

            "පොළොන්නරුව", "කොළඹ", "මාතලේ", "අම්පාර", "මුලතිව්"

        \],

        "numeric\_ranges": {

            "monthly\_count": (0, 50000)

        }

    },

    "DIV\_03\_FINANCIALS": {

        "required\_columns": \["LINE\_ITEM", "CATEGORY", "ANNUAL\_TOTAL"\],

        "category\_values": \["INCOME", "INCOME\_SUB", "EXPENSE", "EXPENSE\_SUB"\],

        "numeric\_ranges": {

            "monthly\_amounts": (0.0, 10000000000.0)  # Max 10 billion per line item

        }

    },

    "DIV\_04\_BOARD": {

        "required\_rows": 7,  # 7 board members

        "required\_columns": \["NAME\_SINHALA", "POSITION", "BIO", "PHOTO\_FILENAME"\],

        "character\_limits": {

            "BIO": 300

        }

    },

    "DIV\_05\_EVENTS": {

        "max\_rows": 15,

        "required\_columns": \["EVENT\_DATE", "EVENT\_TITLE", "DESCRIPTION", "PHOTO\_FOLDER"\],

        "character\_limits": {

            "EVENT\_TITLE": 100,

            "DESCRIPTION": 500

        },

        "date\_format": r"^\\d{4}-\\d{2}-\\d{2}$",  # YYYY-MM-DD

        "photo\_validation": True

    }

}

\# ============================================================================

\# CHART CONFIGURATION

\# ============================================================================

CHART\_SETTINGS = {

    "default\_dpi": 300,

    "default\_format": "PNG",

    "figsize": (10, 6),  # inches

    "colors": {

        "primary": BRAND\_COLORS\["deep\_maroon"\],

        "secondary": BRAND\_COLORS\["royal\_navy"\],

        "accent": BRAND\_COLORS\["official\_gold"\]

    }

}

\# Chart-specific settings

CHART\_TYPES = {

    "district\_performance": {

        "type": "bar",

        "figsize": (12, 6),

        "color": BRAND\_COLORS\["deep\_maroon"\],

        "xlabel": "දිස්ත්‍රික්කය",

        "ylabel": "සාමාජිකයින්",

        "rotation": 45

    },

    "financial\_trend": {

        "type": "line",

        "figsize": (10, 5),

        "color": BRAND\_COLORS\["royal\_navy"\],

        "marker": "o",

        "xlabel": "වර්ෂය",

        "ylabel": "එකතුව (මිලියන)"

    },

    "recruitment\_growth": {

        "type": "bar",

        "figsize": (10, 5),

        "color": BRAND\_COLORS\["info\_blue"\],

        "xlabel": "මාසය",

        "ylabel": "බඳවා ගැනීම්"

    }

}

# 

\============================================================================

\# HTML\_TEMPLATES configuration

\# ============================================================================

HTML\_TEMPLATES = {

    "base": "base.html",

    "cover": "cover\_page.html",

    "scorecards": "section\_scorecards.html",

    "districts": "section\_districts.html",

    "board": "section\_board.html",

    "events": "section\_events.html",

    "financials": "section\_financials.html"

}

\============================================================================

\# GENERATION MODES

\# ============================================================================

GENERATION\_MODES = {

    "preview": {

        "watermark": True,

        "watermark\_css": """

            @page {

                background: url('data:image/svg+xml;utf8,DRAFT') center center no-repeat;

            }

        """,

        "include\_validation\_warnings": True,

        "save\_html": True,  # NEW: Save HTML for debugging

        "output\_dir": PREVIEW\_DIR

    },

    "final": {

        "watermark": False,

        "include\_validation\_warnings": False,

        "save\_html": False,

        "output\_dir": FINAL\_DIR,

        "embed\_fonts": True

    }

}

\# ============================================================================

\# PERFORMANCE SETTINGS

\# ============================================================================

PERFORMANCE = {

    "image\_processing\_threads": 4,

    "chart\_cache\_enabled": True,

    "pdf\_compression": True,

    "max\_generation\_time\_seconds": 90,  # Increased for WeasyPrint

    "embed\_images\_as\_base64": True,     # NEW: Faster than file refs

    "inline\_css": True,                  # NEW: Faster than external CSS

    "optimize\_fonts": True               # NEW: Subset fonts

}

\# ============================================================================

\# LOGGING CONFIGURATION

\# ============================================================================

LOGGING = {

    "level": "INFO",  # DEBUG, INFO, WARNING, ERROR

    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",

    "date\_format": "%Y-%m-%d %H:%M:%S",

    "log\_file": LOGS\_DIR / "ssb\_automation.log",

    "max\_log\_size\_mb": 10,

    "backup\_count": 5

}

\# ============================================================================

\# NOTIFICATION SETTINGS

\# ============================================================================

NOTIFICATIONS = {

    "email\_enabled": False,  # Set to True when email configured

    "email\_smtp\_server": "smtp.example.com",

    "email\_port": 587,

    "email\_from": "ssb.automation@ssb.gov.lk",

    "coordinator\_email": "coordinator@ssb.gov.lk"

}

\# ============================================================================

\# ERROR HANDLING

\# ============================================================================

ERROR\_HANDLING = {

    "on\_missing\_data": "block",  # Options: "block", "warn", "use\_placeholder"

    "on\_missing\_image": "placeholder",  # Options: "error", "placeholder", "skip"

    "placeholder\_image": ASSETS\_DIR / "placeholders" / "no-image.png",

    "strict\_validation": True  # If True, any validation error blocks generation

}

\# ============================================================================

\# BACKUP CONFIGURATION

\# ============================================================================

BACKUP = {

    "enabled": True,

    "backup\_dir": DATA\_DIR / "backups",

    "retention\_months": 6,

    "auto\_backup\_before\_generation": True

}

\# ============================================================================

\# HELPER FUNCTIONS

\# ============================================================================

def get\_division\_name(division\_number, language="si"):

    """Get division name by number"""

    if language == "si":

        return DIVISION\_NAMES\_SI.get(division\_number, f"Division {division\_number}")

    else:

        return f"Division {division\_number}"

def get\_sheet\_name(division\_number):

    """Get Excel sheet name for division"""

    return DIVISION\_SHEETS.get(division\_number)

def get\_month\_name\_sinhala(month\_number):

    """Convert month number to Sinhala name"""

    months = {

        1: "ජනවාරි", 2: "පෙබරවාරි", 3: "මාර්තු", 4: "අප්‍රේල්",

        5: "මැයි", 6: "ජූනි", 7: "ජූලි", 8: "අගෝස්තු",

        9: "සැප්තැම්බර්", 10: "ඔක්තෝබර්", 11: "නොවැම්බර්", 12: "දෙසැම්බර්"

    }

    return months.get(month\_number, "")

def create\_output\_directories():

    """Create all necessary output directories if they don't exist"""

    directories = \[

        OUTPUT\_DIR, PREVIEW\_DIR, FINAL\_DIR, LOGS\_DIR, 

        CHARTS\_DIR, PROOF\_SHEETS\_DIR,

        EVENTS\_PROCESSED\_DIR, DIRECTORS\_PROCESSED\_DIR

    \]

    for directory in directories:

        directory.mkdir(parents=True, exist\_ok=True)

def validate\_configuration():

    """Validate that all required files and directories exist"""

    errors = \[\]

    # Check master Excel exists

    if not MASTER\_EXCEL.exists():

        errors.append(f"Master Excel not found: {MASTER\_EXCEL}")

    # Check fonts exist

    for font\_config in FONTS.values():

        if font\_config\["file"\]:

            if not font\_config\["path"\].exists():

                errors.append(f"Font file not found: {font\_config\['path'\]}")

    # Check placeholder image exists

    if not ERROR\_HANDLING\["placeholder\_image"\].exists():

        errors.append(f"Placeholder image not found: {ERROR\_HANDLING\['placeholder\_image'\]}")

    return errors

\# ============================================================================

\# INITIALIZATION

\# ============================================================================

def initialize\_system():

    """

    Initialize the system on first run

    Call this from main.py before any processing

    """

    # Create directories

    create\_output\_directories()

    # Validate configuration

    errors = validate\_configuration()

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

    'BASE\_DIR', 'DATA\_DIR', 'MASTER\_EXCEL', 'OUTPUT\_DIR',

    'DIVISION\_SHEETS', 'DIVISION\_NAMES\_SI', 'IMAGE\_SPECS',

    'BRAND\_COLORS', 'FONTS', 'CONTENT\_LIMITS', 'VALIDATION\_RULES',

    'CHART\_SETTINGS', 'GENERATION\_MODES', 'LOGGING',

    'get\_division\_name', 'get\_sheet\_name', 'get\_month\_name\_sinhala',

    'initialize\_system'

\]

**2\. ENVIRONMENT VARIABLES (Optional)**
----------------------------------------

**File:** .env (for sensitive configuration)

\# Email Configuration (if notifications enabled)

EMAIL\_SMTP\_SERVER=smtp.gmail.com

EMAIL\_PORT=587

EMAIL\_USERNAME=ssb.automation@ssb.gov.lk

EMAIL\_PASSWORD=your\_password\_here

\# Database (if future integration needed)

DB\_HOST=localhost

DB\_PORT=5432

DB\_NAME=ssb\_reports

DB\_USER=ssb\_user

DB\_PASSWORD=your\_password\_here

\# API Keys (if external services used)

CLOUD\_STORAGE\_API\_KEY=your\_api\_key\_here

**Loading environment variables:**

\# In main.py

from dotenv import load\_dotenv

import os

load\_dotenv()  # Load .env file

EMAIL\_USERNAME = os.getenv("EMAIL\_USERNAME")

EMAIL\_PASSWORD = os.getenv("EMAIL\_PASSWORD")

**3\. REQUIREMENTS FILE**
-------------------------

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

**4\. COMMAND-LINE INTERFACE**
------------------------------

**File:** /src/cli\_config.py

"""

Command-line argument configuration

"""

import argparse

from datetime import datetime

def parse\_arguments():

    """Parse command-line arguments"""

    parser = argparse.ArgumentParser(

        description="SSB Monthly Report Automation System",

        formatter\_class=argparse.RawDescriptionHelpFormatter,

        epilog="""

Examples:

  # Generate preview for February 2026

  python main.py --month 2026-02 --mode preview

  # Generate final report

  python main.py --month 2026-02 --mode final

  # Validate data only (no PDF generation)

  python main.py --month 2026-02 --validate-only

  # Process images only

  python process\_images.py --event 2026-02-18\_AWARDS

        """

    )

    # Required arguments

    parser.add\_argument(

        '--month',

        type=str,

        required=True,

        help='Report month in YYYY-MM format (e.g., 2026-02)'

    )

    # Optional arguments

    parser.add\_argument(

        '--mode',

        type=str,

        choices=\['preview', 'final'\],

        default='preview',

        help='Generation mode (default: preview)'

    )

    parser.add\_argument(

        '--validate-only',

        action='store\_true',

        help='Run validation only, do not generate PDF'

    )

    parser.add\_argument(

        '--skip-validation',

        action='store\_true',

        help='Skip validation checks (not recommended)'

    )

    parser.add\_argument(

        '--skip-images',

        action='store\_true',

        help='Skip image processing (use existing processed images)'

    )

    parser.add\_argument(

        '--output-dir',

        type=str,

        help='Custom output directory (overrides config)'

    )

    parser.add\_argument(

        '--verbose',

        action='store\_true',

        help='Enable verbose logging'

    )

    parser.add\_argument(

        '--dry-run',

        action='store\_true',

        help='Simulate generation without creating files'

    )

    args = parser.parse\_args()

    # Validate month format

    try:

        datetime.strptime(args.month, "%Y-%m")

    except ValueError:

        parser.error("Month must be in YYYY-MM format (e.g., 2026-02)")

    return args

\# Image processing CLI

def parse\_image\_arguments():

    """Parse arguments for image processing script"""

    parser = argparse.ArgumentParser(

        description="SSB Image Processing Script"

    )

    parser.add\_argument(

        '--event',

        type=str,

        help='Process specific event folder (e.g., 2026-02-18\_AWARDS)'

    )

    parser.add\_argument(

        '--batch',

        action='store\_true',

        help='Process all events for a given month'

    )

    parser.add\_argument(

        '--month',

        type=str,

        help='Month to process (required with --batch)'

    )

    parser.add\_argument(

        '--type',

        type=str,

        choices=\['event', 'director', 'signature'\],

        default='event',

        help='Image type to process'

    )

    parser.add\_argument(

        '--proof-sheet',

        action='store\_true',

        help='Generate proof sheet PDF'

    )

    return parser.parse\_args()

**6\. CUSTOMIZATION GUIDE**
---------------------------

### **Changing Brand Colors**

**Edit:** config.py → BRAND\_COLORS

BRAND\_COLORS = {

    "deep\_maroon": "#990000",  # Changed from #800000

    # ... rest unchanged

}

### **Adjusting Content Limits**

**Edit:** config.py → CONTENT\_LIMITS

CONTENT\_LIMITS = {

    "events\_per\_month": 20,  # Increased from 15

    "event\_description\_chars": 700,  # Increased from 500

}

### **Adding New Division**

**Edit:** config.py → DIVISION\_SHEETS & DIVISION\_NAMES\_SI

DIVISION\_SHEETS = {

    # ... existing divisions

    11: "DIV\_11\_LEGAL"  # New division

}

DIVISION\_NAMES\_SI = {

    # ... existing names

    11: "නීති අංශය"

}

**Document Version:** 1.0 **Last Updated:** February 7, 2026 **Configuration Schema:** v1.0