# 261405 — Advanced Computer Engineering Technology

Lecture slides built with [Quarto](https://quarto.org) (Reveal.js).

🔗 **Live slides:** https://kasemsit.github.io/261405/

## Slides

| Deck | Source | Topic |
|------|--------|-------|
| Machine Learning: From Data to LLMs | [`slides/ml-intro.qmd`](slides/ml-intro.qmd) | ~80–90 min intro for students with no prior ML, landing on LLMs |

## Build & preview

```bash
cd slides

# one-off render to HTML
quarto render ml-intro.qmd

# live preview in the browser (auto-reloads on save)
quarto preview ml-intro.qmd
```

Open `slides/ml-intro.html` in any browser. Press **`s`** for speaker notes,
**`f`** for fullscreen, **`o`** for the slide overview, **`b`** for the chalkboard.

## Export to PDF

```bash
cd slides
quarto render ml-intro.qmd --to pdf      # needs a recent Chrome/Chromium
```

## Deployment (automatic, via GitHub Actions)

Every push to `main` triggers [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml),
which renders the deck and publishes it to **GitHub Pages** — the deck is served as the
site's home page (`index.html`).

**One-time setup on GitHub:** repo **Settings → Pages → Build and deployment →
Source: _GitHub Actions_**. After the first successful run the slides are live at the
URL above.

> CI only needs Quarto: the diagrams/charts are committed as SVGs, so no
> mermaid-cli or matplotlib runs at build time.

## Diagrams

All flowcharts are **original Mermaid**, kept as editable sources in
`slides/diagrams/*.mmd` and **pre-rendered to SVG** in `slides/images/`.

> Why pre-render? Reveal.js hides inactive slides with `display:none`, so
> browser-side Mermaid measures those diagrams at ~0 width and clips the labels.
> Static SVGs sidestep that entirely (and load faster / work offline).

After editing any `diagrams/*.mmd`, regenerate the SVGs:

```bash
cd slides
./render-diagrams.sh      # uses npx @mermaid-js/mermaid-cli + mermaid-config.json
```

## Images / figures

The plots (overfitting panels, the word-embedding map) are **original figures**
generated with matplotlib — safe to publish. Regenerate them with:

```bash
cd slides
python3 figures/make-figures.py   # writes images/overfitting.svg, images/embeddings.svg
```

To add your own pictures, drop them into `slides/images/` and reference them
with `![](images/your-file.png)`. (The original `.pptx` figures are third-party
and intentionally **not** included — don't publish them.)

## Keeping slides to one page

Reveal renders at 1280×720; content taller than that gets clipped. To audit
which slides overflow, the helper script visits every slide, reveals all
fragments, and measures content height (accounting for Reveal's scale):

```bash
cd slides && quarto render ml-intro.qmd
node tools/measure-overflow.js "$PWD/ml-intro.html"   # needs: npm i puppeteer-core
```

Fix an overflowing slide by adding `{.smaller}` to its `##` heading, trimming
text, or shrinking an image with `{width="80%"}`.

> The original `.pptx` decks reuse third-party figures (CS329S, *Hands-On LLM*),
> so those images are **not** included here — don't publish them.

## Structure

```
261405/
├── README.md
└── slides/
    ├── ml-intro.qmd          # the deck
    ├── custom.scss           # CMU-red theme + scroll/overflow handling
    ├── diagrams/*.mmd        # editable Mermaid sources
    ├── images/*.svg          # pre-rendered diagrams (+ your own figures)
    ├── mermaid-config.json   # theme/font for pre-rendered diagrams
    └── render-diagrams.sh    # regenerate SVGs after editing .mmd
```
