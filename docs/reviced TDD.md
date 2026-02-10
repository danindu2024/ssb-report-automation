**Technical Design Document: SSB Monthly Report Automation**
============================================================

**Version: 3.0**
--------------------------------------

**Date:** February 9, 2026 **Author:** System Architect **Project:** Sri Lanka Social Security Board Monthly Report Generation

**1\. EXECUTIVE SUMMARY**
-------------------------

### **1.1 Project Scope**

Automate generation of 50+ page monthly performance reports for Sri Lanka Social Security Board (SSB), consolidating data from 10+ divisions into a professionally formatted Sinhala-language PDF document.

### **1.2 Critical Requirements**

*   **Input:** Excel templates from 10 divisions → Master Excel consolidation
    
*   **Output:** Print-ready PDF with tables, charts, images, and narrative text
    
*   **Languages:** Sinhala (Unicode font support essential)
    
*   **Preview:** Mandatory stakeholder review before final generation
    
*   **Performance:** Must handle 50+ pages with complex layouts efficiently
    

### **1.3 Technology Stack**

**Component**

**Technology**

**Justification**

PDF Generation

**WeasyPrint (Python)**

**Superior Sinhala rendering via Pango/HarfBuzz, CSS-based layouts, proper Unicode support**

Excel Processing

openpyxl (Python)

Native Excel handling, formula evaluation

Charting

Matplotlib/Plotly

Professional chart generation with Sinhala font support

Image Processing

Pillow (PIL)

Automatic cropping, resizing, optimization

Templating

**Jinja2 + HTML/CSS**

**Industry-standard templating with CSS for precise layout control**

Preview Generation

WeasyPrint → PDF viewer

Direct PDF preview with accurate rendering

### **1.4 Why WeasyPrint**

1.  **Perfect Sinhala Rendering:** Built on top of Pango/HarfBuzz for proper text shaping of complex Indic scripts
    
2.  **CSS-Based Layout:** Use standard CSS for page layout, headers, footers, tables
    
3.  **HTML Familiarity:** Easier to maintain with standard web technologies
    
4.  **Print CSS Support:** Full support for @page rules, page breaks, print-specific CSS
    
5.  **Web Fonts:** Easy integration of Google Fonts (Noto Sans Sinhala)
    
6.  **Full Unicode Support:** Handles all Unicode scripts correctly out of the box
    

**Expected Performance:**

*   50-page report: 20-30 seconds
    
*   Acceptable for monthly batch generation workflow
    

**2\. REVISED SYSTEM ARCHITECTURE**
-----------------------------------

### **2.1 Data Flow Pipeline**

*   ┌──────────────────────────────────────────────────────────────┐
    
*   │ STAGE 1: DATA COLLECTION                                     │
    
*   ├──────────────────────────────────────────────────────────────┤
    
*   │ Division 1-10 Excel Templates (separate files)               │
    
*   │ ↓                                                             │
    
*   │ Master Excel Sheet (linked formulas, auto-update)            │
    
*   │ ↓                                                             │
    
*   │ Validation Check (manual review by coordinator)              │
    
*   └──────────────────────────────────────────────────────────────┘
    
*                              ↓
    
*   ┌──────────────────────────────────────────────────────────────┐
    
*   │ STAGE 2: DATA EXTRACTION & TRANSFORMATION                    │
    
*   ├──────────────────────────────────────────────────────────────┤
    
*   │ Python Script reads Master Excel                             │
    
*   │ ↓                                                             │
    
*   │ Data Validation Layer (checks for missing/invalid data)      │
    
*   │ ↓                                                             │
    
*   │ Structured JSON (intermediate representation)                │
    
*   └──────────────────────────────────────────────────────────────┘
    
*                              ↓
    
*   ┌──────────────────────────────────────────────────────────────┐
    
*   │ STAGE 3: ASSET PROCESSING                                    │
    
*   ├──────────────────────────────────────────────────────────────┤
    
*   │ Event Photos + Director Images                               │
    
*   │ ↓                                                             │
    
*   │ Auto-Crop & Resize (Pillow)                                  │
    
*   │ ↓                                                             │
    
*   │ Optimized Images (print quality, standard dimensions)        │
    
*   └──────────────────────────────────────────────────────────────┘
    
*                              ↓
    
*   ┌──────────────────────────────────────────────────────────────┐
    
*   │ STAGE 4: CHART GENERATION                                    │
    
*   ├──────────────────────────────────────────────────────────────┤
    
*   │ Financial data → Bar charts (Matplotlib)                     │
    
*   │ District performance → Tables + Graphs                       │
    
*   │ Trend data → Line charts (monthly comparison)                │
    
*   │ ↓                                                             │
    
*   │ Vector Graphics (high-quality, embedded Sinhala fonts)       │
    
*   └──────────────────────────────────────────────────────────────┘
    
*                              ↓
    
*   ┌──────────────────────────────────────────────────────────────┐
    
*   │ STAGE 5: HTML TEMPLATE GENERATION (NEW)                      │
    
*   ├──────────────────────────────────────────────────────────────┤
    
*   │ Jinja2 Template Engine                                       │
    
*   │ ├─ Load HTML templates with CSS                             │
    
*   │ ├─ Inject data from JSON                                     │
    
*   │ ├─ Render dynamic sections (events, tables)                  │
    
*   │ └─ Apply print-specific CSS (@page rules)                    │
    
*   │ ↓                                                             │
    
*   │ Complete HTML Document (with inline CSS and base64 images)   │
    
*   └──────────────────────────────────────────────────────────────┘
    
*                              ↓
    
*   ┌──────────────────────────────────────────────────────────────┐
    
*   │ STAGE 6: PDF GENERATION (WEASYPRINT)                         │
    
*   ├──────────────────────────────────────────────────────────────┤
    
*   │ WeasyPrint Rendering Engine                                  │
    
*   │ ├─ Parse HTML + CSS                                          │
    
*   │ ├─ Load Noto Sans Sinhala web font                           │
    
*   │ ├─ Render with HarfBuzz text shaping                         │
    
*   │ ├─ Apply page breaks (@page, page-break-inside)              │
    
*   │ └─ Generate print-ready PDF                                  │
    
*   │ ↓                                                             │
    
*   │ PREVIEW PDF (draft watermark via CSS)                        │
    
*   │ ↓                                                             │
    
*   │ Coordinator Review → Approval                                │
    
*   │ ↓                                                             │
    
*   │ FINAL PDF (print-ready, no watermark)                        │
    
*   └──────────────────────────────────────────────────────────────┘
    

### **2.2 Directory Structure (Updated)**

*   /ssb-report-automation
    
*   │
    
*   ├── /data                          # Data sources
    
*   │   ├── master\_sheet.xlsx          # Master consolidation file
    
*   │   ├── /division\_templates        # 10 division Excel files
    
*   │   │   ├── division\_01.xlsx
    
*   │   │   ├── division\_02.xlsx
    
*   │   │   └── ...
    
*   │   └── /validation\_logs           # Data validation history
    
*   │
    
*   ├── /assets                        # Media files
    
*   │   ├── /images
    
*   │   │   ├── /events                # Monthly event photos (auto-processed)
    
*   │   │   │   ├── /2026\_01
    
*   │   │   │   ├── /2026\_02
    
*   │   │   │   └── ...
    
*   │   │   ├── /directors             # Board member photos
    
*   │   │   └── /signatures            # Digital signatures
    
*   │   ├── /fonts
    
*   │   │   ├── NotoSansSinhala-Regular.ttf
    
*   │   │   └── NotoSansSinhala-Bold.ttf
    
*   │   └── /css                       # NEW: CSS stylesheets
    
*   │       ├── print.css              # Print-specific styles
    
*   │       ├── layout.css             # Page layout
    
*   │       └── components.css         # Reusable components
    
*   │
    
*   ├── /src                           # Python source code
    
*   │   ├── main.py                    # Entry point
    
*   │   ├── data\_loader.py             # Excel → JSON extraction
    
*   │   ├── data\_validator.py          # Validation rules
    
*   │   ├── image\_processor.py         # Auto-crop, resize
    
*   │   ├── chart\_generator.py         # Matplotlib charts
    
*   │   ├── html\_builder.py            # NEW: Jinja2 HTML generation
    
*   │   ├── pdf\_generator.py           # NEW: WeasyPrint PDF generation
    
*   │   └── config.py                  # Configuration settings
    
*   │
    
*   ├── /templates                     # NEW: HTML/CSS templates
    
*   │   ├── base.html                  # Base template with header/footer
    
*   │   ├── cover\_page.html            # Cover page
    
*   │   ├── section\_scorecards.html    # Scorecards section
    
*   │   ├── section\_districts.html     # District performance
    
*   │   ├── section\_board.html         # Board of directors
    
*   │   ├── section\_events.html        # Events section
    
*   │   ├── section\_financials.html    # Financial tables
    
*   │   └── components/                # Reusable components
    
*   │       ├── event\_card.html
    
*   │       ├── table.html
    
*   │       └── chart.html
    
*   │
    
*   ├── /output                        # Generated files
    
*   │   ├── /html                      # NEW: Rendered HTML (for debugging)
    
*   │   ├── /preview                   # Draft PDFs with watermark
    
*   │   ├── /final                     # Approved final PDFs
    
*   │   └── /logs                      # Generation logs
    
*   │
    
*   └── requirements.txt               # Python dependencies (UPDATED)
    

**3\. HTML/CSS TEMPLATE STRUCTURE (NEW SECTION)**
-------------------------------------------------

### **3.1 Base Template with Print CSS**

**File:** /templates/base.html

*       
    
*       {{ report\_title }}
    

*       </div></li><li class="slate-li"><div style="position:relative">        /\* Import Sinhala font from Google Fonts or local \*/</div></li><li class="slate-li"><div style="position:relative">        @font-face {</div></li><li class="slate-li"><div style="position:relative">            font-family: &#x27;Noto Sans Sinhala&#x27;;</div></li><li class="slate-li"><div style="position:relative">            src: url(&#x27;{{ font\_path\_regular }}&#x27;) format(&#x27;truetype&#x27;);</div></li><li class="slate-li"><div style="position:relative">            font-weight: normal;</div></li><li class="slate-li"><div style="position:relative">            font-style: normal;</div></li><li class="slate-li"><div style="position:relative">        }</div></li><li class="slate-li"><div style="position:relative">        </div></li><li class="slate-li"><div style="position:relative">        @font-face {</div></li><li class="slate-li"><div style="position:relative">            font-family: &#x27;Noto Sans Sinhala&#x27;;</div></li><li class="slate-li"><div style="position:relative">            src: url(&#x27;{{ font\_path\_bold }}&#x27;) format(&#x27;truetype&#x27;);</div></li><li class="slate-li"><div style="position:relative">            font-weight: bold;</div></li><li class="slate-li"><div style="position:relative">            font-style: normal;</div></li><li class="slate-li"><div style="position:relative">        }</div></li><li class="slate-li"><div style="position:relative">        </div></li><li class="slate-li"><div style="position:relative">        /\* Page setup for print \*/</div></li><li class="slate-li"><div style="position:relative">        @page {</div></li><li class="slate-li"><div style="position:relative">            size: A4;</div></li><li class="slate-li"><div style="position:relative">            margin: 2.54cm;</div></li><li class="slate-li"><div style="position:relative">            </div></li><li class="slate-li"><div style="position:relative">            @top-center {</div></li><li class="slate-li"><div style="position:relative">                content: "{{ organization\_name }}";</div></li><li class="slate-li"><div style="position:relative">                font-family: &#x27;Noto Sans Sinhala&#x27;, sans-serif;</div></li><li class="slate-li"><div style="position:relative">                font-size: 10pt;</div></li><li class="slate-li"><div style="position:relative">                color: #666;</div></li><li class="slate-li"><div style="position:relative">            }</div></li><li class="slate-li"><div style="position:relative">            </div></li><li class="slate-li"><div style="position:relative">            @bottom-right {</div></li><li class="slate-li"><div style="position:relative">                content: "පිටුව " counter(page);</div></li><li class="slate-li"><div style="position:relative">                font-family: &#x27;Noto Sans Sinhala&#x27;, sans-serif;</div></li><li class="slate-li"><div style="position:relative">                font-size: 9pt;</div></li><li class="slate-li"><div style="position:relative">            }</div></li><li class="slate-li"><div style="position:relative">        }</div></li><li class="slate-li"><div style="position:relative">        </div></li><li class="slate-li"><div style="position:relative">        /\* First page (cover) - no header/footer \*/</div></li><li class="slate-li"><div style="position:relative">        @page:first {</div></li><li class="slate-li"><div style="position:relative">            @top-center { content: none; }</div></li><li class="slate-li"><div style="position:relative">            @bottom-right { content: none; }</div></li><li class="slate-li"><div style="position:relative">        }</div></li><li class="slate-li"><div style="position:relative">        </div></li><li class="slate-li"><div style="position:relative">        /\* Base typography \*/</div></li><li class="slate-li"><div style="position:relative">        body {</div></li><li class="slate-li"><div style="position:relative">            font-family: &#x27;Noto Sans Sinhala&#x27;, sans-serif;</div></li><li class="slate-li"><div style="position:relative">            font-size: 11pt;</div></li><li class="slate-li"><div style="position:relative">            line-height: 1.6;</div></li><li class="slate-li"><div style="position:relative">            color: #333;</div></li><li class="slate-li"><div style="position:relative">        }</div></li><li class="slate-li"><div style="position:relative">        </div></li><li class="slate-li"><div style="position:relative">        h1 {</div></li><li class="slate-li"><div style="position:relative">            font-size: 24pt;</div></li><li class="slate-li"><div style="position:relative">            color: #800000; /\* Deep Maroon \*/</div></li><li class="slate-li"><div style="position:relative">            margin-bottom: 12pt;</div></li><li class="slate-li"><div style="position:relative">            page-break-after: avoid;</div></li><li class="slate-li"><div style="position:relative">        }</div></li><li class="slate-li"><div style="position:relative">        </div></li><li class="slate-li"><div style="position:relative">        h2 {</div></li><li class="slate-li"><div style="position:relative">            font-size: 18pt;</div></li><li class="slate-li"><div style="position:relative">            color: #002366; /\* Royal Navy \*/</div></li><li class="slate-li"><div style="position:relative">            margin-top: 18pt;</div></li><li class="slate-li"><div style="position:relative">            margin-bottom: 10pt;</div></li><li class="slate-li"><div style="position:relative">            page-break-after: avoid;</div></li><li class="slate-li"><div style="position:relative">        }</div></li><li class="slate-li"><div style="position:relative">        </div></li><li class="slate-li"><div style="position:relative">        /\* Page break control \*/</div></li><li class="slate-li"><div style="position:relative">        .page-break {</div></li><li class="slate-li"><div style="position:relative">            page-break-before: always;</div></li><li class="slate-li"><div style="position:relative">        }</div></li><li class="slate-li"><div style="position:relative">        </div></li><li class="slate-li"><div style="position:relative">        .keep-together {</div></li><li class="slate-li"><div style="position:relative">            page-break-inside: avoid;</div></li><li class="slate-li"><div style="position:relative">        }</div></li><li class="slate-li"><div style="position:relative">        </div></li><li class="slate-li"><div style="position:relative">        /\* Watermark for preview mode \*/</div></li><li class="slate-li"><div style="position:relative">        {% if mode == &#x27;preview&#x27; %}</div></li><li class="slate-li"><div style="position:relative">        @page {</div></li><li class="slate-li"><div style="position:relative">            background: url(&#x27;data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400"><text x="50%" y="50%" font-size="60" fill="rgba(128,0,0,0.1)" text-anchor="middle" transform="rotate(-45 300 200)">DRAFT</text></svg>&#x27;) center center no-repeat;</div></li><li class="slate-li"><div style="position:relative">        }</div></li><li class="slate-li"><div style="position:relative">        {% endif %}</div></li><li class="slate-li"><div style="position:relative">        </div></li><li class="slate-li"><div style="position:relative">        /\* Tables \*/</div></li><li class="slate-li"><div style="position:relative">        table {</div></li><li class="slate-li"><div style="position:relative">            width: 100%;</div></li><li class="slate-li"><div style="position:relative">            border-collapse: collapse;</div></li><li class="slate-li"><div style="position:relative">            margin: 12pt 0;</div></li><li class="slate-li"><div style="position:relative">            page-break-inside: avoid; /\* Prevent table splitting \*/</div></li><li class="slate-li"><div style="position:relative">        }</div></li><li class="slate-li"><div style="position:relative">        </div></li><li class="slate-li"><div style="position:relative">        th {</div></li><li class="slate-li"><div style="position:relative">            background-color: #002366;</div></li><li class="slate-li"><div style="position:relative">            color: white;</div></li><li class="slate-li"><div style="position:relative">            padding: 8pt;</div></li><li class="slate-li"><div style="position:relative">            text-align: left;</div></li><li class="slate-li"><div style="position:relative">            font-weight: bold;</div></li><li class="slate-li"><div style="position:relative">        }</div></li><li class="slate-li"><div style="position:relative">        </div></li><li class="slate-li"><div style="position:relative">        td {</div></li><li class="slate-li"><div style="position:relative">            padding: 6pt 8pt;</div></li><li class="slate-li"><div style="position:relative">            border-bottom: 1px solid #DEE2E6;</div></li><li class="slate-li"><div style="position:relative">        }</div></li><li class="slate-li"><div style="position:relative">        </div></li><li class="slate-li"><div style="position:relative">        /\* Scorecards \*/</div></li><li class="slate-li"><div style="position:relative">        .scorecard-container {</div></li><li class="slate-li"><div style="position:relative">            display: flex;</div></li><li class="slate-li"><div style="position:relative">            justify-content: space-between;</div></li><li class="slate-li"><div style="position:relative">            margin: 20pt 0;</div></li><li class="slate-li"><div style="position:relative">            page-break-inside: avoid;</div></li><li class="slate-li"><div style="position:relative">        }</div></li><li class="slate-li"><div style="position:relative">        </div></li><li class="slate-li"><div style="position:relative">        .scorecard {</div></li><li class="slate-li"><div style="position:relative">            width: 30%;</div></li><li class="slate-li"><div style="position:relative">            padding: 15pt;</div></li><li class="slate-li"><div style="position:relative">            border-radius: 8pt;</div></li><li class="slate-li"><div style="position:relative">            text-align: center;</div></li><li class="slate-li"><div style="position:relative">        }</div></li><li class="slate-li"><div style="position:relative">        </div></li><li class="slate-li"><div style="position:relative">        .scorecard-recruitment {</div></li><li class="slate-li"><div style="position:relative">            background-color: #FFE5E5;</div></li><li class="slate-li"><div style="position:relative">            border: 2px solid #800000;</div></li><li class="slate-li"><div style="position:relative">        }</div></li><li class="slate-li"><div style="position:relative">        </div></li><li class="slate-li"><div style="position:relative">        .scorecard-collection {</div></li><li class="slate-li"><div style="position:relative">            background-color: #E5F0FF;</div></li><li class="slate-li"><div style="position:relative">            border: 2px solid #002366;</div></li><li class="slate-li"><div style="position:relative">        }</div></li><li class="slate-li"><div style="position:relative">        </div></li><li class="slate-li"><div style="position:relative">        .scorecard-premium {</div></li><li class="slate-li"><div style="position:relative">            background-color: #FFF8E5;</div></li><li class="slate-li"><div style="position:relative">            border: 2px solid #D4AF37;</div></li><li class="slate-li"><div style="position:relative">        }</div></li><li class="slate-li"><div style="position:relative">        </div></li><li class="slate-li"><div style="position:relative">        .scorecard-value {</div></li><li class="slate-li"><div style="position:relative">            font-size: 28pt;</div></li><li class="slate-li"><div style="position:relative">            font-weight: bold;</div></li><li class="slate-li"><div style="position:relative">            margin: 8pt 0;</div></li><li class="slate-li"><div style="position:relative">        }</div></li><li class="slate-li"><div style="position:relative">        </div></li><li class="slate-li"><div style="position:relative">        .scorecard-label {</div></li><li class="slate-li"><div style="position:relative">            font-size: 12pt;</div></li><li class="slate-li"><div style="position:relative">            color: #666;</div></li><li class="slate-li"><div style="position:relative">        }</div></li><li class="slate-li"><div style="position:relative">        </div></li><li class="slate-li"><div style="position:relative">        /\* Images \*/</div></li><li class="slate-li"><div style="position:relative">        img {</div></li><li class="slate-li"><div style="position:relative">            max-width: 100%;</div></li><li class="slate-li"><div style="position:relative">            height: auto;</div></li><li class="slate-li"><div style="position:relative">        }</div></li><li class="slate-li"><div style="position:relative">        </div></li><li class="slate-li"><div style="position:relative">        .event-photo {</div></li><li class="slate-li"><div style="position:relative">            width: 100%;</div></li><li class="slate-li"><div style="position:relative">            max-width: 800px;</div></li><li class="slate-li"><div style="position:relative">            height: auto;</div></li><li class="slate-li"><div style="position:relative">            margin: 10pt 0;</div></li><li class="slate-li"><div style="position:relative">        }</div></li><li class="slate-li"><div style="position:relative">        </div></li><li class="slate-li"><div style="position:relative">        .director-photo {</div></li><li class="slate-li"><div style="position:relative">            width: 150px;</div></li><li class="slate-li"><div style="position:relative">            height: 150px;</div></li><li class="slate-li"><div style="position:relative">            border-radius: 50%;</div></li><li class="slate-li"><div style="position:relative">            object-fit: cover;</div></li><li class="slate-li"><div style="position:relative">        }</div></li><li class="slate-li"><div style="position:relative">    
    

*       {% block content %}{% endblock %}
    

### **3.2 Events Section Template**

**File:** /templates/section\_events.html

*   {% extends "base.html" %}
    

*   {% block content %}
    

*       
    
    මාසික ක්‍රියාකාරකම්
    ===================
    

*       {% for event in events %}
    

*           
    
    {{ event.title }}
    -----------------
    
*           
    
    දිනය: {{ event.date\_si }}
    

*           {% if event.photo\_path %}
    
*           ![{{ event.title }}]({{ event.photo_path }})
    
*           {% endif %}
    

*           
    
    {{ event.description }}
    

*           
    
    ස්ථානය: {{ event.location }}
    
*           
    
    සහභාගිවූවන්: {{ event.participants }}
    

*       {% endfor %}
    

*   {% endblock %}
    

### **3.3 District Performance Table**

**File:** /templates/section\_districts.html

*   {% extends "base.html" %}
    

*   {% block content %}
    

*       
    
    දිස්ත්‍රික්ක කාර්ය සාධනය
    ========================
    

*       
    
    *               {% for district in districts %}
        
    
    *               {% endfor %}
        
    
    ශ්‍රේණිය
    
    දිස්ත්‍රික්කය
    
    බඳවා ගැනීම්
    
    වර්ධන %
    
    {{ district.rank }}
    
    {{ district.name\_si }}
    
    {{ district.count|format\_number }}
    
    {{ district.growth\_pct|format\_decimal }}%
    

*           
    
    දිස්ත්‍රික්ක සංසන්දනය
    ---------------------
    
*           ![District Performance Chart]({{ district_chart_path }})
    

*   {% endblock %}
    

**4\. PYTHON IMPLEMENTATION (UPDATED)**
---------------------------------------

### **4.1 HTML Builder Module**

**File:** /src/html\_builder.py

*   """
    
*   HTML generation using Jinja2 templates
    
*   """
    
*   from jinja2 import Environment, FileSystemLoader
    
*   import base64
    
*   from pathlib import Path
    
*   from config import BASE\_DIR, FONTS
    

*   class HTMLReportBuilder:
    
*       def \_\_init\_\_(self, mode='preview'):
    
*           """
    
*           Initialize HTML builder
    

*           Args:
    
*               mode: 'preview' or 'final'
    
*           """
    
*           self.mode = mode
    
*           self.template\_dir = BASE\_DIR / 'templates'
    

*           # Set up Jinja2 environment
    
*           self.env = Environment(
    
*               loader=FileSystemLoader(str(self.template\_dir)),
    
*               autoescape=True
    
*           )
    

*           # Register custom filters
    
*           self.env.filters\['format\_number'\] = self.format\_number
    
*           self.env.filters\['format\_decimal'\] = self.format\_decimal
    
*           self.env.filters\['embed\_image'\] = self.embed\_image
    

*       def format\_number(self, value):
    
*           """Format number with thousands separator"""
    
*           return f"{value:,}"
    

*       def format\_decimal(self, value, decimals=2):
    
*           """Format decimal with specified precision"""
    
*           return f"{value:.{decimals}f}"
    

*       def embed\_image(self, image\_path):
    
*           """Convert image to base64 data URI for embedding"""
    
*           if not Path(image\_path).exists():
    
*               return ""
    

*           with open(image\_path, 'rb') as f:
    
*               image\_data = base64.b64encode(f.read()).decode()
    

*           # Determine MIME type
    
*           ext = Path(image\_path).suffix.lower()
    
*           mime\_types = {
    
*               '.jpg': 'image/jpeg',
    
*               '.jpeg': 'image/jpeg',
    
*               '.png': 'image/png'
    
*           }
    
*           mime\_type = mime\_types.get(ext, 'image/jpeg')
    

*           return f"data:{mime\_type};base64,{image\_data}"
    

*       def build\_complete\_html(self, data):
    
*           """
    
*           Build complete HTML document from all sections
    

*           Args:
    
*               data: Dictionary containing all report data
    

*           Returns:
    
*               Complete HTML string
    
*           """
    
*           # Build individual sections
    
*           sections = \[\]
    

*           # Cover page
    
*           sections.append(self.render\_template('cover\_page.html', data))
    

*           # Scorecards
    
*           sections.append(self.render\_template('section\_scorecards.html', data))
    

*           # District performance
    
*           sections.append(self.render\_template('section\_districts.html', data))
    

*           # Board of directors
    
*           sections.append(self.render\_template('section\_board.html', data))
    

*           # Events
    
*           sections.append(self.render\_template('section\_events.html', data))
    

*           # Financial tables
    
*           sections.append(self.render\_template('section\_financials.html', data))
    

*           # Combine all sections
    
*           combined\_html = '\\n'.join(sections)
    

*           # Wrap in base template
    
*           base\_template = self.env.get\_template('base.html')
    
*           final\_html = base\_template.render(
    
*               content=combined\_html,
    
*               mode=self.mode,
    
*               font\_path\_regular=str(FONTS\['sinhala\_regular'\]\['path'\]),
    
*               font\_path\_bold=str(FONTS\['sinhala\_bold'\]\['path'\]),
    
*               \*\*data
    
*           )
    

*           return final\_html
    

*       def render\_template(self, template\_name, data):
    
*           """Render a single template with data"""
    
*           template = self.env.get\_template(template\_name)
    
*           return template.render(\*\*data)
    

### **4.2 PDF Generator Module (WeasyPrint)**

**File:** /src/pdf\_generator.py

*   """
    
*   PDF generation using WeasyPrint
    
*   """
    
*   from weasyprint import HTML, CSS
    
*   from weasyprint.text.fonts import FontConfiguration
    
*   from pathlib import Path
    
*   from config import OUTPUT\_DIR, FONTS, BASE\_DIR
    
*   import logging
    

*   logger = logging.getLogger(\_\_name\_\_)
    

*   class PDFGenerator:
    
*       def \_\_init\_\_(self, mode='preview'):
    
*           """
    
*           Initialize PDF generator
    

*           Args:
    
*               mode: 'preview' or 'final'
    
*           """
    
*           self.mode = mode
    
*           self.output\_dir = OUTPUT\_DIR / mode
    
*           self.output\_dir.mkdir(parents=True, exist\_ok=True)
    

*           # Font configuration for WeasyPrint
    
*           self.font\_config = FontConfiguration()
    

*       def generate\_pdf(self, html\_content, output\_filename):
    
*           """
    
*           Generate PDF from HTML content
    

*           Args:
    
*               html\_content: Complete HTML string
    
*               output\_filename: Name of output PDF file
    

*           Returns:
    
*               Path to generated PDF
    
*           """
    
*           output\_path = self.output\_dir / output\_filename
    

*           try:
    
*               # Additional CSS for fine-tuning
    
*               additional\_css = CSS(string=self.\_get\_additional\_css())
    

*               # Generate PDF
    
*               logger.info(f"Generating PDF in {self.mode} mode...")
    
*               HTML(string=html\_content, base\_url=str(BASE\_DIR)).write\_pdf(
    
*                   output\_path,
    
*                   stylesheets=\[additional\_css\],
    
*                   font\_config=self.font\_config
    
*               )
    

*               logger.info(f"✓ PDF generated: {output\_path}")
    
*               return output\_path
    

*           except Exception as e:
    
*               logger.error(f"PDF generation failed: {e}")
    
*               raise
    

*       def \_get\_additional\_css(self):
    
*           """
    
*           Additional CSS for print optimization
    
*           """
    
*           return """
    
*           @page {
    
*               size: A4 portrait;
    
*               margin: 2.54cm;
    
*           }
    

*           /\* Ensure proper text rendering \*/
    
*           body {
    
*               -webkit-font-smoothing: antialiased;
    
*               -moz-osx-font-smoothing: grayscale;
    
*           }
    

*           /\* Prevent orphans/widows \*/
    
*           p {
    
*               orphans: 3;
    
*               widows: 3;
    
*           }
    

*           /\* Table row breaks \*/
    
*           tr {
    
*               page-break-inside: avoid;
    
*           }
    
*           """
    

*       def generate\_from\_file(self, html\_file\_path, output\_filename):
    
*           """
    
*           Generate PDF from HTML file
    

*           Args:
    
*               html\_file\_path: Path to HTML file
    
*               output\_filename: Name of output PDF file
    

*           Returns:
    
*               Path to generated PDF
    
*           """
    
*           with open(html\_file\_path, 'r', encoding='utf-8') as f:
    
*               html\_content = f.read()
    

*           return self.generate\_pdf(html\_content, output\_filename)
    

### **4.3 Updated Main Script**

**File:** /src/main.py

*   """
    
*   Main entry point for SSB Report Automation
    
*   """
    
*   import logging
    
*   from pathlib import Path
    
*   from datetime import datetime
    

*   from config import initialize\_system, OUTPUT\_DIR, LOGS\_DIR
    
*   from data\_loader import load\_master\_sheet
    
*   from data\_validator import validate\_data
    
*   from image\_processor import process\_all\_event\_images
    
*   from chart\_generator import generate\_all\_charts
    
*   from html\_builder import HTMLReportBuilder
    
*   from pdf\_generator import PDFGenerator
    
*   from cli\_config import parse\_arguments
    

*   \# Set up logging
    
*   logging.basicConfig(
    
*       level=logging.INFO,
    
*       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    
*       handlers=\[
    
*           logging.FileHandler(LOGS\_DIR / 'generation.log'),
    
*           logging.StreamHandler()
    
*       \]
    
*   )
    
*   logger = logging.getLogger(\_\_name\_\_)
    

*   def main():
    
*       """Main execution flow"""
    
*       # Parse command-line arguments
    
*       args = parse\_arguments()
    

*       logger.info(f"=== SSB Report Generation Started ===")
    
*       logger.info(f"Month: {args.month}")
    
*       logger.info(f"Mode: {args.mode}")
    

*       # Initialize system
    
*       if not initialize\_system():
    
*           logger.error("System initialization failed")
    
*           return 1
    

*       # Step 1: Load data from Excel
    
*       logger.info("Step 1: Loading data from master Excel...")
    
*       data = load\_master\_sheet(args.month)
    

*       # Step 2: Validate data
    
*       if not args.skip\_validation:
    
*           logger.info("Step 2: Validating data...")
    
*           errors = validate\_data(data)
    

*           if errors:
    
*               logger.error(f"Validation failed with {len(errors)} errors:")
    
*               for error in errors:
    
*                   logger.error(f"  - {error}")
    

*               # Write validation report
    
*               validation\_report = LOGS\_DIR / f"validation\_report\_{args.month}.txt"
    
*               with open(validation\_report, 'w', encoding='utf-8') as f:
    
*                   f.write(f"Validation Report: {args.month}\\n")
    
*                   f.write(f"Generated: {datetime.now()}\\n\\n")
    
*                   f.write(f"Total Errors: {len(errors)}\\n\\n")
    
*                   for error in errors:
    
*                       f.write(f"- {error}\\n")
    

*               logger.info(f"Validation report saved: {validation\_report}")
    

*               if args.validate\_only:
    
*                   return 0
    
*               else:
    
*                   logger.error("Fix validation errors before generating PDF")
    
*                   return 1
    

*       if args.validate\_only:
    
*           logger.info("Validation passed. Exiting (--validate-only)")
    
*           return 0
    

*       # Step 3: Process images
    
*       if not args.skip\_images:
    
*           logger.info("Step 3: Processing images...")
    
*           process\_all\_event\_images(data\['events'\])
    

*       # Step 4: Generate charts
    
*       logger.info("Step 4: Generating charts...")
    
*       chart\_paths = generate\_all\_charts(data)
    
*       data\['chart\_paths'\] = chart\_paths
    

*       # Step 5: Build HTML
    
*       logger.info("Step 5: Building HTML from templates...")
    
*       html\_builder = HTMLReportBuilder(mode=args.mode)
    
*       html\_content = html\_builder.build\_complete\_html(data)
    

*       # Save HTML for debugging (optional)
    
*       html\_output\_dir = OUTPUT\_DIR / 'html'
    
*       html\_output\_dir.mkdir(parents=True, exist\_ok=True)
    
*       html\_file = html\_output\_dir / f"Report\_{args.month}\_{args.mode.upper()}.html"
    
*       with open(html\_file, 'w', encoding='utf-8') as f:
    
*           f.write(html\_content)
    
*       logger.info(f"HTML saved: {html\_file}")
    

*       # Step 6: Generate PDF
    
*       logger.info("Step 6: Generating PDF with WeasyPrint...")
    
*       pdf\_generator = PDFGenerator(mode=args.mode)
    
*       pdf\_filename = f"Report\_{args.month}\_{args.mode.upper()}.pdf"
    

*       pdf\_path = pdf\_generator.generate\_pdf(html\_content, pdf\_filename)
    

*       logger.info(f"\\n{'='\*60}")
    
*       logger.info(f"✓ PDF GENERATION COMPLETE")
    
*       logger.info(f"{'='\*60}")
    
*       logger.info(f"Output: {pdf\_path}")
    
*       logger.info(f"Mode: {args.mode.upper()}")
    
*       logger.info(f"{'='\*60}\\n")
    

*       return 0
    

*   if \_\_name\_\_ == '\_\_main\_\_':
    
*       exit(main())
    

**5\. SINHALA FONT HANDLING (CRITICAL - UPDATED)**
--------------------------------------------------

### **5.1 Font Configuration**

**Required Fonts:**

*   Noto Sans Sinhala (Google Fonts - free, Unicode-compliant)
    
*   Download: https://fonts.google.com/noto/specimen/Noto+Sans+Sinhala
    

**WeasyPrint Font Loading:**

*   \# WeasyPrint automatically handles fonts via CSS @font-face
    
*   \# No manual font registration needed
    

**CSS Font Declaration:**

*   @font-face {
    
*       font-family: 'Noto Sans Sinhala';
    
*       src: url('/assets/fonts/NotoSansSinhala-Regular.ttf') format('truetype');
    
*       font-weight: normal;
    
*       font-style: normal;
    
*   }
    

*   @font-face {
    
*       font-family: 'Noto Sans Sinhala';
    
*       src: url('/assets/fonts/NotoSansSinhala-Bold.ttf') format('truetype');
    
*       font-weight: bold;
    
*       font-style: normal;
    
*   }
    

*   body {
    
*       font-family: 'Noto Sans Sinhala', sans-serif;
    
*   }
    

### **5.2 Text Shaping (Automatic with WeasyPrint)**

WeasyPrint uses **Pango + HarfBuzz** for text rendering:

*   ✅ Automatic handling of complex scripts (Sinhala, Tamil, etc.)
    
*   ✅ Proper ligature rendering
    
*   ✅ Correct combining character placement
    
*   ✅ Bidirectional text support (if needed)
    

**No manual intervention required** - just use Unicode text in HTML templates.

### **5.3 Testing Sinhala Rendering**

*   \# test\_sinhala\_rendering.py
    
*   from weasyprint import HTML
    

*   html\_content = """
    

*       
    
*       </div></li><li class="slate-li"><div style="position:relative">        @font-face {</div></li><li class="slate-li"><div style="position:relative">            font-family: &#x27;Noto Sans Sinhala&#x27;;</div></li><li class="slate-li"><div style="position:relative">            src: url(&#x27;assets/fonts/NotoSansSinhala-Regular.ttf&#x27;);</div></li><li class="slate-li"><div style="position:relative">        }</div></li><li class="slate-li"><div style="position:relative">        body {</div></li><li class="slate-li"><div style="position:relative">            font-family: &#x27;Noto Sans Sinhala&#x27;, sans-serif;</div></li><li class="slate-li"><div style="position:relative">            font-size: 14pt;</div></li><li class="slate-li"><div style="position:relative">        }</div></li><li class="slate-li"><div style="position:relative">    
    

*       
    
    ශ්‍රී ලංකා සමාජ ආරක්ෂණ මණ්ඩලය
    =============================
    
*       
    
    මාසික කාර්ය සාධන වාර්තාව - 2026 පෙබරවාරි
    
*       
    
    බඳවා ගැනීම්: 66,977
    
*       
    
    එකතුව: රු. මිලියන 934.71
    

*   """
    

*   HTML(string=html\_content).write\_pdf('test\_sinhala.pdf')
    
*   print("✓ Test PDF generated: test\_sinhala.pdf")
    

**6\. PERFORMANCE OPTIMIZATION (UPDATED)**
------------------------------------------

### **6.1 Expected Generation Time**

With WeasyPrint:

*   **50-page report:** 20-30 seconds
    
*   **Breakdown:**
    
    *   Excel reading: 2 seconds
        
    *   Chart generation: 5 seconds
        
    *   Image processing: 3 seconds
        
    *   HTML generation: 2 seconds
        
    *   PDF rendering (WeasyPrint): 15-18 seconds
        

**Optimization Techniques:**

1.  **Embed Images as Base64:** Faster than file references
    

*   def embed\_image(image\_path):
    
*       with open(image\_path, 'rb') as f:
    
*           data = base64.b64encode(f.read()).decode()
    
*       return f"data:image/jpeg;base64,{data}"
    

1.  **Cache Chart Generation:**
    

*   \# Generate charts only if data changed
    
*   chart\_cache\_key = hashlib.md5(str(data).encode()).hexdigest()
    
*   if not chart\_exists(chart\_cache\_key):
    
*       generate\_charts(data)
    

1.  **Minimize CSS:** Inline critical CSS, remove unused styles
    
2.  **Use PNG for Charts:** Better compression than JPEG for charts
    

**7\. INSTALLATION & DEPENDENCIES (UPDATED)**
---------------------------------------------

### **7.1 Requirements File**

**File:** requirements.txt

*   \# Core PDF Generation (UPDATED)
    
*   weasyprint==61.0
    
*   cairocffi==1.6.1
    
*   tinycss2==1.2.1
    
*   cssselect2==0.7.0
    

*   \# Excel Processing
    
*   openpyxl==3.1.2
    

*   \# Image Processing
    
*   Pillow==10.1.0
    
*   pillow-heif==0.14.0
    

*   \# Charts
    
*   matplotlib==3.8.2
    

*   \# Templating
    
*   jinja2==3.1.2
    

*   \# Utilities
    
*   python-dateutil==2.8.2
    

### **7.2 Installation**

*   \# Install Python 3.9+
    
*   \# Install system dependencies (for WeasyPrint)
    

*   \# For Ubuntu/Debian:
    
*   sudo apt-get install python3-pip python3-cffi python3-brotli \\
    
*       libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz-subset0
    

*   \# For macOS:
    
*   brew install python cairo pango gdk-pixbuf libffi
    

*   \# For Windows:
    
*   \# Download GTK3 runtime from https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer
    

*   \# Install Python packages
    
*   pip install -r requirements.txt
    

**8\. CRITICAL SUCCESS FACTORS (UPDATED)**
------------------------------------------

### **✅ Do's**

1.  **Test Sinhala rendering early** - generate test PDF with sample text
    
2.  **Use semantic HTML** - proper
    
    , ,
    
    tags*   **Leverage CSS for layout** - use flexbox, grid for modern layouts
        
    *   **Validate HTML** - use W3C validator to catch errors
        
    *   **Always generate preview first** - never skip validation
        
    *   **Save intermediate HTML** - helps debug rendering issues
        
    
    ### **❌ Don'ts**
    
    1.  **Don't use inline styles excessively** - use CSS classes instead
        
    2.  **Don't skip font installation** - WeasyPrint requires system fonts
        
    3.  **Don't use JavaScript** - WeasyPrint doesn't execute JS
        
    4.  **Don't mix HTML entities with Unicode** - use Unicode directly
        
    5.  **Don't create overly complex HTML** - keep structure simple
        

    
    **10\. TROUBLESHOOTING (UPDATED)**
    ----------------------------------
    
    ### **Issue 1: "Sinhala text shows boxes/broken characters"**
    
    **Cause:** Font not loaded properly **Fix:**
    
    1.  Verify font file exists in /assets/fonts/
        
    2.  Check @font-face path in CSS is correct (use absolute paths)
        
    3.  Test font installation: fc-list | grep Sinhala
        
    
    ### **Issue 2: "PDF generation fails with 'Cairo' error"**
    
    **Cause:** System dependencies missing **Fix:**
    
    *   \# Ubuntu/Debian
        
    *   sudo apt-get install libcairo2 libpango-1.0-0 libpangocairo-1.0-0
        
    
    *   \# macOS
        
    *   brew install cairo pango
        
    
    ### **Issue 3: "Tables split across pages incorrectly"**
    
    **Cause:** Missing page-break-inside CSS **Fix:**
    
    *   table {
        
    *       page-break-inside: avoid;
        
    *   }
        
    *   tr {
        
    *       page-break-inside: avoid;
        
    *   }
        
    
    ### **Issue 4: "Images don't appear in PDF"**
    
    **Cause:** Incorrect image paths or base64 encoding **Fix:**
    
    *   \# Use absolute paths or base64 embedding
        
    *   ![](file:///absolute/path/to/image.jpg)
        
    *   \# OR
        
    *   ![](data:image/jpeg;base64,{{ image_data }})
        
    

    
    **Document Control**
    --------------------
    
    *   **Version:** 3.0 (WeasyPrint Revision)
        
    *   **Last Updated:** February 9, 2026
        
    *   **Major Changes:** WeasyPrint-based PDF generation with Jinja2 HTML templating
        
    *   **Next Review:** After pilot implementation
        
    *   **Owner:** SSB IT Department
