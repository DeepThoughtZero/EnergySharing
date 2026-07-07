import re

file_path = "/home/bigbrain/Dokumente/Jochen/PowerSharing/PowerSharingHomepage/pages/bol_versammlung.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update the total slides counter from 18 to 19
content = content.replace("1 / 18", "1 / 19")

# 2. Insert the TOC slide
toc_slide = """
        <!-- ══════════ F1b ── Inhaltsverzeichnis ══════════ -->
        <div class="slide" data-slide="1">
            <div class="bg-glow blue" style="width:500px;height:500px;top:20%;left:-10%"></div>
            <div class="slide-tag"><span class="dot"></span> Agenda</div>
            <h2 class="slide-heading">Unsere <span class="accent">Themen</span> heute</h2>
            <p class="slide-subtitle">Ein klarer Fahrplan für die Energiewende in BOL.</p>
            <div class="slide-body" style="max-width: 800px; margin-top: 1.5rem;">
                <ul class="cta-list" style="margin: 0 auto;">
                    <li class="anim-item"><div class="cta-icon icon-yellow">1</div><span><strong>Vision:</strong> BOL als Vorreiter-Region für die Energiewende</span></li>
                    <li class="anim-item"><div class="cta-icon icon-green">2</div><span><strong>Das Power-Share Modell</strong> & unsere Partner</span></li>
                    <li class="anim-item"><div class="cta-icon icon-blue">3</div><span><strong>Wirtschaftlichkeit</strong> & Rechenbeispiele</span></li>
                    <li class="anim-item"><div class="cta-icon icon-orange">4</div><span><strong>Herausforderungen</strong> & Lösungsansätze</span></li>
                    <li class="anim-item"><div class="cta-icon icon-purple">5</div><span><strong>Partnerschaft:</strong> Wie die Gemeinden uns unterstützen können</span></li>
                    <li class="anim-item"><div class="cta-icon icon-teal">6</div><span><strong>Offene Fragen</strong> & Nächste Schritte</span></li>
                </ul>
            </div>
        </div>
"""
# Find where F2 starts
f2_marker = "<!-- ══════════ F2 ── Team Power-Share ══════════ -->"
content = content.replace(f2_marker, toc_slide + "\n        " + f2_marker)

# 3. Update data-slide attributes
# We split the content by '<div class="slide"' and reconstruct it
parts = content.split('<div class="slide"')
new_content = parts[0]
for i in range(1, len(parts)):
    # The part starts with ' data-slide="X">'
    # We can replace ' data-slide="X"' with ' data-slide="{i-1}"'
    part = parts[i]
    part = re.sub(r' data-slide="\d+"', f' data-slide="{i-1}"', part, count=1)
    
    # Also replace slide-tag based on its content
    # We extract the slide-tag span
    tag_match = re.search(r'<div class="slide-tag"><span class="dot"></span> (.*?)</div>', part)
    if tag_match:
        tag_text = tag_match.group(1)
        new_text = tag_text
        if tag_text == "Initiative" or "Block 1" in tag_text:
            new_text = "1. Vision: BOL als Vorreiter-Region für die Energiewende"
        elif "Block 2" in tag_text:
            new_text = "2. Das Power-Share Modell & unsere Partner"
        elif "Block 3" in tag_text or tag_text == "Block 4 · Ausblick":
            new_text = "3. Wirtschaftlichkeit & Rechenbeispiele"
        elif "Block 4 · Schulterschluss" in tag_text or "Block 4 · An Süwag/Syna" in tag_text:
            new_text = "4. Herausforderungen & Lösungsansätze"
        elif "Block 4 · Bitten" in tag_text:
            new_text = "5. Partnerschaft: Wie die Gemeinden uns unterstützen können"
        elif "Abschluss" in tag_text:
            new_text = "6. Offene Fragen & Nächste Schritte"
        
        if new_text != tag_text:
            part = part.replace(f'<div class="slide-tag"><span class="dot"></span> {tag_text}</div>',
                                f'<div class="slide-tag"><span class="dot"></span> {new_text}</div>')

    new_content += '<div class="slide"' + part

# Verify the changes
with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("Modification complete.")
