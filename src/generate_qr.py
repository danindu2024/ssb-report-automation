import qrcode
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"
CHARTS_DIR = OUTPUT_DIR / "charts"

# Ensure charts exists
CHARTS_DIR.mkdir(parents=True, exist_ok=True)

# Generate a mock QR code for the cover page
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)
qr.add_data('https://ssb.gov.lk/annual-report/2026')
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
output_path = CHARTS_DIR / "cover_qr.png"
img.save(str(output_path))
print(f"Generated Cover QR code at {output_path}")
