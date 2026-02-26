"""
Chart Generation Engine for SSB Monthly Report Automation.
Creates standardized, beautiful charts using Plotly per the Transformation Guide.
"""
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

from config import CHARTS_DIR

# --- Design System Colors ---
COLORS = {
    "primary": "#002366",      # Navy Blue
    "accent1": "#FF6B35",      # Coral/Orange
    "accent2": "#00A8B5",      # Teal
    "success": "#2ECC71",      # Green
    "alert":   "#E74C3C",      # Red
    "text_dark": "#2C3E50",    # Charcoal
    "text_light": "#6C757D",   # Gray
    "bg_light": "#F8F9FA",     # Light Gray
    "border": "#E9ECEF"        # Border line
}

# --- Base Layout Settings ---
BASE_LAYOUT = dict(
    font=dict(family="Noto Sans Sinhala, Arial", color="#000000", size=28),
    paper_bgcolor="white",
    plot_bgcolor="white",
    margin=dict(l=100, r=40, t=120, b=100)
)

def _clean_number(val):
    if val is None: return 0.0
    try: return float(str(val).replace(',', '').strip())
    except: return 0.0

def apply_base_layout(fig, title, y_title=None, x_title=None):
    fig.update_layout(**BASE_LAYOUT)
    fig.update_layout(
        title=dict(text=title, font=dict(size=40, color=COLORS["primary"]), y=0.98, x=0.5, xanchor='center', yanchor='top'),
        xaxis=dict(title=dict(text=x_title, font=dict(size=32, color="#000000")), showgrid=False, linecolor=COLORS["border"], tickfont=dict(size=28, color="#000000")),
        yaxis=dict(title=dict(text=y_title, font=dict(size=32, color="#000000")), showgrid=True, gridcolor=COLORS["border"], linecolor=COLORS["border"], tickfont=dict(size=28, color="#000000"))
    )
    return fig

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

def generate_district_performance_chart(district_rows, month):
    """Top 10 Districts by TOTAL - uses Bar Chart"""
    valid_districts = []
    for r in district_rows:
        total = _clean_number(r.get("TOTAL", 0))
        if r.get("DISTRICT") and total > 0:
            valid_districts.append({"name": r["DISTRICT"], "total": total})
            
    top_10 = sorted(valid_districts, key=lambda x: x["total"], reverse=True)[:10]

    if not top_10:
        return None

    names = [d["name"] for d in top_10]
    totals = [d["total"] for d in top_10]

    fig = go.Figure(data=[
        go.Bar(
            x=names, 
            y=totals, 
            marker_color=COLORS["primary"],
            text=[f"{t:,.0f}" for t in totals],
            textposition='auto',
            textfont=dict(size=28, color="white")
        )
    ])

    apply_base_layout(fig, title="දිස්ත්‍රික් කාර්ය සාධනය (District Performance)", y_title="සම්පූර්ණ ගණන (Total Count)")
    
    output_path = CHARTS_DIR / f"districts_performance_{month}.png"
    fig.write_image(str(output_path), width=1600, height=900, scale=2)
    print(f"   📊 Plot generated: {output_path.name}")
    return output_path.name

def generate_recruitment_growth_chart(district_rows, month):
    """Aggregate all active districts month-over-month for the year"""
    months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    monthly_totals = {m: 0 for m in months}

    for r in district_rows:
        for m in months:
            monthly_totals[m] += _clean_number(r.get(m, 0))

    try:
        current_m_num = int(month.split("-")[1])
        active_months = months[:current_m_num]
        active_totals = [monthly_totals[m] for m in active_months]
    except Exception:
        active_months = months
        active_totals = [monthly_totals[m] for m in active_months]

    if sum(active_totals) == 0:
        return None

    fig = go.Figure()
    
    # Area chart
    fig.add_trace(go.Scatter(
        x=active_months, 
        y=active_totals, 
        fill='tozeroy',
        fillcolor=f"rgba(0, 168, 181, 0.2)", # Teal with opacity
        line=dict(color=COLORS["accent2"], width=6),
        mode='lines+markers+text',
        marker=dict(size=20, color=COLORS["accent2"]),
        text=[f"{t:,.0f}" for t in active_totals],
        textposition="top center",
        textfont=dict(size=28, color="#000000")
    ))

    apply_base_layout(fig, title="මාසික බඳවා ගැනීමේ වර්ධනය (Monthly Recruitment Growth)", y_title="නව සාමාජිකයින් (New Members)")

    output_path = CHARTS_DIR / f"recruitment_growth_{month}.png"
    fig.write_image(str(output_path), width=1600, height=900, scale=2)
    print(f"   📊 Plot generated: {output_path.name}")
    return output_path.name

def generate_financial_trend_chart(finance_rows, month):
    """Extract Income/Collection lines and chart them"""
    months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    
    target_row = None
    for r in finance_rows:
        if r.get("CATEGORY") == "INCOME" or "Premium" in str(r.get("LINE_ITEM", "")):
            target_row = r
            break
            
    if not target_row:
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

    # Values in millions
    values_m = [v / 1_000_000 for v in values]

    fig = go.Figure(data=[
        go.Bar(
            x=active_months, 
            y=values_m, 
            marker_color=COLORS["accent1"],
            text=[f"{v:,.1f}M" for v in values_m],
            textposition='auto',
            textfont=dict(size=28, color="white")
        )
    ])

    title_text = f'මූල්‍ය ප්‍රවණතා — {target_row.get("LINE_ITEM", "Income")} (Financial Trends)'
    apply_base_layout(fig, title=title_text, y_title="මිලියන (Millions)")

    output_path = CHARTS_DIR / f"financial_trends_{month}.png"
    fig.write_image(str(output_path), width=1600, height=900, scale=2)
    print(f"   📊 Plot generated: {output_path.name}")
    return output_path.name