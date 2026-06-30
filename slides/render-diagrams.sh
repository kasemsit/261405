#!/usr/bin/env bash
# Pre-render all Mermaid diagrams to static SVG (avoids the Reveal.js
# hidden-slide measurement bug). Re-run after editing any diagrams/*.mmd.
set -e
cd "$(dirname "$0")"
export PUPPETEER_SKIP_DOWNLOAD=1
for f in diagrams/*.mmd; do
  name=$(basename "$f" .mmd)
  echo "rendering $name"
  npx -y @mermaid-js/mermaid-cli -i "$f" -o "images/$name.svg" \
    -c mermaid-config.json -b transparent
done
echo "done: $(ls images/diag*.svg | wc -l) diagrams rendered"

# Post-process: add rounded corners (rx=8) to all node rects, thicken arrows
python3 - << 'PYEOF'
import re, glob

EXTRA_CSS = (
    ".flowchart-link{stroke:#555!important;stroke-width:1.6px!important;}"
    ".arrowheadPath{fill:#444!important;}"
    ".marker{fill:#555!important;stroke:#555!important;}"
    ".cluster rect{rx:10px;border-radius:10px;}"
)
for path in sorted(glob.glob("images/diag*.svg")):
    with open(path) as f:
        svg = f.read()
    svg = re.sub(
        r'(<rect class="basic label-container"(?![^>]*\brx=)[^>]*?)(/?>)',
        r'\1 rx="8"\2', svg)
    if EXTRA_CSS not in svg:
        svg = svg.replace('</style>', EXTRA_CSS + '</style>', 1)
    with open(path, 'w') as f:
        f.write(svg)
print(f"styled {len(glob.glob('images/diag*.svg'))} SVGs")
PYEOF
