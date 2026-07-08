import re, subprocess, os
html_path = 'pages/bol_versammlung.html'
out_html_path = 'pages/bol_versammlung_test.html'
pdf_path = 'pages/bol_versammlung_test.pdf'

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# basic print css
print_css = """
<style>
@media print {
    body, html { zoom: 1.25 !important; }
}
</style>
"""
html = html.replace('</head>', print_css + '\n</head>')

with open(out_html_path, 'w', encoding='utf-8') as f:
    f.write(html)

subprocess.run([
    'google-chrome', '--headless', '--disable-gpu', '--window-size=1920,1080',
    '--print-to-pdf=' + pdf_path, '--no-pdf-header-footer',
    'file://' + os.path.abspath(out_html_path)
])
print("Done")
