"""
Chart Generation Engine for SSB Monthly Report Automation.
Creates standardized charts using Matplotlib with Sinhala font support.
Based on specs in reviced TDD.md and imp roadmap.md.
"""
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.ticker as ticker
from pathlib import Path
import os

from config import CHARTS_DIR, ASSETS_DIR

# --- Font setup ---
FONTS_DIR = ASSETS_DIR / "fonts"
SINHALA_REGULAR = FONTS_DIR / "NotoSansSinhala-Regular.ttf"
SINHALA_BOLD = FONTS_DIR / "NotoSansSinhala-Bold.ttf"

# Install fonts into matplotlib
# NOTE: We do NOT set rcParams['font.family'] globally.
# Doing so causes Matplotlib to repeatedly try (and fail) to resolve the font
# by name from its cache, producing hundreds of 'findfont: not found' warnings.
# Instead we pass FontProperties objects per-element.
font_regular = fm.FontProperties(fname=str(SINHALA_REGULAR))
font_bold = fm.FontProperties(fname=str(SINHALA_BOLD))

# --- Color Scheme ---
COLORS = {
    "primary": "#800000",      # SSB Maroon
    "secondary": "#E0E0E0",    # Light Grey (Targets)
    "accent": "#004080",       # Deep Blue
    "text_dark": "#333333",
    "text_light": "#666666"
}


def _clean_number(val):
    if val is None: return 0.0
    try: return float(str(val).replace(',', '').strip())
    except: return 0.0


def generate_all_charts(data, month):
    """
    Orchestrator to generate all required charts for the monthly report.
    Returns a dictionary of generated chart filenames.
    """
    charts = {}

    if "districts" in data and data["districts"]:
        charts["districts_performance"] = generate_district_performance_chart(data["districts"], month)
        charts["recruitment_growth"] = generate_recruitment_growth_chart(data["districts"], month)

    if "financials" in data and data["financials"]:
        charts["financial_trends"] = generate_financial_trend_chart(data["financials"], month)

    return charts


# 1. District Performance Chart (DIV_02_DISTRICTS)
def generate_district_performance_chart(district_rows, month):
    """Top 10 Districts by TOTAL - uses rank numbers on x-axis
    (Sinhala district names are shown in the HTML table beneath the chart)"""
    valid_districts = []
    for r in district_rows:
        total = _clean_number(r.get("TOTAL", 0))
        if r.get("DISTRICT") and total > 0:
            valid_districts.append({"name": r["DISTRICT"], "total": total})
            
    top_10 = sorted(valid_districts, key=lambda x: x["total"], reverse=True)[:10]

    if not top_10:
        return None

    # Use rank numbers (1-10) as x-labels — Sinhala names are in the HTML table
    ranks = [str(i+1) for i in range(len(top_10))]
    totals = [d["total"] for d in top_10]

    plt.figure(figsize=(10, 6), dpi=300)
    bars = plt.bar(ranks, totals, color=COLORS["primary"], width=0.6)

    # English labels — Matplotlib does not support Sinhala complex script shaping
    plt.title('Top 10 Districts — Recruitment', fontsize=16, pad=20, fontweight='bold', color=COLORS['text_dark'])
    plt.xlabel('Rank (see table below for district names)', fontsize=10, color=COLORS['text_light'])
    plt.ylabel('Total Count', fontsize=12)
    
    # Grid and Spines
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    # Value Labels on bars
    for bar in bars:
        h = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, h + (max(totals)*0.01), 
                 f'{int(h):,}', ha='center', color=COLORS["text_dark"], fontsize=10)

    plt.tight_layout()
    output_path = CHARTS_DIR / f"districts_performance_{month}.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"   📊 Plot generated: {output_path.name}")
    return output_path.name


# 2. Recruitment Growth Chart (DIV_02_DISTRICTS)
def generate_recruitment_growth_chart(district_rows, month):
    """Aggregate all active districts month-over-month for the year"""
    months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    monthly_totals = {m: 0 for m in months}

    for r in district_rows:
        for m in months:
            monthly_totals[m] += _clean_number(r.get(m, 0))

    # Stop at current month (find last non-zero or use month index)
    try:
        current_m_num = int(month.split("-")[1])
        active_months = months[:current_m_num]
        active_totals = [monthly_totals[m] for m in active_months]
    except Exception:
        active_months = months
        active_totals = [monthly_totals[m] for m in active_months]

    if sum(active_totals) == 0:
        return None

    plt.figure(figsize=(10, 5), dpi=300)
    
    # Plot line with markers
    plt.plot(active_months, active_totals, marker='o', linewidth=3, markersize=8, color=COLORS["accent"])
    plt.fill_between(active_months, active_totals, alpha=0.1, color=COLORS["accent"])

    # Styling
    plt.title('Monthly Recruitment Growth Trend', fontsize=16, pad=20, fontweight='bold', color=COLORS['text_dark'])
    plt.ylabel('New Members', fontsize=12)
    
    for label in plt.gca().get_xticklabels():
        label.set_fontsize(10)
    for label in plt.gca().get_yticklabels():
        label.set_fontsize(10)
        
    # Grid and Spines
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    for x, y in zip(active_months, active_totals):
        plt.text(x, y + (max(active_totals)*0.05), f'{int(y):,}', ha='center',
                 fontweight='bold', color=COLORS["accent"], fontsize=10)

    plt.tight_layout()
    output_path = CHARTS_DIR / f"recruitment_growth_{month}.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')  # Bug #3 fix: dpi was only on figure(), not savefig()
    plt.close()

    print(f"   📊 Plot generated: {output_path.name}")
    return output_path.name


# 3. Financial Trend Chart (DIV_03_FINANCIALS)
def generate_financial_trend_chart(finance_rows, month):
    """Extract Income/Collection lines and chart them"""
    months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    
    # We look for a line item representing "Premium Collections" or "Income"
    target_row = None
    for r in finance_rows:
        if r.get("CATEGORY") == "INCOME" or "Premium" in str(r.get("LINE_ITEM", "")):
            target_row = r
            break
            
    if not target_row:
        # Fallback to first row
        target_row = finance_rows[0] if finance_rows else None
        
    if not target_row: 
        return None

    try:
        current_m_num = int(month.split("-")[1])
        active_months = months[:current_m_num]
        values = [_clean_number(target_row.get(m, 0)) for m in active_months]
    except:
        return None

    if sum(values) == 0: return None

    plt.figure(figsize=(10, 5), dpi=300)
    
    # Bar plot for formatting currency
    bars = plt.bar(active_months, values, color=COLORS["secondary"], edgecolor=COLORS["primary"], linewidth=1.5)

    plt.title(f'Financial Performance — {target_row.get("LINE_ITEM", "Income")}', fontsize=16, pad=20, fontweight='bold', color=COLORS['text_dark'])
    plt.ylabel('LKR (Millions)', fontsize=12)
    
    # Format Y-axis as millions (assuming raw is in Rupees)
    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'{x/1000000:,.1f}M'))
    
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    plt.tight_layout()
    output_path = CHARTS_DIR / f"financial_trends_{month}.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"   📊 Plot generated: {output_path.name}")
    return output_path.name