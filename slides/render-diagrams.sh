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
echo "done: $(ls images/*.svg | wc -l) SVGs"
