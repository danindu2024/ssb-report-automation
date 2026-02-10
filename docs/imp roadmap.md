**Implementation Roadmap: SSB Report Automation**
=================================================

**Version:** 1.0 **Date:** February 7, 2026 **Total Timeline:** 5 Weeks (Aggressive) | 8 Weeks (Conservative)

**PHASE 1: INFRASTRUCTURE SETUP (Week 1)**
------------------------------------------

### **Week 1.1: Development Environment**

**Tasks:**

*   \[ \] Install Python 3.9+ on workstation
    

\[ \] Install required libraries:pip install weasyprint openpyxl pillow-heif matplotlib jinja2

\# For Ubuntu/Debian:

sudo apt-get install python3-pip python3-cffi python3-brotli \\

    libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz-subset0

\# For macOS:

brew install cairo pango gdk-pixbuf

\[ \] Set up directory structure: mkdir -p ssb-report-automation/{data,assets,src,templates,output}mkdir -p assets/images/{events/raw,events/processed,directors,signatures}mkdir -p output/{preview,final,logs,charts}

\[ \] Test Sinhala font rendering:from weasyprint import HTML

html\_content = """

    

    </p><p class="slate-paragraph">        @font-face {</p><p class="slate-paragraph">            font-family: &#x27;Noto Sans Sinhala&#x27;;</p><p class="slate-paragraph">            src: url(&#x27;assets/fonts/NotoSansSinhala-Regular.ttf&#x27;);</p><p class="slate-paragraph">        }</p><p class="slate-paragraph">        body { font-family: &#x27;Noto Sans Sinhala&#x27;; font-size: 14pt; }</p><p class="slate-paragraph">    

ශ්‍රී ලංකා සමාජ ආරක්ෂණ මණ්ඩලය
=============================

මාසික වාර්තාව - 2026

"""

HTML(string=html\_content).write\_pdf('test\_sinhala.pdf')

print("✓ Sinhala rendering test passed")

**Deliverables:**

*   Working Python environment
    
*   Directory structure created
    
*   Test PDF with Sinhala text generated
    

**Risk Mitigation:**

*   If Sinhala font doesn't render: Download Noto Sans Sinhala from Google Fonts
    
*   If Pillow install fails: Use conda instead of pip (conda install pillow)
    

**PHASE 2: DATA LAYER (Week 2)**
--------------------------------

### **Week 2.1: Excel Template Creation**

**Tasks:**

*   \[ \] Create master Excel template (SSB\_Master\_Report\_2026.xlsx)
    
    *   Define 10 division sheets with exact column structure (see Data Spec doc)
        
    *   Add metadata rows (Division Code, Month, Status, Last Updated)
        
    *   Apply data validation rules (dropdowns, number ranges)
        
*   \[ \] Create Division 01 template (DIV\_01\_Scorecards\_Template.xlsx)
    
    *   Link to master sheet using formulas
        
    *   Test auto-update mechanism
        
*   \[ \] Document Excel usage guide for divisions (separate doc)
    

**Deliverables:**

*   Master Excel file with all 10 sheets
    
*   Division 01 template (test case)
    
*   User guide PDF
    

**Testing:**

1.  Update Division 01 template, save
    
2.  Open master, click "Refresh All"
    
3.  Verify data appears correctly
    

### **Week 2.2: Data Extraction Module**

**Tasks:**

\[ \] Build data\_loader.py: def load\_master\_sheet(filepath):

    """Extract all division data from master Excel"""

    wb = openpyxl.load\_workbook(filepath, data\_only=True)

    data = {

        "report\_meta": extract\_metadata(wb),

        "scorecards": extract\_scorecards(wb\["DIV\_01\_SCORECARDS"\]),

        "districts": extract\_districts(wb\["DIV\_02\_DISTRICTS"\]),

        # ... for all 10 divisions

    }

    return data

\[ \] Build data\_validator.py: def validate\_data(data):

    """Check for missing/invalid data, return error list"""

    errors = \[\]

    # Check scorecards

    if data\["scorecards"\]\["recruitment\_actual"\] < 0:

        errors.append("Invalid recruitment count")

    # Check photo folders exist

    for event in data\["events"\]:

        if not os.path.exists(f"assets/images/events/raw/{event\['photo\_folder'\]}"):

            errors.append(f"Missing photo folder: {event\['photo\_folder'\]}")

    return errors

**Deliverables:**

*   Data loader extracting all 10 divisions
    
*   Validation script with 20+ rules
    
*   Test data set (sample February 2026 data)
    

**Testing:**

1.  Load master Excel
    
2.  Print extracted JSON to verify structure
    
3.  Run validator, confirm it catches intentional errors
    

**PHASE 3: IMAGE PROCESSING (Week 3)**
--------------------------------------

### **Week 3.1: Core Image Processor**

**Tasks:**

*   \[ \] Implement image\_processor.py (see Image Processing doc for full code)
    
    *   Auto-rotate function
        
    *   Smart crop function
        
    *   Batch processing function
        
*   \[ \] Test with sample event photos:
    
    *   Mix of portrait/landscape
        
    *   Different resolutions (1024×768 to 6000×4000)
        
    *   Various formats (JPG, PNG, HEIC if possible)
        

**Deliverables:**

*   Working image processor handling all formats
    
*   Proof sheet generator
    
*   Validation report for images
    

**Testing:**

1.  Create test folder: 2026-TEST-EVENT/ with 10 varied photos
    
2.  Run: python process\_images.py --event 2026-TEST-EVENT
    
3.  Verify all photos cropped to 800×600
    
4.  Check proof sheet PDF shows before/after correctly
    

### **Week 3.2: Integration with Excel**

**Tasks:**

*   \[ \] Auto-count processed photos and update Excel
    
*   \[ \] Generate image validation report
    
*   \[ \] Handle missing photo errors gracefully
    

**Deliverables:**

*   Excel auto-update working
    
*   Validation report in /output/logs/
    

**PHASE 4: PDF GENERATION ENGINE (Weeks 4-5)**
----------------------------------------------

### **Week 4.1: Template System**

**Tasks:**

**\- \[ \] Create base HTML template with print CSS (\`/templates/base.html\`)**

**\- \[ \] Define CSS for page layout, headers, footers**

**\- \[ \] Implement @page rules for print-specific styling**

**\- \[ \] Create section templates (cover, scorecards, events, etc.)**

**\- \[ \] Test HTML rendering in browser before PDF conversion**

**Code Example (HTML Template):**

**\`\`\`html**

        **@page {**

            **size: A4;**

            **margin: 2.54cm;**

            **@bottom-right {**

                **content: "පිටුව " counter(page);**

                **font-family: 'Noto Sans Sinhala';**

            **}**

        **}**

        **body {**

            **font-family: 'Noto Sans Sinhala', sans-serif;**

            **font-size: 11pt;**

        **}**

        **.keep-together {**

            **page-break-inside: avoid;**

        **}**

    **{% for event in events %}**

        **{{ event.title }}**

        **{{ event.description }}**

    **{% endfor %}**

**\`\`\`**

**Deliverables:**

**\- Base HTML template with print CSS**

**\- 5+ section templates (cover, scorecards, events, etc.)**

**\- Test HTML viewable in browser**

### **Week 4.2: Content Sections (Critical)**

Tasks:

\- \[ \] Build Jinja2 HTML builder module (\`html\_builder.py\`)

\- \[ \] Create event cards template with CSS styling

\- \[ \] Create district table template

\- \[ \] Create board members grid layout

\- \[ \] Implement dynamic content rendering

Code Example (Python HTML Builder):

\`\`\`python

from jinja2 import Environment, FileSystemLoader

class HTMLReportBuilder:

    def \_\_init\_\_(self):

        self.env = Environment(loader=FileSystemLoader('templates'))

    def build\_events\_section(self, events\_data):

        template = self.env.get\_template('section\_events.html')

        return template.render(events=events\_data)

    def build\_complete\_html(self, data):

        sections = \[\]

        sections.append(self.build\_cover\_page(data))

        sections.append(self.build\_scorecards(data))

        sections.append(self.build\_events\_section(data\['events'\]))

        # ... more sections

        base\_template = self.env.get\_template('base.html')

        return base\_template.render(content=''.join(sections))

\`\`\`

Deliverables:

\- HTML builder module

\- All section templates created

\- Sample HTML generated from test data

### **Week 5.1: Charts & Visualizations**

**Tasks:**

*   \[ \] Implement chart\_generator.py:
    
    *   District bar chart (Matplotlib)
        
    *   Financial trend line chart
        
    *   Recruitment growth chart
        
*   \[ \] Ensure Sinhala labels render correctly
    
*   \[ \] Embed charts in PDF (high-res, 300 DPI)
    

**Code Example:**

import matplotlib.pyplot as plt

def generate\_district\_chart(district\_data):

    plt.rcParams\['font.family'\] = 'Noto Sans Sinhala'

    fig, ax = plt.subplots(figsize=(10, 6))

    districts = \[d\['name'\] for d in district\_data\[:10\]\]  # Top 10

    counts = \[d\['count'\] for d in district\_data\[:10\]\]

    bars = ax.bar(districts, counts, color='#800000')

    ax.set\_xlabel('දිස්ත්‍රික්කය', fontsize=12)

    ax.set\_ylabel('සාමාජිකයින්', fontsize=12)

    plt.xticks(rotation=45, ha='right')

    plt.tight\_layout()

    plt.savefig('output/charts/districts.png', dpi=300, bbox\_inches='tight')

    plt.close()

    return 'output/charts/districts.png'

\### Embedding Charts in HTML:

Charts can be embedded as base64 or file references:

\`\`\`python

\# Method 1: File reference

\# Method 2: Base64 embedding (faster)

import base64

with open(chart\_path, 'rb') as f:

    chart\_data = base64.b64encode(f.read()).decode()

chart\_uri = f"data:image/png;base64,{chart\_data}"

\`\`\`

**Deliverables:**

*   5 chart types working
    
*   Charts embedded in PDF correctly
    
*   Sinhala text rendering verified
    

### **Week 5.2: Preview & Final Modes**

**Tasks:**

**\- \[ \] Implement CSS-based watermark for preview mode**

**\- \[ \] Build WeasyPrint PDF generation module**

**\- \[ \] Test both preview and final modes**

**Code Example (CSS Watermark):**

**\`\`\`css**

**/\* In base.html, conditional CSS \*/**

**{% if mode == 'preview' %}**

**@page {**

    **background: url('data:image/svg+xml;utf8,DRAFT') center center no-repeat;**

**}**

**{% endif %}**

**\`\`\`**

**Code Example (PDF Generation):**

**\`\`\`python**

**from weasyprint import HTML, CSS**

**from weasyprint.text.fonts import FontConfiguration**

**class PDFGenerator:**

    **def \_\_init\_\_(self, mode='preview'):**

        **self.mode = mode**

        **self.font\_config = FontConfiguration()**

    **def generate\_pdf(self, html\_content, output\_path):**

        **HTML(string=html\_content).write\_pdf(**

            **output\_path,**

            **font\_config=self.font\_config**

        **)**

**\`\`\`**

**Deliverables:**

**\- Preview mode with CSS watermark**

**\- Final mode without watermark**

**\- Both modes tested successfully**

**PHASE 5: INTEGRATION & TESTING (Week 6)**
-------------------------------------------

### **Week 6.1: End-to-End Testing**

**Test Case 1: Happy Path (Complete Data)**

Steps:

1\. \`python validate\_data.py --month 2026-02\`

2\. \`python process\_images.py --batch --month 2026-02\`

3\. \`python main.py --month 2026-02 --mode preview\`

4\. \*\*NEW:\*\* Open generated HTML in browser to verify layout

5\. Review PDF preview

6\. \`python main.py --month 2026-02 --mode final\`

Expected Output:

\- HTML renders correctly in Chrome/Firefox

\- PDF has proper Sinhala text (no broken characters)

\- 52-page PDF, all sections rendered

\- Generation time: <30 seconds

**Test Case 2: Missing Data**

Input: Division 05 missing event photos

Expected Output: Validation error, generation blocked

Steps:

1\. python validate\_data.py --month 2026-02

Expected: Error message listing missing photo folders

**Test Case 3: Maximum Content (Stress Test)**

Input: 15 events, all districts, maximum data

Expected Output: PDF generation completes in <30 seconds

Steps:

1\. Time generation process

2\. Verify pagination correct (no broken tables)

3\. Check file size reasonable (<10MB)

**Deliverables:**

*   Test report documenting all 10 test cases
    
*   Bug fixes for any failures
    
*   Performance tuning if generation >30 seconds
    

\### Test Case 4: Sinhala Text Rendering

Input: Report with extensive Sinhala content

Expected Output: All Sinhala text renders correctly (no boxes, proper ligatures)

Steps:

1\. Generate PDF

2\. Open in Adobe Reader

3\. Search for sample Sinhala text (e.g., "සමාජ ආරක්ෂණ")

4\. Verify text is selectable and searchable

5\. Print test page to verify print quality

Success Criteria:

\- ✅ No broken characters

\- ✅ Proper vowel placement

\- ✅ Text is searchable

\- ✅ Copy-paste preserves Unicode

### **Week 6.2: User Documentation**

**Tasks:**

*   \[ \] Write "Division Template User Guide" (PDF)
    
    *   How to fill Excel template
        
    *   Photo upload instructions
        
    *   Common mistakes to avoid
        
*   \[ \] Write "Coordinator Manual" (PDF)
    
    *   Monthly workflow checklist
        
    *   Running scripts (step-by-step commands)
        
    *   Troubleshooting guide
        
*   \[ \] Create video tutorial (optional, 10 minutes)
    
    *   Screen recording of full process
        
    *   Narration in Sinhala
        

**Deliverables:**

*   Division User Guide PDF (20 pages)
    
*   Coordinator Manual PDF (30 pages)
    
*   Video tutorial (if time permits)
    

**PHASE 6: TRAINING & HANDOVER (Week 7)**
-----------------------------------------

### **Week 7.1: Division Training Session**

**Audience:** Representatives from all 10 divisions

**Agenda:**

1.  System overview (30 min)
    
2.  Excel template walkthrough (45 min)
    
3.  Photo upload demo (30 min)
    
4.  Q&A (30 min)
    

**Materials:**

*   Printed user guides (10 copies)
    
*   Sample Excel templates on USB drives
    
*   Training data set for practice
    

**Deliverables:**

*   Training attendance sheet (signed by all divisions)
    
*   Feedback forms (identify pain points)
    
*   Action items list (any template changes requested)
    

### **Week 7.2: Coordinator Training**

**Audience:** IT department staff who will run the system

**Agenda:**

1.  Technical architecture overview (1 hour)
    
2.  Running scripts hands-on (2 hours)
    
    *   Data validation
        
    *   Image processing
        
    *   PDF generation
        
3.  Troubleshooting common issues (1 hour)
    
4.  Monthly workflow practice (1 hour)
    

**Deliverables:**

*   Coordinator trained and certified
    
*   Technical documentation reviewed and approved
    
*   Backup coordinator identified
    

**PHASE 7: PILOT RUN (Week 8)**
-------------------------------

### **Week 8: March 2026 Report (Test Run)**

**Goal:** Generate real March 2026 report using the system

**Timeline:**

*   **Day 1-5:** Divisions submit March data
    
*   **Day 6:** Coordinator validates data, requests corrections
    
*   **Day 7-10:** Divisions fix errors
    
*   **Day 11:** Run image processing
    
*   **Day 12:** Generate preview PDF
    
*   **Day 13:** Management review
    
*   **Day 14:** Generate final PDF
    
*   **Day 15:** Send to printing
    
*   **Day 16-20:** Collect feedback from stakeholders
    

**Success Metrics:**

*   \[ \] Report generated without manual intervention
    
*   \[ \] Less than 3 rounds of corrections needed
    
*   \[ \] PDF quality matches or exceeds previous manual reports
    
*   \[ \] Generation time <30 seconds
    
*   \[ \] No printing issues (fonts embedded correctly)
    

**Deliverables:**

*   March 2026 printed report
    
*   Feedback summary from management
    
*   Issue log (any bugs encountered)
    
*   Refined workflow based on lessons learned
    

**POST-IMPLEMENTATION: MAINTENANCE PLAN**
-----------------------------------------

### **Monthly Routine (Ongoing)**

**Week 1 (Data Collection):**

*   Send reminder emails to divisions
    
*   Monitor submission status
    

**Week 2-3 (Validation & Processing):**

*   Run validation script
    
*   Process images
    
*   Coordinate with divisions on errors
    

**Week 4 (Generation & Approval):**

*   Generate preview
    
*   Get management approval
    
*   Generate final PDF
    
*   Send to printing
    

### **Quarterly Reviews (Every 3 Months)**

**Review Checklist:**

*   \[ \] Any new divisions added? (update templates)
    
*   \[ \] Layout changes requested? (update templates)
    
*   \[ \] Performance degradation? (optimize scripts)
    
*   \[ \] Division feedback review (improve usability)
    

### **Annual Maintenance (Yearly)**

**Tasks:**

*   \[ \] Update Python libraries: pip install --upgrade -r requirements.txt
    
*   \[ \] Refresh brand colors if style guide changes
    
*   \[ \] Archive old data (move to /archive/ folder)
    
*   \[ \] Test system with new year's data structure
    

**RISK MANAGEMENT**
-------------------

### **Critical Risks & Mitigation**

**Risk**

**Probability**

**Impact**

**Mitigation**

Divisions don't adopt Excel templates

Medium

High

Mandatory training + simplified templates

Data quality poor (errors)

High

Medium

Strict validation script + coordinator review

PDF generation fails on large data

Low

High

Stress testing in Phase 5 + pagination logic

Sinhala fonts don't render

Low

Critical

Test early (Phase 1), use proven Noto fonts

Image processing too slow

Low

Medium

Batch processing + caching optimizations

Key person leaves (knowledge loss)

Medium

High

Document everything + train backup coordinator

### **Contingency Plan**

**If system fails during production:**

1.  **Immediate:** Revert to manual Word template for current month
    
2.  **Week 1:** Debug issue, fix critical bug
    
3.  **Week 2:** Test fix with sample data
    
4.  **Week 3:** Resume automated generation
    

**Backup Strategy:**

*   Keep master Excel backed up daily (OneDrive auto-sync)
    
*   Store 6 months of generated PDFs
    
*   Maintain previous Word templates for 1 year
    

**SUCCESS CRITERIA**
--------------------

### **Phase Completion Metrics**

**Phase 1-2 (Infrastructure + Data):**

*   \[ \] Python environment stable
    
*   \[ \] Excel templates created and tested
    
*   \[ \] Data extraction working for all 10 divisions
    

**Phase 3 (Images):**

*   \[ \] 100 sample photos processed correctly
    
*   \[ \] No manual cropping needed
    
*   \[ \] Proof sheets generated automatically
    

**Phase 4-5 (PDF Generation):**

*   \[ \] 50-page test PDF generated
    
*   \[ \] All sections render correctly
    
*   \[ \] Sinhala text displays properly
    
*   \[ \] Charts embedded with correct data
    

**Phase 6-7 (Training):**

*   \[ \] All 10 divisions trained
    
*   \[ \] Coordinator can run system independently
    
*   \[ \] Documentation complete
    

**Phase 8 (Pilot):**

*   \[ \] Real report printed successfully
    
*   \[ \] Management approval obtained
    
*   \[ \] No critical bugs
    

### **Long-Term Success (3 Months Post-Launch)**

*   \[ \] 3 consecutive monthly reports generated automatically
    
*   \[ \] <5% error rate in division data submission
    
*   \[ \] Generation time <30 seconds consistently
    
*   \[ \] Zero printing/font issues
    
*   \[ \] Coordinator satisfaction rating >8/10
    

**BUDGET & RESOURCES**
----------------------

### **Technology Costs**

**Item**

**Cost**

**Notes**

Python (open source)

Free

WeasyPrint library

Free

Noto Sans Sinhala font

Free

Google Fonts

Microsoft Excel

Existing

Already licensed

**Total:**

**LKR 0**

All open source

**DELIVERABLES CHECKLIST**
--------------------------

### **Technical Deliverables**

*   \[ \] data\_loader.py - Excel extraction
    
*   \[ \] data\_validator.py - Data validation
    
*   \[ \] image\_processor.py - Photo processing
    
*   \[ \] chart\_generator.py - Chart creation
    
*   \[ \] pdf\_builder.py - PDF generation
    
*   \[ \] main.py - Orchestration script
    
*   \[ \] config.py - Configuration settings
    

### **Documentation Deliverables**

*   \[ \] Technical Design Document (this document)
    
*   \[ \] Data Specification Document
    
*   \[ \] Image Processing Strategy
    
*   \[ \] Division User Guide
    
*   \[ \] Coordinator Manual
    
*   \[ \] Troubleshooting Guide
    

### **Data Deliverables**

*   \[ \] Master Excel template
    
*   \[ \] 10 division Excel templates
    
*   \[ \] Sample data set (for testing)
    
*   \[ \] Font files (Noto Sans Sinhala)
    

### **Training Deliverables**

*   \[ \] Training presentation slides
    
*   \[ \] Video tutorial (optional)
    
*   \[ \] Quick reference cards (printed)
    

**TIMELINE VISUALIZATION**
--------------------------

Week 1: \[========== Infrastructure Setup ==========\]

Week 2: \[========== Data Layer ==========\]

Week 3: \[========== Image Processing ==========\]

Week 4: \[===== PDF Templates =====\]

Week 5: \[===== Content Sections & Charts =====\]

Week 6: \[========== Integration & Testing ==========\]

Week 7: \[========== Training ==========\]

Week 8: \[========== Pilot Run (March 2026) ==========\]

─────────────────────────────────────────────────────

        ^                              ^

    START (Feb 7)                  LAUNCH (Apr 1)

**Critical Path:** Data Layer → Image Processing → PDF Generation

**Bottleneck Risk:** Week 4-5 (PDF generation complexity)

**Buffer:** Week 6 dedicated to testing and fixing issues

**NEXT STEPS (Immediate Actions)**
----------------------------------

### **This Week (Feb 7-14, 2026)**

**Priority 1 (Critical):**

1.  Get management approval for Python-based approach
    
2.  Install Python environment and test libraries
    
3.  Download Noto Sans Sinhala font and test rendering
    

**Priority 2 (Important):** 4. Review 2025 report PDF with divisions (identify all sections) 5. Draft master Excel template structure (all 10 sheets) 6. Create sample data set for Division 01 (February 2026)

**Priority 3 (Nice to have):** 7. Research auto-crop algorithms (test OpenCV face detection) 8. Set up version control (Git repository for code)

### **Next Week (Feb 15-21, 2026)**

1.  Complete master Excel template
    
2.  Build data extraction script
    
3.  Test data loader with sample data
    
4.  Begin image processor development
    

**Document Version:** 1.0 **Last Updated:** February 7, 2026 **Owner:** SSB IT Department **Next Review:** After Week 2 completion