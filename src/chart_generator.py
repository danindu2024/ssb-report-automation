import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from pathlib import Path

# Setup Paths
BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"
FONTS_DIR = ASSETS_DIR / "fonts"
IMAGES_DIR = ASSETS_DIR / "images"

# Load Sinhala Font
font_path = FONTS_DIR / "NotoSansSinhala-Regular.ttf"
sinhala_font = fm.FontProperties(fname=str(font_path))

def generate_district_chart(district_data):
    """
    Generates a bar chart comparing Target vs Actual for top 5 districts.
    """
    # 1. Sort data to find top 5 districts by Target (to keep chart readable)
    # district_data is a list of dicts: [{'district': 'Name', 'target': 100, ...}, ...]
    top_districts = sorted(district_data, key=lambda x: x['target'], reverse=True)[:5]

    names = [d['district'] for d in top_districts]
    targets = [d['target'] for d in top_districts]
    actuals = [d['recruitment'] for d in top_districts]

    # 2. Setup the Plot
    plt.figure(figsize=(10, 6))
    
    # Create bars
    x_pos = range(len(names))
    width = 0.35
    
    plt.bar([x - width/2 for x in x_pos], targets, width, label='Target', color='#e0e0e0')
    plt.bar([x + width/2 for x in x_pos], actuals, width, label='Actual', color='#002366')

    # 3. Styling
    plt.ylabel('Recruits', fontsize=12)
    plt.title('Top 5 Districts Performance', fontsize=14, fontweight='bold', pad=20)
    plt.xticks(x_pos, names, rotation=0)
    plt.legend()
    
    # Add value labels on top of bars
    for i, v in enumerate(actuals):
        plt.text(i + width/2, v + 100, str(int(v)), ha='center', color='#002366', fontweight='bold')

    # 4. Save Chart
    output_path = IMAGES_DIR / "chart_district_performance.png"
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    
    print(f"   📊 Chart generated: {output_path.name}")
    return "chart_district_performance.png"