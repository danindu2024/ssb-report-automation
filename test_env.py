from weasyprint import HTML

# Simple HTML with Sinhala text
html = """
<!DOCTYPE html>
<style>
    @font-face {
        font-family: 'Noto Sans Sinhala';
        src: local('Noto Sans Sinhala'), url('assets/fonts/NotoSansSinhala-Regular.ttf');
    }
    body { font-family: 'Noto Sans Sinhala', sans-serif; }
</style>
<h1>ශ්‍රී ලංකා සමාජ ආරක්ෂණ මණ්ඩලය</h1>
<p>පරීක්ෂණ වාර්තාව: සාර්ථකයි (Success)</p>
"""

print("Generating test PDF...")
HTML(string=html).write_pdf("test_sinhala.pdf")
print("Done. Check test_sinhala.pdf")