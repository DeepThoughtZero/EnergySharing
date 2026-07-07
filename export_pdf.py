import re
import subprocess
import os

html_path = 'pages/bol_versammlung.html'
out_html_path = 'pages/bol_versammlung_print.html'
pdf_path = 'pages/bol_versammlung.pdf'

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Remove password overlay
html = re.sub(r'<div id="pw-overlay">.*?</div>', '', html, flags=re.DOTALL)

# Add active class to all slides just in case
html = html.replace('class="slide"', 'class="slide active"')

# Replace count-up elements with their actual values
def replace_count_up(match):
    attrs = match.group(1)
    target_match = re.search(r'data-target="([^"]+)"', attrs)
    target = target_match.group(1) if target_match else "0"
    
    suffix_match = re.search(r'data-suffix="([^"]+)"', attrs)
    suffix = suffix_match.group(1) if suffix_match else ""
    
    prefix_match = re.search(r'data-prefix="([^"]+)"', attrs)
    prefix = prefix_match.group(1) if prefix_match else ""
    
    no_sep = re.search(r'data-no-sep', attrs)
    
    val = target
    if not no_sep and val.isdigit():
        val = f"{int(val):,}".replace(',', '.')
        
    return f'<span class="count-up"{attrs}>{prefix}{val}{suffix}</span>'

html = re.sub(r'<span class="count-up"([^>]+)>.*?</span>', replace_count_up, html)

# Disable the JS that resets the counters to 0
html = html.replace("el.textContent = '0';", "// el.textContent = '0';")
html = html.replace("animateCounter(el)", "// animateCounter(el)")

print_css = """
<style>
@media print {
    body, html {
        height: auto !important;
        overflow: visible !important;
        background-color: #0a0f1a !important;
        color: #e2e8f0 !important;
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
    }
    .deck {
        position: static !important;
        height: auto !important;
        width: 100% !important;
        display: block !important;
        overflow: visible !important;
    }
    .slide {
        position: relative !important;
        opacity: 1 !important;
        pointer-events: auto !important;
        transform: none !important;
        page-break-after: always !important;
        page-break-inside: avoid !important;
        height: 100vh !important;
        width: 100vw !important;
        display: flex !important;
        overflow: hidden !important;
        break-after: page !important;
    }
    .slide .anim-item {
        opacity: 1 !important;
        transform: none !important;
    }
    #pw-overlay, .nav-bar, .close-btn, .progress-track {
        display: none !important;
    }
    .timeline-line-fill { width: 100% !important; }
    .donut-fill { stroke-dasharray: 999, 999 !important; }
}
@page {
    size: 1920px 1080px; 
    margin: 0;
}
</style>
"""

html = html.replace('</head>', print_css + '\n</head>')

with open(out_html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Modified HTML created. Running Chrome...")

cmd = [
    'google-chrome',
    '--headless',
    '--disable-gpu',
    '--print-to-pdf=' + pdf_path,
    '--no-pdf-header-footer',
    'file://' + os.path.abspath(out_html_path)
]

res = subprocess.run(cmd, capture_output=True, text=True)
print(res.stdout)
print(res.stderr)
if os.path.exists(pdf_path):
    print("PDF created successfully at", pdf_path)
    os.remove(out_html_path)
    print("Cleaned up temporary HTML.")
else:
    print("Failed to create PDF")
