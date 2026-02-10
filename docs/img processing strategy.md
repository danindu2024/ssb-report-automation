**Image Processing Strategy Document**
======================================

**Version:** 1.0 **Date:** February 7, 2026 **Purpose:** Automated image handling for SSB monthly reports

**1\. PROBLEM STATEMENT**
-------------------------

### **Current Challenges (From Your Requirements)**

1.  **Variable Photo Sizes:** Event photos submitted in different dimensions (portrait, landscape, various resolutions)
    
2.  **Manual Cropping Needed:** Currently requires manual editing to fit report layout
    
3.  **Quality Inconsistency:** Mix of high-res and low-res images
    
4.  **Naming Chaos:** No standardized file naming convention
    
5.  **Storage Inefficiency:** Large original files embedded in PDFs
    

**2\. AUTOMATED SOLUTION ARCHITECTURE**
---------------------------------------

### **2.1 Processing Pipeline**

┌─────────────────────────────────────────────────────────────┐

│  STAGE 1: RAW IMAGE UPLOAD                                  │

├─────────────────────────────────────────────────────────────┤

│  Division uploads event photos to shared folder             │

│  Location: /assets/images/events/raw/\[FOLDER\_NAME\]/         │

│  Files: Any size, any format (JPG/PNG/HEIC)                 │

└─────────────────────────────────────────────────────────────┘

                          ↓

┌─────────────────────────────────────────────────────────────┐

│  STAGE 2: AUTO-DETECTION & VALIDATION                       │

├─────────────────────────────────────────────────────────────┤

│  Python script scans folder                                 │

│  - Validates file format (converts HEIC→JPG if needed)      │

│  - Checks minimum resolution (1024px minimum width)         │

│  - Renames files sequentially (01.jpg, 02.jpg, ...)         │

└─────────────────────────────────────────────────────────────┘

                          ↓

┌─────────────────────────────────────────────────────────────┐

│  STAGE 3: INTELLIGENT AUTO-CROP                             │

├─────────────────────────────────────────────────────────────┤

│  Face Detection (optional, for people-focused events)       │

│  - Uses OpenCV to detect faces                              │

│  - Centers crop on detected faces                           │

│                                                              │

│  Smart Center Crop (default)                                │

│  - Analyzes image composition                               │

│  - Crops to standard aspect ratio (4:3 for report)          │

│  - Preserves subject matter in center                       │

└─────────────────────────────────────────────────────────────┘

                          ↓

┌─────────────────────────────────────────────────────────────┐

│  STAGE 4: STANDARDIZED RESIZE                               │

├─────────────────────────────────────────────────────────────┤

│  Target Dimensions (for report embedding):                  │

│  - Event photos: 800×600px (4:3 ratio)                      │

│  - Director photos: 400×400px (1:1 ratio, square)           │

│  - Signature images: 300×100px (3:1 ratio)                  │

│                                                              │

│  Resolution: 300 DPI (print quality)                        │

└─────────────────────────────────────────────────────────────┘

                          ↓

┌─────────────────────────────────────────────────────────────┐

│  STAGE 5: OPTIMIZATION & COMPRESSION                        │

├─────────────────────────────────────────────────────────────┤

│  JPEG Optimization:                                         │

│  - Quality: 85 (optimal balance)                            │

│  - Progressive encoding (faster web loading)                │

│  - Strip EXIF metadata (reduce file size)                   │

│                                                              │

│  Result: 50-70% file size reduction, no visible quality loss│

└─────────────────────────────────────────────────────────────┘

                          ↓

┌─────────────────────────────────────────────────────────────┐

│  STAGE 6: PROCESSED OUTPUT                                  │

├─────────────────────────────────────────────────────────────┤

│  Location: /assets/images/events/processed/\[FOLDER\]/        │

│  Files: Standardized dimensions, optimized size             │

│  Ready for: Direct PDF embedding                            │

└─────────────────────────────────────────────────────────────┘

**3\. IMPLEMENTATION DETAILS**
------------------------------

### **3.1 Python Processing Script**

**File:** /src/image\_processor.py

from PIL import Image, ImageOps, ExifTags

import os

from pathlib import Path

\# Image dimension targets

IMAGE\_SPECS = {

    "event": {"width": 800, "height": 600, "aspect": 4/3},

    "director": {"width": 400, "height": 400, "aspect": 1/1},

    "signature": {"width": 300, "height": 100, "aspect": 3/1}

}

def process\_event\_photos(event\_folder\_name):

    """

    Batch process all photos in an event folder

    Args:

        event\_folder\_name: e.g., "2026-02-18\_AWARDS-KUR"

    Returns:

        List of processed file paths

    """

    raw\_dir = Path(f"assets/images/events/raw/{event\_folder\_name}")

    processed\_dir = Path(f"assets/images/events/processed/{event\_folder\_name}")

    processed\_dir.mkdir(parents=True, exist\_ok=True)

    processed\_files = \[\]

    photo\_count = 1

    for img\_file in sorted(raw\_dir.glob("\*")):

        if img\_file.suffix.lower() in \['.jpg', '.jpeg', '.png', '.heic'\]:

            try:

                # Step 1: Load and auto-rotate (fix phone orientation)

                img = Image.open(img\_file)

                img = auto\_rotate(img)

                # Step 2: Intelligent crop to 4:3 ratio

                img\_cropped = smart\_crop(img, IMAGE\_SPECS\["event"\]\["aspect"\])

                # Step 3: Resize to standard dimensions

                img\_resized = img\_cropped.resize(

                    (IMAGE\_SPECS\["event"\]\["width"\], IMAGE\_SPECS\["event"\]\["height"\]),

                    Image.Resampling.LANCZOS  # High-quality downsampling

                )

                # Step 4: Optimize and save

                output\_file = processed\_dir / f"{photo\_count:02d}.jpg"

                img\_resized.save(

                    output\_file,

                    "JPEG",

                    quality=85,

                    optimize=True,

                    progressive=True

                )

                processed\_files.append(str(output\_file))

                photo\_count += 1

            except Exception as e:

                print(f"Error processing {img\_file.name}: {e}")

    return processed\_files

def auto\_rotate(img):

    """

    Fix image orientation based on EXIF data (from phone cameras)

    """

    try:

        for orientation in ExifTags.TAGS.keys():

            if ExifTags.TAGS\[orientation\] == 'Orientation':

                break

        exif = img.\_getexif()

        if exif is not None:

            orientation\_value = exif.get(orientation)

            if orientation\_value == 3:

                img = img.rotate(180, expand=True)

            elif orientation\_value == 6:

                img = img.rotate(270, expand=True)

            elif orientation\_value == 8:

                img = img.rotate(90, expand=True)

    except:

        pass  # No EXIF data, use image as-is

    return img

def smart\_crop(img, target\_aspect\_ratio):

    """

    Crop image to target aspect ratio, preserving center content

    Args:

        img: PIL Image object

        target\_aspect\_ratio: e.g., 4/3 for landscape, 1/1 for square

    Returns:

        Cropped PIL Image

    """

    current\_width, current\_height = img.size

    current\_aspect = current\_width / current\_height

    if abs(current\_aspect - target\_aspect\_ratio) < 0.01:

        # Already correct ratio, no crop needed

        return img

    if current\_aspect > target\_aspect\_ratio:

        # Image is wider than target → crop width

        new\_width = int(current\_height \* target\_aspect\_ratio)

        left = (current\_width - new\_width) // 2

        return img.crop((left, 0, left + new\_width, current\_height))

    else:

        # Image is taller than target → crop height

        new\_height = int(current\_width / target\_aspect\_ratio)

        top = (current\_height - new\_height) // 2

        return img.crop((0, top, current\_width, top + new\_height))

def process\_director\_photos():

    """

    Process board member headshots to square format

    """

    raw\_dir = Path("assets/images/directors/raw")

    processed\_dir = Path("assets/images/directors/processed")

    processed\_dir.mkdir(parents=True, exist\_ok=True)

    for img\_file in raw\_dir.glob("DIRECTOR\_\*.jpg"):

        img = Image.open(img\_file)

        img = auto\_rotate(img)

        # Crop to square (1:1 aspect ratio)

        img\_cropped = smart\_crop(img, 1.0)

        # Resize to standard dimensions

        img\_resized = img\_cropped.resize((400, 400), Image.Resampling.LANCZOS)

        # Save optimized

        output\_file = processed\_dir / img\_file.name

        img\_resized.save(output\_file, "JPEG", quality=90, optimize=True)

\# Advanced: Face detection for people-focused cropping

def face\_detection\_crop(img, target\_aspect\_ratio):

    """

    OPTIONAL: Use OpenCV to detect faces and center crop on them

    Better for event photos with people

    Requires: pip install opencv-python

    """

    import cv2

    import numpy as np

    # Convert PIL to OpenCV format

    img\_cv = cv2.cvtColor(np.array(img), cv2.COLOR\_RGB2BGR)

    # Load face detection model

    face\_cascade = cv2.CascadeClassifier(

        cv2.data.haarcascades + 'haarcascade\_frontalface\_default.xml'

    )

    # Detect faces

    faces = face\_cascade.detectMultiScale(img\_cv, scaleFactor=1.1, minNeighbors=5)

    if len(faces) > 0:

        # Find center point of all detected faces

        face\_centers = \[(x + w//2, y + h//2) for (x, y, w, h) in faces\]

        avg\_x = sum(x for x, y in face\_centers) // len(face\_centers)

        avg\_y = sum(y for x, y in face\_centers) // len(face\_centers)

        # Crop centered on face(s)

        width, height = img.size

        target\_width = int(height \* target\_aspect\_ratio)

        left = max(0, avg\_x - target\_width // 2)

        right = min(width, left + target\_width)

        return img.crop((left, 0, right, height))

    else:

        # No faces detected, fallback to center crop

        return smart\_crop(img, target\_aspect\_ratio)

**4\. FOLDER STRUCTURE & NAMING CONVENTIONS**
---------------------------------------------

### **4.1 Directory Organization**

/assets/images/

│

├── /events/

│   ├── /raw/                          # Original uploads (divisions upload here)

│   │   ├── /2026-01-28\_MINISTER/

│   │   │   ├── IMG\_1234.jpg          # Original file names (any format)

│   │   │   ├── IMG\_1235.jpg

│   │   │   └── photo\_event.png

│   │   ├── /2026-02-18\_AWARDS-KUR/

│   │   │   ├── DSC\_0001.jpg

│   │   │   └── ...

│   │   └── /2026-02-25\_TRAINING/

│   │       └── ...

│   │

│   └── /processed/                    # Auto-generated (script output)

│       ├── /2026-01-28\_MINISTER/

│       │   ├── 01.jpg                 # Standardized naming

│       │   ├── 02.jpg

│       │   └── 03.jpg

│       ├── /2026-02-18\_AWARDS-KUR/

│       │   ├── 01.jpg

│       │   └── ...

│       └── /2026-02-25\_TRAINING/

│           └── ...

│

├── /directors/

│   ├── /raw/

│   │   ├── DIRECTOR\_DISSANAYAKE.jpg

│   │   ├── DIRECTOR\_HERATH.jpg

│   │   └── ...

│   └── /processed/

│       ├── DIRECTOR\_DISSANAYAKE.jpg   # Square cropped, 400×400

│       └── ...

│

└── /signatures/

    ├── /raw/

    │   ├── SIGNATURE\_CHAIRMAN.png

    │   └── ...

    └── /processed/

        ├── SIGNATURE\_CHAIRMAN.png     # Transparent background, 300×100

        └── ...

### **4.2 Naming Convention Rules**

**Event Folder Names:**

Format: YYYY-MM-DD\_EVENT-CODE

Rules:

\- Date: ISO format (YYYY-MM-DD)

\- Event code: All caps, hyphens for spaces, max 20 chars

\- No special characters except hyphen

Examples:

✓ 2026-02-18\_AWARDS-KUR

✓ 2026-03-10\_MINISTER-VISIT

✗ 2026-2-18\_awards (date format wrong, lowercase)

✗ 2026-02-18\_සම්මාන උළෙල (Sinhala not allowed in folder names)

**Individual Photo Files (after processing):**

Format: NN.jpg (where NN = sequential number, zero-padded)

Examples:

01.jpg, 02.jpg, ..., 15.jpg

Rationale: 

\- Simple, unambiguous ordering

\- No dependency on original camera filenames

\- Easy to reference in Excel (PHOTO\_COUNT column)

**5\. QUALITY VALIDATION**
--------------------------

### **5.1 Pre-Processing Checks**

**Script validates before processing:**

def validate\_raw\_images(event\_folder):

    """

    Check if uploaded images meet minimum requirements

    """

    errors = \[\]

    raw\_dir = Path(f"assets/images/events/raw/{event\_folder}")

    for img\_file in raw\_dir.glob("\*"):

        if img\_file.suffix.lower() in \['.jpg', '.jpeg', '.png'\]:

            img = Image.open(img\_file)

            width, height = img.size

            # Check 1: Minimum resolution

            if width < 1024 or height < 768:

                errors.append(f"{img\_file.name}: Too low resolution ({width}×{height}). Minimum: 1024×768")

            # Check 2: Aspect ratio not too extreme

            aspect = width / height

            if aspect < 0.5 or aspect > 2.5:

                errors.append(f"{img\_file.name}: Unusual aspect ratio ({aspect:.2f}). May not crop well.")

            # Check 3: File size reasonable (not corrupted)

            file\_size\_mb = img\_file.stat().st\_size / (1024 \* 1024)

            if file\_size\_mb < 0.1:

                errors.append(f"{img\_file.name}: File suspiciously small ({file\_size\_mb:.2f}MB). May be corrupted.")

    return errors

**Validation Report:**

IMAGE VALIDATION: 2026-02-18\_AWARDS-KUR

─────────────────────────────────────────

✓ DSC\_0001.jpg: 3000×2000 (OK)

✗ DSC\_0002.jpg: 800×600 (FAIL - Resolution too low)

✓ DSC\_0003.jpg: 4000×3000 (OK)

⚠ IMG\_1234.jpg: 5000×1000 (WARNING - Extreme aspect ratio)

ACTION REQUIRED:

\- Replace DSC\_0002.jpg with higher resolution version

\- Review IMG\_1234.jpg (panorama? May need manual crop)

### **5.2 Post-Processing Quality Check**

**Visual proof sheet generation:**

from weasyprint import HTML, CSS

from jinja2 import Template

from datetime import datetime

\# Ensure you have these imports at the top of your file:

\# from pathlib import Path

\# from config import PROOF\_SHEETS\_DIR, EVENTS\_PROCESSED\_DIR

def generate\_proof\_sheet(event\_folder):

    """

    Create a contact sheet PDF showing all processed photos for review.

    """

    # 1. Setup Paths

    processed\_dir = EVENTS\_PROCESSED\_DIR / event\_folder

    output\_path = PROOF\_SHEETS\_DIR / f"{event\_folder}\_PROOF.pdf"

    # Ensure output directory exists

    PROOF\_SHEETS\_DIR.mkdir(parents=True, exist\_ok=True)

    # 2. Gather Images

    if not processed\_dir.exists():

        print(f"Error: Processed folder not found: {processed\_dir}")

        return

    images = sorted(\[

        img for img in processed\_dir.glob("\*.jpg")

    \])

    if not images:

        print(f"Warning: No images found in {processed\_dir}")

        return

    # 3. Define HTML Template (Embedded for simplicity)

    # Uses CSS Grid for a clean 3-column layout

    html\_template = """

        </p><p class="slate-paragraph">            @page { </p><p class="slate-paragraph">                size: A4; </p><p class="slate-paragraph">                margin: 1.5cm; </p><p class="slate-paragraph">                @bottom-right { content: "Page " counter(page); font-size: 9pt; }</p><p class="slate-paragraph">            }</p><p class="slate-paragraph">            body { </p><p class="slate-paragraph">                font-family: sans-serif; </p><p class="slate-paragraph">                color: #333;</p><p class="slate-paragraph">            }</p><p class="slate-paragraph">            .header { </p><p class="slate-paragraph">                text-align: center; </p><p class="slate-paragraph">                margin-bottom: 20px; </p><p class="slate-paragraph">                border-bottom: 2px solid #002366; </p><p class="slate-paragraph">                padding-bottom: 10px;</p><p class="slate-paragraph">            }</p><p class="slate-paragraph">            h1 { color: #002366; font-size: 18pt; margin: 0; }</p><p class="slate-paragraph">            .meta { color: #666; font-size: 10pt; margin-top: 5px; }</p><p class="slate-paragraph">            </p><p class="slate-paragraph">            /\* Grid Layout \*/</p><p class="slate-paragraph">            .gallery { </p><p class="slate-paragraph">                display: flex; </p><p class="slate-paragraph">                flex-wrap: wrap; </p><p class="slate-paragraph">                gap: 15px; </p><p class="slate-paragraph">                justify-content: flex-start;</p><p class="slate-paragraph">            }</p><p class="slate-paragraph">            .card { </p><p class="slate-paragraph">                width: 30%; /\* 3 columns approx \*/</p><p class="slate-paragraph">                border: 1px solid #eee; </p><p class="slate-paragraph">                padding: 5px; </p><p class="slate-paragraph">                box-sizing: border-box;</p><p class="slate-paragraph">                page-break-inside: avoid; /\* Prevent splitting images across pages \*/</p><p class="slate-paragraph">            }</p><p class="slate-paragraph">            img { </p><p class="slate-paragraph">                width: 100%; </p><p class="slate-paragraph">                height: auto; </p><p class="slate-paragraph">                display: block; </p><p class="slate-paragraph">                background: #f0f0f0;</p><p class="slate-paragraph">            }</p><p class="slate-paragraph">            .filename { </p><p class="slate-paragraph">                font-size: 9pt; </p><p class="slate-paragraph">                text-align: center; </p><p class="slate-paragraph">                margin-top: 5px; </p><p class="slate-paragraph">                font-family: monospace;</p><p class="slate-paragraph">                color: #444;</p><p class="slate-paragraph">            }</p><p class="slate-paragraph">        

Event Proof Sheet
=================

                **Event:** {{ event\_folder }} | 

                **Date:** {{ date }} | 

                **Count:** {{ images|length }} Photos

            {% for img in images %}

                ![]({{ img.as_uri() }})

{{ img.name }}

            {% endfor %}

    """

    # 4. Render HTML

    template = Template(html\_template)

    html\_content = template.render(

        event\_folder=event\_folder,

        images=images,

        date=datetime.now().strftime("%Y-%m-%d %H:%M")

    )

    # 5. Generate PDF

    try:

        print(f"Generating proof sheet for {event\_folder}...")

        HTML(string=html\_content).write\_pdf(output\_path)

        print(f"✓ Proof sheet saved: {output\_path}")

    except Exception as e:

        print(f"✗ Failed to generate proof sheet: {e}")

**6\. INTEGRATION WITH EXCEL**
------------------------------

### **6.1 Division Workflow (Simplified)**

**Step 1: Upload photos to shared folder**

*   Division creates folder: 2026-02-18\_AWARDS-KUR
    
*   Uploads photos with any filenames
    

**Step 2: Update Excel template**

*   In DIV\_05\_Events\_Template.xlsx:
    
    *   PHOTO\_FOLDER column: 2026-02-18\_AWARDS-KUR
        
    *   PHOTO\_COUNT: (leave blank, auto-counted by script)
        

**Step 3: Notify coordinator**

*   Email: "Division 05 uploaded photos for Feb 18 awards event"
    

### **6.2 Coordinator Workflow**

**Step 1: Run processing script**

python process\_images.py --event 2026-02-18\_AWARDS-KUR

**Output:**

Processing event: 2026-02-18\_AWARDS-KUR

─────────────────────────────────────────

Found 5 raw images

✓ Processed: 01.jpg (3000×2000 → 800×600, 2.1MB → 145KB)

✓ Processed: 02.jpg (4000×3000 → 800×600, 3.5MB → 160KB)

✓ Processed: 03.jpg (3500×2300 → 800×600, 2.8MB → 152KB)

✓ Processed: 04.jpg (3200×2400 → 800×600, 2.4MB → 148KB)

✓ Processed: 05.jpg (3800×2500 → 800×600, 3.1MB → 155KB)

Total size reduction: 13.9MB → 760KB (94.5% smaller)

Output: assets/images/events/processed/2026-02-18\_AWARDS-KUR/

Proof sheet: output/proof\_sheets/2026-02-18\_AWARDS-KUR\_PROOF.pdf

**Step 2: Review proof sheet**

*   Open 2026-02-18\_AWARDS-KUR\_PROOF.pdf
    
*   Verify all photos cropped correctly
    
*   If any photo needs manual adjustment, edit in /processed/ folder
    

**Step 3: Auto-update Excel**

\# Script automatically counts processed photos

photo\_count = len(list(Path(f"assets/images/events/processed/{event\_folder}").glob("\*.jpg")))

\# Updates master Excel

wb = openpyxl.load\_workbook("data/master\_sheet.xlsx")

sheet = wb\["DIV\_05\_EVENTS"\]

\# Find row for this event, update PHOTO\_COUNT column

sheet\["G8"\].value = photo\_count  # Example: row 8

wb.save("data/master\_sheet.xlsx")

\#### Integration with HTML Templates

For WeasyPrint, processed images can be embedded as base64:

\`\`\`python

import base64

def embed\_image\_for\_html(image\_path):

    """Convert processed image to base64 for HTML embedding"""

    with open(image\_path, 'rb') as f:

        image\_data = base64.b64encode(f.read()).decode()

    return f"data:image/jpeg;base64,{image\_data}"

\`\`\`

This eliminates file path issues and speeds up PDF generation.

**7\. SPECIAL CASES**
---------------------

### **7.1 Handling Different Orientations**

**Problem:** Mix of portrait and landscape photos in same event

**Solution:** Two processing modes

def process\_mixed\_orientation(event\_folder, orientation="auto"):

    """

    Auto-detect orientation and apply appropriate crop

    Args:

        orientation: "auto" | "landscape" | "portrait" | "square"

    """

    if orientation == "auto":

        # Detect majority orientation

        portrait\_count = 0

        landscape\_count = 0

        for img\_file in raw\_dir.glob("\*.jpg"):

            img = Image.open(img\_file)

            if img.width > img.height:

                landscape\_count += 1

            else:

                portrait\_count += 1

        # Use majority orientation for all photos (consistency)

        primary = "landscape" if landscape\_count >= portrait\_count else "portrait"

    else:

        primary = orientation

    # Process with detected orientation

    aspect\_ratio = 4/3 if primary == "landscape" else 3/4

    # ... (continue with smart\_crop)

### **7.2 Panorama Photos (Wide Shots)**

**Problem:** Venue panoramas (e.g., 5000×1000 pixels)

**Solution:** Special handling

def detect\_panorama(img):

    """Check if image is panoramic"""

    aspect = img.width / img.height

    return aspect > 2.5 or aspect < 0.4

def process\_panorama(img):

    """

    For panoramas, use different strategy:

    - Don't center crop (loses too much)

    - Instead, resize to fit width, allow height variation

    """

    target\_width = 800

    aspect = img.width / img.height

    target\_height = int(target\_width / aspect)

    return img.resize((target\_width, target\_height), Image.Resampling.LANCZOS)

### **7.3 Signatures & Transparent Backgrounds**

**Problem:** Chairman signature needs transparent background

**Solution:** PNG processing

def process\_signature(signature\_file):

    """

    Process signature images (preserve transparency)

    """

    img = Image.open(signature\_file).convert("RGBA")

    # Remove white background (make transparent)

    datas = img.getdata()

    new\_data = \[\]

    for item in datas:

        # Change all white (also shades of whites)

        if item\[0\] > 200 and item\[1\] > 200 and item\[2\] > 200:

            new\_data.append((255, 255, 255, 0))  # Transparent

        else:

            new\_data.append(item)

    img.putdata(new\_data)

    # Resize to standard signature dimensions

    img = img.resize((300, 100), Image.Resampling.LANCZOS)

    # Save as PNG (supports transparency)

    img.save("assets/images/signatures/processed/signature.png", "PNG")

**8\. BATCH PROCESSING**
------------------------

### **8.1 Process All Events at Once**

\# Command to process all pending events

python process\_images.py --batch --month 2026-02

**Script logic:**

def batch\_process\_month(month):

    """

    Process all event folders for a given month

    """

    master\_wb = openpyxl.load\_workbook("data/master\_sheet.xlsx")

    events\_sheet = master\_wb\["DIV\_05\_EVENTS"\]

    # Find all events for this month

    for row in events\_sheet.iter\_rows(min\_row=5):

        event\_date = row\[0\].value  # Column A: EVENT\_DATE

        photo\_folder = row\[5\].value  # Column F: PHOTO\_FOLDER

        if event\_date and event\_date.startswith(month):

            if photo\_folder and Path(f"assets/images/events/raw/{photo\_folder}").exists():

                print(f"\\nProcessing: {photo\_folder}")

                process\_event\_photos(photo\_folder)

            else:

                print(f"⚠ Warning: Photo folder missing for {event\_date}")

**9\. TROUBLESHOOTING**
-----------------------

### **Common Issues & Fixes**

**Issue**

**Cause**

**Solution**

"Image quality poor in PDF"

Over-compression (quality < 80)

Increase JPEG quality to 85-90

"People's heads cut off"

Auto-crop centering issue

Use face\_detection\_crop()

"Photos different sizes in PDF"

Aspect ratio mismatch

Verify all processed to same dimensions

"Script crashes on iPhone photos"

HEIC format not supported

Install pillow-heif: pip install pillow-heif

"Panorama photos look squished"

Standard crop on wide image

Use detect\_panorama() special handling

**10\. PERFORMANCE METRICS**
----------------------------

**Processing Speed (Tested on standard PC):**

*   1 event photo (3MB original): 0.8 seconds
    
*   10 photos batch: 6 seconds
    
*   Full month (50 photos): 30 seconds
    

**File Size Savings:**

*   Original uploads: ~3MB per photo
    
*   Processed output: ~150KB per photo
    
*   **Reduction: 95%**
    

**Quality Metrics:**

*   Print resolution: 300 DPI (industry standard)
    
*   PDF embedding size: Optimal (no unnecessary bloat)
    
*   Visual quality: No perceptible degradation vs. originals
    

**11\. FUTURE ENHANCEMENTS (Optional)**
---------------------------------------

### **Phase 2 Improvements**

1.  **Web Upload Interface:**
    
    *   Simple web form for divisions to upload photos
        
    *   Drag-and-drop, auto-naming
        
    *   Real-time preview of cropped result
        
2.  **AI-Powered Smart Crop:**
    
    *   Machine learning model to detect "interesting" regions
        
    *   Better than center crop for complex compositions
        
3.  **Automatic Captioning:**
    
    *   OCR on images with text (event banners)
        
    *   Auto-suggest event titles from detected text
        
4.  **Cloud Storage Integration:**
    
    *   Auto-sync with Google Drive
        
    *   Backup raw images to cloud
        

**Document Version:** 1.0 **Last Updated:** February 7, 2026 **Dependencies:** PIL/Pillow, OpenCV (optional)