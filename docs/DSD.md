# **Data Specification Document: Excel Templates & Master Sheet**

**Version:** 1.0 **Date:** February 7, 2026 **Purpose:** Define exact Excel structure for all 10 divisions

## **1\. MASTER EXCEL STRUCTURE**

### **1.1 File Details**

- **Filename:** SSB_Master_Report_2026.xlsx

- **Location:** /data/master_sheet.xlsx

- **Access:** Read-only for divisions; Edit access for Coordinator only

- **Update Mechanism:** Linked formulas from division templates (auto-refresh)

### **1.2 Sheet Organization**

**Sheet Name**

**Source Division**

**Data Type**

**Rows**

**Columns**

DIV_01_SCORECARDS

Social Security Dept

Metrics

12 (months)

15

DIV_02_DISTRICTS

District Offices

Performance

25 (districts) × 12 (months)

15

DIV_03_FINANCIALS

Finance Dept

Accounting

50 (line items)

14

DIV_04_BOARD

Admin/HR

Personnel

7 (directors)

6

DIV_05_EVENTS

Public Relations

Activities

Variable (max 15/month)

7

DIV_06_HR

Human Resources

Staff data

12 (months)

10

DIV_07_TRAINING

Training Unit

Programs

Variable (max 20/month)

9

DIV_08_PENSIONS

Pension Dept

Disbursement

12 (months)

12

DIV_09_IT

IT Department

Tech initiatives

Variable

8

DIV_10_AUDIT

Internal Audit

Findings

Variable

10

## **2\. DIVISION TEMPLATE SPECIFICATIONS**

### **2.1 General Rules (Apply to ALL Templates)**

**Mandatory Metadata Cells:**

Cell A1: Division Code (e.g., "DIV_01")

Cell B1: Division Name (Sinhala, e.g., "සමාජ ආරක්ෂණ අංශය")

Cell A2: Report Month (format: "2026-02")

Cell B2: Status (dropdown: "DRAFT" | "VALIDATED" | "APPROVED")

Cell A3: Last Updated (auto-timestamp formula: =NOW())

Cell B3: Responsible Officer Name

**Data Validation:**

- All numeric cells: Data > Validation > Decimal, Min=0

- Date cells: Data > Validation > Date, Format=YYYY-MM-DD

- Status cell: Data > Validation > List = {DRAFT, VALIDATED, APPROVED}

**Formatting:**

- Header row: Bold, Background #002366 (Navy), Font white

- Number format: #,##0 (thousands separator, no decimals for counts)

- Currency format: #,##0.00 (two decimals for financial values)

- Date format: YYYY-MM-DD (ISO 8601)

## **2.2 TEMPLATE 1: Scorecards (Division 01)**

**Filename:** DIV_01_Scorecards_Template.xlsx

**Sheet Name:** MONTHLY_METRICS

**Structure:**

**Row**

**Column A**

**Column B**

**Column C**

**Column D**

**...**

**Column O**

1

DIV_CODE

DIV_NAME

\-

\-

\-

\-

2

MONTH

STATUS

LAST_UPDATED

OFFICER

\-

\-

3

\-

\-

\-

\-

\-

\-

4

**MONTH**

**RECRUITMENT_TARGET**

**RECRUITMENT_ACTUAL**

**GROWTH_PCT**

**ANNUAL_COLLECTION**

**FIRST_PREMIUM**

5

2026-01

70000

66977

4.5

260.60

318.69

6

2026-02

\[formula\]

\[input\]

\[formula\]

\[input\]

\[input\]

...

...

...

...

...

...

...

15

2026-12

\[formula\]

\[input\]

\[formula\]

\[input\]

\[input\]

16

**TOTAL**

\[=SUM(B5:B15)\]

\[=SUM(C5:C15)\]

\[=AVG(D5:D15)\]

\[=SUM(E5:E15)\]

\[=SUM(F5:F15)\]

**Column Definitions:**

**Column**

**Name**

**Type**

**Formula/Validation**

**Description**

A

MONTH

Date

Format: YYYY-MM

Reporting month

B

RECRUITMENT_TARGET

Integer

Validation: ≥0, ≤100000

Monthly target (from annual plan)

C

RECRUITMENT_ACTUAL

Integer

**USER INPUT**

Actual new members recruited

D

GROWTH_PCT

Decimal

\=(C-B)/B\*100

% growth (actual vs target)

E

ANNUAL_COLLECTION

Decimal

**USER INPUT**

Total collections (million LKR)

F

FIRST_PREMIUM

Decimal

**USER INPUT**

First premium income (million LKR)

**Master Sheet Link:**

\# In Master Sheet (DIV_01_SCORECARDS)

Cell B5: ='\[DIV_01_Scorecards_Template.xlsx\]MONTHLY_METRICS'!$C$5

Cell E5: ='\[DIV_01_Scorecards_Template.xlsx\]MONTHLY_METRICS'!$E$5

\# ... (repeat for all months and metrics)

## **2.3 TEMPLATE 2: District Performance (Division 02)**

**Filename:** DIV_02_Districts_Template.xlsx

**Sheet Name:** DISTRICT_MONTHLY

**Structure:**

**Row**

**A**

**B**

**C**

**D**

**E**

**F**

**G**

**H**

4

**DISTRICT**

**JAN**

**FEB**

**MAR**

...

**DEC**

**TOTAL**

**RANK**

5

නුවරඑළිය

10437

\[input\]

\[input\]

...

\[input\]

\[=SUM(B5:M5)\]

\[=RANK(N5,$N$5:$N$29)\]

6

කුරුණෑගල

7346

\[input\]

\[input\]

...

\[input\]

\[formula\]

\[formula\]

...

...

...

...

...

...

...

...

...

29

කෑගල්ල

1850

\[input\]

\[input\]

...

\[input\]

\[formula\]

\[formula\]

**Critical Features:**

1.  **Auto-Ranking:** RANK formula updates automatically when data changes

2.  **Conditional Formatting:**
    - Top 5 districts: Green background

    - Bottom 5 districts: Yellow background

3.  **Data Validation:** Each cell (B5:M29) must be integer ≥0

**Master Sheet Link:**

\# Master pulls entire table range

\='\[DIV_02_Districts_Template.xlsx\]DISTRICT_MONTHLY'!$A$5:$H$29

## **2.4 TEMPLATE 3: Financial Data (Division 03)**

**Filename:** DIV_03_Financials_Template.xlsx

**Sheet Name:** INCOME_STATEMENT

**Structure:**

**Row**

**A**

**B**

**C**

**D**

**...**

**N**

4

**LINE_ITEM**

**CATEGORY**

**JAN**

**FEB**

...

**ANNUAL_TOTAL**

5

සාමාජික දායකත්ව

INCOME

\[input\]

\[input\]

...

\[=SUM(C5:M5)\]

6

\- තැපැල් කාර්යාල

INCOME_SUB

187147374

\[input\]

...

\[formula\]

7

\- බැංකු හා වෙනත්

INCOME_SUB

747560665

\[input\]

...

\[formula\]

...

...

...

...

...

...

...

25

විශ්‍රාම වැටුප් ගෙවීම්

EXPENSE

\[input\]

\[input\]

...

\[formula\]

...

...

...

...

...

...

...

**Validation Rules:**

- CATEGORY values: {INCOME, INCOME_SUB, EXPENSE, EXPENSE_SUB}

- All numeric cells: Decimal, ≥0

- SUB-categories must indent (use CONCATENATE(" - ", text))

**Auto-Calculations:**

\# Row 50: Total Income

\=SUMIF($B$5:$B$49, "INCOME", $N$5:$N$49)

\# Row 51: Total Expenses

\=SUMIF($B$5:$B$49, "EXPENSE", $N$5:$N$49)

\# Row 52: Net Surplus

\=N50-N51

## **2.5 TEMPLATE 4: Board of Directors (Division 04)**

**Filename:** DIV_04_Board_Template.xlsx

**Sheet Name:** DIRECTORS

**Structure:**

**A**

**B**

**C**

**D**

**E**

**F**

**NAME_SINHALA**

**NAME_ENGLISH**

**POSITION**

**BIO**

**PHOTO_FILENAME**

**ORDER**

එම්.කේ.බී.දිසානායක මහතා

M.K.B. Dissanayake

සභාපති

\[300 char max\]

DIRECTOR_DISSANAYAKE.jpg

1

...

...

අධ්‍යක්ෂ මණ්ඩල සාමාජික

\[300 char max\]

DIRECTOR_XXX.jpg

2

**Validation:**

- BIO: =LEN(D5)<=300 (character limit)

- PHOTO_FILENAME: Must exist in /assets/images/directors/

- ORDER: Unique integers 1-7 (for display sequence)

**Photo File Naming:**

Format: DIRECTOR\_\[LASTNAME\].jpg

Examples:

\- DIRECTOR_DISSANAYAKE.jpg

\- DIRECTOR_HERATH.jpg

## **2.6 TEMPLATE 5: Events (Division 05) - CRITICAL**

**Filename:** DIV_05_Events_Template.xlsx

**Sheet Name:** MONTHLY_EVENTS

**Structure:**

**A**

**B**

**C**

**D**

**E**

**F**

**G**

**EVENT_DATE**

**EVENT_TITLE**

**DESCRIPTION**

**LOCATION**

**PARTICIPANTS**

**PHOTO_FOLDER**

**PHOTO_COUNT**

2026-01-28

අමාත්‍යවරයා සමග සාකච්ඡාව

\[500 char max\]

අමාත්‍යාංශ පරිශ්‍රය

25

2026-01-28_MINISTER

[auto-counted]3

2026-02-18

සම්මාන උළෙල - කුරුණෑගල

\[500 char max\]

කුරුණෑගල දිස්ත්‍රික් කාර්යාලය

50

2026-02-18_AWARDS-KUR

[auto-counted]

**Critical Rules:**

1.  **Max 15 events per month** (validation: row count ≤15)

2.  **EVENT_DATE:** Must be within current reporting month

3.  **DESCRIPTION:** Character limit enforced: =LEN(C5)<=500

4.  **PHOTO_FOLDER:** Naming convention enforced

**Photo Management:**

Directory structure:

/assets/images/events/

├── 2026-01-28_MINISTER/

│   ├── 01.jpg  (auto-numbered)

│   ├── 02.jpg

│   └── 03.jpg

├── 2026-02-18_AWARDS-KUR/

│   ├── 01.jpg

│   ├── 02.jpg

│   ├── 03.jpg

│   ├── 04.jpg

│   └── 05.jpg

**Python Auto-Detection:**

\# Script automatically finds all photos in folder

photo_folder = "2026-01-28_MINISTER"

photo_paths = glob.glob(f"assets/images/events/{photo_folder}/\*.jpg")

\# Returns: \[01.jpg, 02.jpg, 03.jpg\]

## **2.7 TEMPLATES 6-10: Simplified Specifications**

### **Template 6: HR Statistics (Division 06)**

**Columns:** MONTH | TOTAL_STAFF | NEW_HIRES | RESIGNATIONS | PROMOTIONS | TRAINING_HOURS

### **Template 7: Training Programs (Division 07)**

**Columns:** DATE | PROGRAM_NAME | PARTICIPANTS | DURATION_DAYS | LOCATION | COST

### **Template 8: Pension Disbursement (Division 08)**

**Columns:** MONTH | PENSIONERS_COUNT | TOTAL_AMOUNT | DEATH_BENEFITS | PARTIAL_REFUNDS

### **Template 9: IT Initiatives (Division 09)**

**Columns:** PROJECT_NAME | STATUS | START_DATE | COMPLETION_PCT | BUDGET | DESCRIPTION

### **Template 10: Audit Findings (Division 10)**

**Columns:** AUDIT_DATE | DIVISION | FINDING | SEVERITY | STATUS | ACTION_PLAN

## **3\. DATA LINKING MECHANISM (Master ← Templates)**

### **3.1 Automatic Update Formula**

**In Master Sheet (DIV_01_SCORECARDS tab):**

\# Cell mapping example

Cell C8 (Feb Recruitment): ='C:\\SSB\\data\\division_templates\\\[DIV_01_Scorecards_Template.xlsx\]MONTHLY_METRICS'!$C$6

\# Advantages:

\- Auto-updates when division file saved

\- Coordinator sees real-time data in Master

\- No manual copy-paste errors

### **3.2 Refresh Protocol**

**Division Workflow:**

1.  Open division template

2.  Update monthly data

3.  Save file (File > Save)

4.  Send email to coordinator: "Division X data updated for Month Y"

**Coordinator Workflow:**

1.  Open Master Excel

2.  Click **Data > Refresh All** (updates all linked formulas)

3.  Verify STATUS column shows "VALIDATED" for all divisions

4.  Run Python validation script

## **4\. DATA VALIDATION SCRIPT (Python)**

### **4.1 Validation Checks**

\# validation_rules.py

VALIDATION_RULES = {

    "DIV_01_SCORECARDS": {

        "required_columns": ["MONTH", "RECRUITMENT\_ACTUAL", "ANNUAL\_COLLECTION", "FIRST\_PREMIUM"],

        "numeric_ranges": {

            "RECRUITMENT_ACTUAL": (0, 100000),

            "ANNUAL_COLLECTION": (0.0, 2000.0),

            "FIRST_PREMIUM": (0.0, 1000.0)

        },

        "date_format": "YYYY-MM"

    },

    "DIV_02_DISTRICTS": {

        "required_rows": 25,  # Must have all 25 districts

        "district_names": \[

            "නුවරඑළිය", "කුරුණෑගල", "යාපනය", ...  # Full list

        \],

        "numeric_ranges": {

            "JAN": (0, 50000),

            "FEB": (0, 50000),

            # ... for all months

        }

    },

    "DIV_05_EVENTS": {

        "max_rows": 15,  # Max 15 events per month

        "required_columns": ["EVENT\_DATE", "EVENT\_TITLE", "PHOTO\_FOLDER", "DESCRIPTION"],

        "character_limits": {

            "DESCRIPTION": 500,

            "EVENT_TITLE": 100

        },

        "photo_validation": True  # Check if PHOTO_FOLDER exists

    }

}

\# Validation execution

def validate_master_sheet(master_file_path):

    wb = openpyxl.load_workbook(master_file_path)

    errors = \[\]

    for sheet_name, rules in VALIDATION_RULES.items():

        sheet = wb\[sheet_name\]

        # Check required columns exist

        header_row = \[cell.value for cell in sheet\[4\]\]

        for col in rules\["required_columns"\]:

            if col not in header_row:

                errors.append(f"{sheet_name}: Missing column {col}")

        # Check numeric ranges

        if "numeric_ranges" in rules:

            for col, (min_val, max_val) in rules\["numeric_ranges"\].items():

                col_idx = header_row.index(col)

                for row in sheet.iter_rows(min_row=5, max_row=sheet.max_row):

                    val = row\[col_idx\].value

                    if val and (val < min_val or val > max_val):

                        errors.append(f"{sheet_name} Row {row\[0\].row}: {col}={val} out of range \[{min_val}, {max_val}\]")

        # Check photo folders exist

        if rules.get("photo_validation"):

            photo_col_idx = header_row.index("PHOTO_FOLDER")

            for row in sheet.iter_rows(min_row=5, max_row=sheet.max_row):

                folder = row\[photo_col_idx\].value

                if folder and not os.path.exists(f"assets/images/events/{folder}"):

                    errors.append(f"{sheet_name} Row {row\[0\].row}: Photo folder missing: {folder}")

    return errors

### **4.2 Validation Report Output**

**File:** /output/logs/validation_report_2026-02.txt

SSB MONTHLY REPORT VALIDATION

Generated: 2026-03-01 09:15:23

Month: February 2026

\================================================================================

DIVISION STATUS CHECK

\================================================================================

✓ DIV_01_SCORECARDS: VALIDATED (Last updated: 2026-02-28 16:30)

✓ DIV_02_DISTRICTS: VALIDATED (Last updated: 2026-02-28 14:20)

✗ DIV_03_FINANCIALS: DRAFT (Last updated: 2026-02-25 10:15) ← ACTION REQUIRED

✓ DIV_04_BOARD: APPROVED (Last updated: 2026-01-15 11:00)

✗ DIV_05_EVENTS: VALIDATED (Last updated: 2026-02-28 17:00)

✓ DIV_06_HR: VALIDATED (Last updated: 2026-02-28 09:00)

✓ DIV_07_TRAINING: VALIDATED (Last updated: 2026-02-27 15:45)

✓ DIV_08_PENSIONS: VALIDATED (Last updated: 2026-02-28 11:30)

✓ DIV_09_IT: VALIDATED (Last updated: 2026-02-26 13:20)

✓ DIV_10_AUDIT: VALIDATED (Last updated: 2026-02-28 16:00)

ACTION: Division 03 must update status to VALIDATED before final generation

\================================================================================

DATA VALIDATION ERRORS

\================================================================================

ERROR: DIV_02_DISTRICTS Row 12: FEB value=55000 exceeds maximum (50000)

ERROR: DIV_05_EVENTS Row 8: Photo folder missing: 2026-02-25_TRAINING-EVENT

WARNINGS:

WARNING: DIV_01_SCORECARDS: Feb recruitment (5200) significantly below target (7000)

WARNING: DIV_05_EVENTS: Event count (14) approaching limit (15)

\================================================================================

PHOTO CHECK

\================================================================================

✓ Director photos: 7/7 found

✗ Event photos: 

   - 2026-02-18_AWARDS-KUR: 5 photos (✓)

   - 2026-02-25_TRAINING-EVENT: MISSING FOLDER (✗)

\================================================================================

SUMMARY

\================================================================================

Total Errors: 2

Total Warnings: 2

Generation Status: BLOCKED (fix errors first)

Next Steps:

1\. Contact Division 02 to correct Feb value for Row 12

2\. Contact Division 05 to upload missing photo folder

3\. Re-run validation after corrections

## **5\. COORDINATOR WORKFLOW CHECKLIST**

### **5.1 Monthly Data Collection (Timeline)**

**Day 1-5 of following month:**

- \[ \] Send reminder email to all 10 divisions

- \[ \] Provide template files if needed

**Day 6-20:**

- \[ \] Monitor division submissions (check email notifications)

- \[ \] Track STATUS column in Master Excel

**Day 21:**

- \[ \] Run validation script: python validate_data.py --month 2026-02

- \[ \] Review validation report

- \[ \] Contact divisions with errors/warnings

**Day 22-25:**

- \[ \] Divisions correct errors

- \[ \] Re-run validation until clean

**Day 26:**

- \[ \] Generate PREVIEW PDF: python main.py --month 2026-02 --mode preview

- \[ \] Review preview for layout issues

**Day 27:**

- \[ \] Request final approval from management

- \[ \] Generate FINAL PDF: python main.py --month 2026-02 --mode final

**Day 28:**

- \[ \] Send to printing

- \[ \] Archive files in /output/archive/2026-02/

## **6\. TROUBLESHOOTING COMMON ISSUES**

### **Issue 1: "Division data not updating in Master"**

**Cause:** Linked formula broken (file moved/renamed) **Fix:**

1.  Check division template file path matches Master formula

2.  Re-establish link: **Data > Edit Links > Update Values**

### **Issue 2: "Photo folder not found error"**

**Cause:** Folder name mismatch between Excel and file system **Fix:**

1.  Verify exact folder name in Excel (case-sensitive)

2.  Check /assets/images/events/ directory

3.  Ensure folder exists before running script

### **Issue 3: "Sinhala text appears as boxes in PDF"**

**Cause:** Font not registered in Python script **Fix:** Verify Noto Sans Sinhala font in /assets/fonts/

### **Issue 4: "Chart data not updating"**

**Cause:** Chart script reading old cached data **Fix:** Delete /output/charts/ folder, regenerate

## **7\. BACKUP & RECOVERY**

### **7.1 Automatic Backup Protocol**

**Before each PDF generation:**

import shutil

from datetime import datetime

def backup_master_sheet(month):

    timestamp = datetime.now().strftime("%Y%m%d\_%H%M%S")

    source = "data/master_sheet.xlsx"

    backup = f"data/backups/master\_{month}\_{timestamp}.xlsx"

    shutil.copy(source, backup)

    print(f"Backup created: {backup}")

**Retention:** Keep 6 months of backups (delete older)

**Document Version:** 1.0 **Last Updated:** February 7, 2026 **Next Review:** After first month implementation
