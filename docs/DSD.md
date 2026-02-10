**Data Specification Document: Excel Templates & Master Sheet**
===============================================================

**Version:** 1.0 **Date:** February 7, 2026 **Purpose:** Define exact Excel structure for all 10 divisions

**1\. MASTER EXCEL STRUCTURE**
------------------------------

### **1.1 File Details**

*   **Filename:** SSB\_Master\_Report\_2026.xlsx
    
*   **Location:** /data/master\_sheet.xlsx
    
*   **Access:** Read-only for divisions; Edit access for Coordinator only
    
*   **Update Mechanism:** Linked formulas from division templates (auto-refresh)
    

### **1.2 Sheet Organization**

**Sheet Name**

**Source Division**

**Data Type**

**Rows**

**Columns**

DIV\_01\_SCORECARDS

Social Security Dept

Metrics

12 (months)

15

DIV\_02\_DISTRICTS

District Offices

Performance

25 (districts) × 12 (months)

8

DIV\_03\_FINANCIALS

Finance Dept

Accounting

50 (line items)

14

DIV\_04\_BOARD

Admin/HR

Personnel

7 (directors)

6

DIV\_05\_EVENTS

Public Relations

Activities

Variable (max 15/month)

7

DIV\_06\_HR

Human Resources

Staff data

12 (months)

10

DIV\_07\_TRAINING

Training Unit

Programs

Variable (max 20/month)

9

DIV\_08\_PENSIONS

Pension Dept

Disbursement

12 (months)

12

DIV\_09\_IT

IT Department

Tech initiatives

Variable

8

DIV\_10\_AUDIT

Internal Audit

Findings

Variable

10

**2\. DIVISION TEMPLATE SPECIFICATIONS**
----------------------------------------

### **2.1 General Rules (Apply to ALL Templates)**

**Mandatory Metadata Cells:**

Cell A1: Division Code (e.g., "DIV\_01")

Cell B1: Division Name (Sinhala, e.g., "සමාජ ආරක්ෂණ අංශය")

Cell A2: Report Month (format: "2026-02")

Cell B2: Status (dropdown: "DRAFT" | "VALIDATED" | "APPROVED")

Cell A3: Last Updated (auto-timestamp formula: =NOW())

Cell B3: Responsible Officer Name

**Data Validation:**

*   All numeric cells: Data > Validation > Decimal, Min=0
    
*   Date cells: Data > Validation > Date, Format=YYYY-MM-DD
    
*   Status cell: Data > Validation > List = {DRAFT, VALIDATED, APPROVED}
    

**Formatting:**

*   Header row: Bold, Background #002366 (Navy), Font white
    
*   Number format: #,##0 (thousands separator, no decimals for counts)
    
*   Currency format: #,##0.00 (two decimals for financial values)
    
*   Date format: YYYY-MM-DD (ISO 8601)
    

**2.2 TEMPLATE 1: Scorecards (Division 01)**
--------------------------------------------

**Filename:** DIV\_01\_Scorecards\_Template.xlsx

**Sheet Name:** MONTHLY\_METRICS

**Structure:**

**Row**

**Column A**

**Column B**

**Column C**

**Column D**

**...**

**Column O**

1

DIV\_CODE

DIV\_NAME

\-

\-

\-

\-

2

MONTH

STATUS

LAST\_UPDATED

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

**RECRUITMENT\_TARGET**

**RECRUITMENT\_ACTUAL**

**GROWTH\_PCT**

**ANNUAL\_COLLECTION**

**FIRST\_PREMIUM**

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

RECRUITMENT\_TARGET

Integer

Validation: ≥0, ≤100000

Monthly target (from annual plan)

C

RECRUITMENT\_ACTUAL

Integer

**USER INPUT**

Actual new members recruited

D

GROWTH\_PCT

Decimal

\=(C-B)/B\*100

% growth (actual vs target)

E

ANNUAL\_COLLECTION

Decimal

**USER INPUT**

Total collections (million LKR)

F

FIRST\_PREMIUM

Decimal

**USER INPUT**

First premium income (million LKR)

**Master Sheet Link:**

\# In Master Sheet (DIV\_01\_SCORECARDS)

Cell B5: ='\[DIV\_01\_Scorecards\_Template.xlsx\]MONTHLY\_METRICS'!$C$5

Cell E5: ='\[DIV\_01\_Scorecards\_Template.xlsx\]MONTHLY\_METRICS'!$E$5

\# ... (repeat for all months and metrics)

**2.3 TEMPLATE 2: District Performance (Division 02)**
------------------------------------------------------

**Filename:** DIV\_02\_Districts\_Template.xlsx

**Sheet Name:** DISTRICT\_MONTHLY

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
    
    *   Top 5 districts: Green background
        
    *   Bottom 5 districts: Yellow background
        
3.  **Data Validation:** Each cell (B5:M29) must be integer ≥0
    

**Master Sheet Link:**

\# Master pulls entire table range

\='\[DIV\_02\_Districts\_Template.xlsx\]DISTRICT\_MONTHLY'!$A$5:$H$29

**2.4 TEMPLATE 3: Financial Data (Division 03)**
------------------------------------------------

**Filename:** DIV\_03\_Financials\_Template.xlsx

**Sheet Name:** INCOME\_STATEMENT

**Structure:**

**Row**

**A**

**B**

**C**

**D**

**...**

**N**

4

**LINE\_ITEM**

**CATEGORY**

**JAN**

**FEB**

...

**ANNUAL\_TOTAL**

5

සාමාජික දායකත්ව

INCOME

\[input\]

\[input\]

...

\[=SUM(C5:M5)\]

6

\- තැපැල් කාර්යාල

INCOME\_SUB

187147374

\[input\]

...

\[formula\]

7

\- බැංකු හා වෙනත්

INCOME\_SUB

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

*   CATEGORY values: {INCOME, INCOME\_SUB, EXPENSE, EXPENSE\_SUB}
    
*   All numeric cells: Decimal, ≥0
    
*   SUB-categories must indent (use CONCATENATE(" - ", text))
    

**Auto-Calculations:**

\# Row 50: Total Income

\=SUMIF($B$5:$B$49, "INCOME", $N$5:$N$49)

\# Row 51: Total Expenses

\=SUMIF($B$5:$B$49, "EXPENSE", $N$5:$N$49)

\# Row 52: Net Surplus

\=N50-N51

**2.5 TEMPLATE 4: Board of Directors (Division 04)**
----------------------------------------------------

**Filename:** DIV\_04\_Board\_Template.xlsx

**Sheet Name:** DIRECTORS

**Structure:**

**A**

**B**

**C**

**D**

**E**

**F**

**NAME\_SINHALA**

**NAME\_ENGLISH**

**POSITION**

**BIO**

**PHOTO\_FILENAME**

**ORDER**

එම්.කේ.බී.දිසානායක මහතා

M.K.B. Dissanayake

සභාපති

\[300 char max\]

DIRECTOR\_DISSANAYAKE.jpg

1

...

...

අධ්‍යක්ෂ මණ්ඩල සාමාජික

\[300 char max\]

DIRECTOR\_XXX.jpg

2

**Validation:**

*   BIO: =LEN(D5)<=300 (character limit)
    
*   PHOTO\_FILENAME: Must exist in /assets/images/directors/
    
*   ORDER: Unique integers 1-7 (for display sequence)
    

**Photo File Naming:**

Format: DIRECTOR\_\[LASTNAME\].jpg

Examples:

\- DIRECTOR\_DISSANAYAKE.jpg

\- DIRECTOR\_HERATH.jpg

**2.6 TEMPLATE 5: Events (Division 05) - CRITICAL**
---------------------------------------------------

**Filename:** DIV\_05\_Events\_Template.xlsx

**Sheet Name:** MONTHLY\_EVENTS

**Structure:**

**A**

**B**

**C**

**D**

**E**

**F**

**G**

**EVENT\_DATE**

**EVENT\_TITLE**

**DESCRIPTION**

**LOCATION**

**PARTICIPANTS**

**PHOTO\_FOLDER**

**PHOTO\_COUNT**

2026-01-28

අමාත්‍යවරයා සමග සාකච්ඡාව

\[500 char max\]

අමාත්‍යාංශ පරිශ්‍රය

25

2026-01-28\_MINISTER

3

2026-02-18

සම්මාන උළෙල - කුරුණෑගල

\[500 char max\]

කුරුණෑගල දිස්ත්‍රික් කාර්යාලය

50

2026-02-18\_AWARDS-KUR

5

**Critical Rules:**

1.  **Max 15 events per month** (validation: row count ≤15)
    
2.  **EVENT\_DATE:** Must be within current reporting month
    
3.  **DESCRIPTION:** Character limit enforced: =LEN(C5)<=500
    
4.  **PHOTO\_FOLDER:** Naming convention enforced
    

**Photo Management:**

Directory structure:

/assets/images/events/

├── 2026-01-28\_MINISTER/

│   ├── 01.jpg  (auto-numbered)

│   ├── 02.jpg

│   └── 03.jpg

├── 2026-02-18\_AWARDS-KUR/

│   ├── 01.jpg

│   ├── 02.jpg

│   ├── 03.jpg

│   ├── 04.jpg

│   └── 05.jpg

**Python Auto-Detection:**

\# Script automatically finds all photos in folder

photo\_folder = "2026-01-28\_MINISTER"

photo\_paths = glob.glob(f"assets/images/events/{photo\_folder}/\*.jpg")

\# Returns: \[01.jpg, 02.jpg, 03.jpg\]

**2.7 TEMPLATES 6-10: Simplified Specifications**
-------------------------------------------------

### **Template 6: HR Statistics (Division 06)**

**Columns:** MONTH | TOTAL\_STAFF | NEW\_HIRES | RESIGNATIONS | PROMOTIONS | TRAINING\_HOURS

### **Template 7: Training Programs (Division 07)**

**Columns:** DATE | PROGRAM\_NAME | PARTICIPANTS | DURATION\_DAYS | LOCATION | COST

### **Template 8: Pension Disbursement (Division 08)**

**Columns:** MONTH | PENSIONERS\_COUNT | TOTAL\_AMOUNT | DEATH\_BENEFITS | PARTIAL\_REFUNDS

### **Template 9: IT Initiatives (Division 09)**

**Columns:** PROJECT\_NAME | STATUS | START\_DATE | COMPLETION\_PCT | BUDGET | DESCRIPTION

### **Template 10: Audit Findings (Division 10)**

**Columns:** AUDIT\_DATE | DIVISION | FINDING | SEVERITY | STATUS | ACTION\_PLAN

**3\. DATA LINKING MECHANISM (Master ← Templates)**
---------------------------------------------------

### **3.1 Automatic Update Formula**

**In Master Sheet (DIV\_01\_SCORECARDS tab):**

\# Cell mapping example

Cell C8 (Feb Recruitment): ='C:\\SSB\\data\\division\_templates\\\[DIV\_01\_Scorecards\_Template.xlsx\]MONTHLY\_METRICS'!$C$6

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
    

**4\. DATA VALIDATION SCRIPT (Python)**
---------------------------------------

### **4.1 Validation Checks**

\# validation\_rules.py

VALIDATION\_RULES = {

    "DIV\_01\_SCORECARDS": {

        "required\_columns": \["MONTH", "RECRUITMENT\_ACTUAL", "ANNUAL\_COLLECTION"\],

        "numeric\_ranges": {

            "RECRUITMENT\_ACTUAL": (0, 100000),

            "ANNUAL\_COLLECTION": (0.0, 2000.0),

            "FIRST\_PREMIUM": (0.0, 1000.0)

        },

        "date\_format": "YYYY-MM"

    },

    "DIV\_02\_DISTRICTS": {

        "required\_rows": 25,  # Must have all 25 districts

        "district\_names": \[

            "නුවරඑළිය", "කුරුණෑගල", "යාපනය", ...  # Full list

        \],

        "numeric\_ranges": {

            "JAN": (0, 50000),

            "FEB": (0, 50000),

            # ... for all months

        }

    },

    "DIV\_05\_EVENTS": {

        "max\_rows": 15,  # Max 15 events per month

        "required\_columns": \["EVENT\_DATE", "EVENT\_TITLE", "PHOTO\_FOLDER"\],

        "character\_limits": {

            "DESCRIPTION": 500,

            "EVENT\_TITLE": 100

        },

        "photo\_validation": True  # Check if PHOTO\_FOLDER exists

    }

}

\# Validation execution

def validate\_master\_sheet(master\_file\_path):

    wb = openpyxl.load\_workbook(master\_file\_path)

    errors = \[\]

    for sheet\_name, rules in VALIDATION\_RULES.items():

        sheet = wb\[sheet\_name\]

        # Check required columns exist

        header\_row = \[cell.value for cell in sheet\[4\]\]

        for col in rules\["required\_columns"\]:

            if col not in header\_row:

                errors.append(f"{sheet\_name}: Missing column {col}")

        # Check numeric ranges

        if "numeric\_ranges" in rules:

            for col, (min\_val, max\_val) in rules\["numeric\_ranges"\].items():

                col\_idx = header\_row.index(col)

                for row in sheet.iter\_rows(min\_row=5, max\_row=sheet.max\_row):

                    val = row\[col\_idx\].value

                    if val and (val < min\_val or val > max\_val):

                        errors.append(f"{sheet\_name} Row {row\[0\].row}: {col}={val} out of range \[{min\_val}, {max\_val}\]")

        # Check photo folders exist

        if rules.get("photo\_validation"):

            photo\_col\_idx = header\_row.index("PHOTO\_FOLDER")

            for row in sheet.iter\_rows(min\_row=5, max\_row=sheet.max\_row):

                folder = row\[photo\_col\_idx\].value

                if folder and not os.path.exists(f"assets/images/events/{folder}"):

                    errors.append(f"{sheet\_name} Row {row\[0\].row}: Photo folder missing: {folder}")

    return errors

### **4.2 Validation Report Output**

**File:** /output/logs/validation\_report\_2026-02.txt

SSB MONTHLY REPORT VALIDATION

Generated: 2026-03-01 09:15:23

Month: February 2026

\================================================================================

DIVISION STATUS CHECK

\================================================================================

✓ DIV\_01\_SCORECARDS: VALIDATED (Last updated: 2026-02-28 16:30)

✓ DIV\_02\_DISTRICTS: VALIDATED (Last updated: 2026-02-28 14:20)

✗ DIV\_03\_FINANCIALS: DRAFT (Last updated: 2026-02-25 10:15) ← ACTION REQUIRED

✓ DIV\_04\_BOARD: APPROVED (Last updated: 2026-01-15 11:00)

✗ DIV\_05\_EVENTS: VALIDATED (Last updated: 2026-02-28 17:00)

✓ DIV\_06\_HR: VALIDATED (Last updated: 2026-02-28 09:00)

✓ DIV\_07\_TRAINING: VALIDATED (Last updated: 2026-02-27 15:45)

✓ DIV\_08\_PENSIONS: VALIDATED (Last updated: 2026-02-28 11:30)

✓ DIV\_09\_IT: VALIDATED (Last updated: 2026-02-26 13:20)

✓ DIV\_10\_AUDIT: VALIDATED (Last updated: 2026-02-28 16:00)

ACTION: Division 03 must update status to VALIDATED before final generation

\================================================================================

DATA VALIDATION ERRORS

\================================================================================

ERROR: DIV\_02\_DISTRICTS Row 12: FEB value=55000 exceeds maximum (50000)

ERROR: DIV\_05\_EVENTS Row 8: Photo folder missing: 2026-02-25\_TRAINING-EVENT

WARNINGS:

WARNING: DIV\_01\_SCORECARDS: Feb recruitment (5200) significantly below target (7000)

WARNING: DIV\_05\_EVENTS: Event count (14) approaching limit (15)

\================================================================================

PHOTO CHECK

\================================================================================

✓ Director photos: 7/7 found

✗ Event photos: 

   - 2026-02-18\_AWARDS-KUR: 5 photos (✓)

   - 2026-02-25\_TRAINING-EVENT: MISSING FOLDER (✗)

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

**5\. COORDINATOR WORKFLOW CHECKLIST**
--------------------------------------

### **5.1 Monthly Data Collection (Timeline)**

**Day 1-5 of following month:**

*   \[ \] Send reminder email to all 10 divisions
    
*   \[ \] Provide template files if needed
    

**Day 6-20:**

*   \[ \] Monitor division submissions (check email notifications)
    
*   \[ \] Track STATUS column in Master Excel
    

**Day 21:**

*   \[ \] Run validation script: python validate\_data.py --month 2026-02
    
*   \[ \] Review validation report
    
*   \[ \] Contact divisions with errors/warnings
    

**Day 22-25:**

*   \[ \] Divisions correct errors
    
*   \[ \] Re-run validation until clean
    

**Day 26:**

*   \[ \] Generate PREVIEW PDF: python main.py --month 2026-02 --mode preview
    
*   \[ \] Review preview for layout issues
    

**Day 27:**

*   \[ \] Request final approval from management
    
*   \[ \] Generate FINAL PDF: python main.py --month 2026-02 --mode final
    

**Day 28:**

*   \[ \] Send to printing
    
*   \[ \] Archive files in /output/archive/2026-02/
    

**6\. TROUBLESHOOTING COMMON ISSUES**
-------------------------------------

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

**7\. BACKUP & RECOVERY**
-------------------------

### **7.1 Automatic Backup Protocol**

**Before each PDF generation:**

import shutil

from datetime import datetime

def backup\_master\_sheet(month):

    timestamp = datetime.now().strftime("%Y%m%d\_%H%M%S")

    source = "data/master\_sheet.xlsx"

    backup = f"data/backups/master\_{month}\_{timestamp}.xlsx"

    shutil.copy(source, backup)

    print(f"Backup created: {backup}")

**Retention:** Keep 6 months of backups (delete older)

**Document Version:** 1.0 **Last Updated:** February 7, 2026 **Next Review:** After first month implementation