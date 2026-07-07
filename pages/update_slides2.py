import re

file_path = "/home/bigbrain/Dokumente/Jochen/PowerSharing/PowerSharingHomepage/pages/bol_versammlung.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Folie 11: Unser Partner für die Abrechnung -> Möglicher Partner für die Abrechnung
content = content.replace(
    "decarbon1ze</span> — Unser Partner für die Abrechnung",
    "decarbon1ze</span> — Möglicher Partner für die Abrechnung"
)

# 2. Folie 12: Weitere denkbare Partner -> Text change
content = content.replace(
    "Wofür benötigen wir einen Partner? Für die 15-Minuten-Bilanzierung, das Datenmanagement und die rechtssichere Abrechnung.",
    "Wofür benötigen wir einen Partner? Für die 15-Minuten-Bilanzierung, Datenmanagement und Abrechnung."
)

# 3. Folie 14: Ring animieren
keyframes_css = "@keyframes spin-donut { from { transform: rotate(-90deg); } to { transform: rotate(270deg); } }\n        "
# Insert keyframes into CSS (just before .donut-chart css)
content = content.replace(
    ".donut-chart { position: relative;",
    keyframes_css + ".donut-chart { position: relative;"
)
# Add inline style to SVG in the donut-wrap
donut_svg_target = '<svg viewBox="0 0 120 120">'
donut_svg_replacement = '<svg viewBox="0 0 120 120" style="animation: spin-donut 60s linear infinite;">'
# Only replace in Folie 10 Ökosystem Donut
f10_marker = "<!-- ══════════ F10 ── Ökosystem Donut ══════════ -->"
parts = content.split(f10_marker)
if len(parts) > 1:
    parts[1] = parts[1].replace(donut_svg_target, donut_svg_replacement, 1)
    content = f10_marker.join(parts)

# 4. Folie 18: Wrap list items in spans
li1 = '<li><i class="fa-solid fa-arrow-right" style="color:#facc15; margin-right:4px;"></i>Die Dorfheizung benötigt im Sommer (PV-Hochphase) <strong>kaum</strong> Energie — genau dann, wenn am meisten Solarstrom anfällt.</li>'
li1_rep = '<li><i class="fa-solid fa-arrow-right" style="color:#facc15; margin-right:4px;"></i><span>Die Dorfheizung benötigt im Sommer (PV-Hochphase) <strong>kaum</strong> Energie — genau dann, wenn am meisten Solarstrom anfällt.</span></li>'
content = content.replace(li1, li1_rep)

li2 = '<li><i class="fa-solid fa-arrow-right" style="color:#facc15; margin-right:4px;"></i>Klimaanlagen erhöhen den Eigenverbrauch, generieren jedoch keine neuen Einnahmen.</li>'
li2_rep = '<li><i class="fa-solid fa-arrow-right" style="color:#facc15; margin-right:4px;"></i><span>Klimaanlagen erhöhen den Eigenverbrauch, generieren jedoch keine neuen Einnahmen.</span></li>'
content = content.replace(li2, li2_rep)


# 5. Folie 22: 2 Seiten nach vorne schieben
f14_marker = "<!-- ══════════ F14 ── Smart Meter ══════════ -->"
f15b_marker = "<!-- ══════════ F15b ── Weitere Vorteile in Zukunft ══════════ -->"
f16_marker = "<!-- ══════════ F16 ── CTA (mit Herr/Frau) ══════════ -->"

# Extract F15b block
idx_15b = content.find(f15b_marker)
idx_16 = content.find(f16_marker)

if idx_15b != -1 and idx_16 != -1:
    f15b_block = content[idx_15b:idx_16]
    # Remove F15b block from its original position
    content = content[:idx_15b] + content[idx_16:]
    
    # Insert F15b block just before F14
    idx_14 = content.find(f14_marker)
    if idx_14 != -1:
        content = content[:idx_14] + f15b_block + content[idx_14:]
    else:
        print("Error: Could not find F14 marker.")

# 6. Re-number data-slide attributes
parts = content.split('<div class="slide"')
new_content = parts[0]
for i in range(1, len(parts)):
    # Replace data-slide="..." with data-slide="i-1"
    part = parts[i]
    part = re.sub(r' data-slide="\d+"', f' data-slide="{i-1}"', part, count=1)
    new_content += '<div class="slide"' + part

with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("Modification complete.")
