#!/usr/bin/env python3
"""Generate original, publish-safe figures for the deck (no copyright issues).

Run from the slides/ directory:
    python3 figures/make-figures.py
Outputs SVGs into images/.
"""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({"font.size": 13, "font.family": "DejaVu Sans", "svg.fonttype": "none"})
RED, INK, GREEN, MUTE, BLUE = "#b8232f", "#1f2933", "#137333", "#7b8794", "#1a73a8"

# ---------- 1) Overfitting: underfit / good fit / overfit ----------
rng = np.random.default_rng(7)
x = np.linspace(0, 1, 14)
true = lambda t: np.sin(2 * np.pi * t)
y = true(x) + rng.normal(0, 0.18, len(x))
xs = np.linspace(0, 1, 300)
fig, ax = plt.subplots(1, 3, figsize=(10.5, 3.3))
for a, deg, ti, (cap, col) in zip(
    ax, [1, 3, 12], ["Underfit", "Good fit", "Overfit"],
    [("too simple", MUTE), ("captures the trend", GREEN), ("memorizes noise", RED)]):
    a.scatter(x, y, s=34, color=INK, zorder=3)
    a.plot(xs, np.polyval(np.polyfit(x, y, deg), xs), color=RED, lw=2.4, zorder=2)
    a.plot(xs, true(xs), color=MUTE, lw=1.4, ls="--", zorder=1)
    a.set_title(ti, color="#7a1f2b", fontweight="bold")
    a.set_xticks([]); a.set_yticks([]); a.set_ylim(-1.8, 1.8)
    for s in a.spines.values(): s.set_color("#cdd4dc")
    a.text(0.02, -1.65, cap, color=col, fontsize=11)
fig.tight_layout()
fig.savefig("images/overfitting.svg", transparent=True, bbox_inches="tight")
print("saved images/overfitting.svg")

# ---------- 2) Word-embedding map ----------
fig, ax = plt.subplots(figsize=(6.6, 5.0))
words = {"cat": (1.0, 3.6), "dog": (1.5, 3.9), "lion": (0.6, 4.2),
         "Thailand": (4.4, 1.1), "Japan": (4.9, 1.5), "France": (4.2, 0.6),
         "king": (1.2, 1.0), "queen": (2.4, 1.7), "man": (1.4, 0.2), "woman": (2.6, 0.9)}
groups = {"animals": ["cat", "dog", "lion"], "countries": ["Thailand", "Japan", "France"],
          "royalty/gender": ["king", "queen", "man", "woman"]}
colors = {"animals": GREEN, "countries": BLUE, "royalty/gender": RED}
for g, ws in groups.items():
    pts = np.array([words[w] for w in ws])
    ax.scatter(pts[:, 0], pts[:, 1], s=70, color=colors[g], label=g, zorder=3)
    for w in ws:
        ax.annotate(w, words[w], xytext=(6, 5), textcoords="offset points", fontsize=12, color=INK)
for a, b in [("man", "king"), ("woman", "queen")]:  # parallel analogy arrows
    ax.annotate("", xy=words[b], xytext=words[a],
                arrowprops=dict(arrowstyle="->", color="#7a1f2b", lw=2, ls="--"))
ax.text(0.55, 0.55, "king − man + woman ≈ queen", color="#7a1f2b", fontsize=11.5, style="italic")
ax.set_xlim(0, 6); ax.set_ylim(-0.4, 5); ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values(): s.set_color("#cdd4dc")
ax.legend(loc="upper right", frameon=False, fontsize=10.5)
fig.tight_layout()
fig.savefig("images/embeddings.svg", transparent=True, bbox_inches="tight")
print("saved images/embeddings.svg")

# ---------- 3) Latency -> business impact ----------
fig, ax = plt.subplots(figsize=(7.6, 3.4))
labels = ["Amazon (2006)\n+100 ms latency", "Bing (2009)\n+2 s latency", "Google×Deloitte (2020)\n−0.1 s latency"]
vals = [1.0, 4.3, 8.4]
bars = ax.barh(labels, vals, color=[RED, RED, GREEN])
for b, v in zip(bars, vals):
    ax.text(v + 0.15, b.get_y() + b.get_height()/2, f"{v}%", va="center", fontweight="bold", color=INK)
ax.set_xlabel("business impact on sales / conversions (%)")
ax.set_xlim(0, 10); ax.invert_yaxis()
for s in ["top", "right"]: ax.spines[s].set_visible(False)
for s in ax.spines.values(): s.set_color("#cdd4dc")
ax.set_title("Small speed changes → real money", color="#7a1f2b", fontweight="bold")
fig.tight_layout(); fig.savefig("images/latency-bar.svg", transparent=True, bbox_inches="tight")
print("saved images/latency-bar.svg")

# ---------- 4) Model scaling over time (2018 → 2026) ----------
fig, ax = plt.subplots(figsize=(7.8, 3.9))
# publicly disclosed sizes (dense models)
disc = [("GPT-1", 2018, 0.117), ("BERT", 2018, 0.34), ("GPT-2", 2019, 1.5),
        ("GPT-3", 2020, 175), ("PaLM", 2022, 540)]
xs = [m[1] for m in disc]; ys = [m[2] for m in disc]
ax.plot(xs, ys, color=RED, lw=1.5, alpha=0.5, zorder=2)
ax.scatter(xs, ys, s=75, color=RED, zorder=3)
for name, yr, p in disc:
    ax.annotate(f"{name}\n{p:g}B", (yr, p), xytext=(0, 9), textcoords="offset points",
                ha="center", fontsize=9.5, color=INK)
# estimated frontier — labs stopped disclosing sizes; GPT-4 rumoured ~1.8T (MoE)
ax.plot([2022, 2023], [540, 1800], color=RED, lw=1.5, alpha=0.3, ls="--", zorder=2)
ax.scatter([2023], [1800], s=90, facecolors="none", edgecolors=RED, linewidths=2, zorder=3)
ax.annotate("GPT-4\n~1.8T (est.)", (2023, 1800), xytext=(0, 10), textcoords="offset points",
            ha="center", fontsize=9.5, color=MUTE)
# 2024–2026: sizes undisclosed
ax.axvspan(2023.5, 2026.4, color="#f4c542", alpha=0.12, zorder=0)
ax.text(2025.0, 4.0, "2024–26:\nsizes undisclosed\n(sparse MoE)",
        color="#8a5200", style="italic", fontsize=8.8, ha="center", va="center")
ax.set_yscale("log"); ax.set_ylabel("parameters (billions, log)")
ax.set_xticks([2018, 2020, 2022, 2024, 2026]); ax.set_xlim(2017.3, 2026.6); ax.set_ylim(0.05, 7000)
for s in ["top", "right"]: ax.spines[s].set_visible(False)
for s in ax.spines.values(): s.set_color("#cdd4dc")
ax.set_title("Bigger and bigger: the scale race (2018 → 2026)", color="#7a1f2b", fontweight="bold", fontsize=12)
fig.tight_layout(); fig.savefig("images/scaling.svg", transparent=True, bbox_inches="tight")
print("saved images/scaling.svg")

# ---------- 5) Classification vs regression ----------
fig, ax = plt.subplots(1, 2, figsize=(8.4, 3.6))
rng = np.random.default_rng(3)
a = rng.normal([1.2, 1.2], 0.45, (25, 2)); b = rng.normal([2.8, 2.8], 0.45, (25, 2))
ax[0].scatter(a[:, 0], a[:, 1], color=RED, s=28, label="class A")
ax[0].scatter(b[:, 0], b[:, 1], color=BLUE, s=28, label="class B")
ax[0].plot([0.3, 3.7], [3.7, 0.3], color=INK, lw=2, ls="--")
ax[0].set_title("Classification → a category", color="#7a1f2b", fontweight="bold", fontsize=12)
ax[0].legend(frameon=False, fontsize=9, loc="upper left")
xr = rng.uniform(0, 4, 30); yr = 0.8 * xr + 0.5 + rng.normal(0, 0.4, 30)
ax[1].scatter(xr, yr, color=GREEN, s=28)
xs = np.linspace(0, 4, 50); ax[1].plot(xs, 0.8 * xs + 0.5, color=RED, lw=2.4)
ax[1].set_title("Regression → a number", color="#7a1f2b", fontweight="bold", fontsize=12)
for a_ in ax:
    a_.set_xticks([]); a_.set_yticks([])
    for s in a_.spines.values(): s.set_color("#cdd4dc")
fig.tight_layout(); fig.savefig("images/clf-vs-reg.svg", transparent=True, bbox_inches="tight")
print("saved images/clf-vs-reg.svg")

# ---------- 6) Attention heatmap ----------
fig, ax = plt.subplots(figsize=(6.2, 5.2))
toks = ["The", "tired", "animal", "didn't", "cross", "because", "it"]
n = len(toks); rng = np.random.default_rng(11)
M = rng.uniform(0.02, 0.18, (n, n))
M[6] = [0.05, 0.08, 0.62, 0.04, 0.05, 0.06, 0.10]  # "it" attends to "animal"
M = M / M.sum(1, keepdims=True)
im = ax.imshow(M, cmap="Reds", aspect="auto")
ax.set_xticks(range(n)); ax.set_yticks(range(n))
ax.set_xticklabels(toks, rotation=40, ha="right", fontsize=11)
ax.set_yticklabels(toks, fontsize=11)
ax.set_ylabel("query word"); ax.set_xlabel("attends to →")
ax.add_patch(plt.Rectangle((1.5, 5.5), 1, 1, fill=False, edgecolor="#137333", lw=2.5))
ax.set_title("Self-attention: \"it\" → \"animal\"", color="#7a1f2b", fontweight="bold")
fig.tight_layout(); fig.savefig("images/attention.svg", transparent=True, bbox_inches="tight")
print("saved images/attention.svg")

# ---------- 7) Confusion matrix (for the metrics slide) ----------
fig, ax = plt.subplots(figsize=(5.0, 4.3))
cells = [["TP", "FN"], ["FP", "TN"]]
desc  = [["caught it\n(correct)", "missed it\n(false neg)"],
         ["false alarm\n(false pos)", "correct\nrejection"]]
fills = [["#e6f4ea", "#fff3e0"], ["#fff3e0", "#e6f4ea"]]
for i in range(2):
    for j in range(2):
        ax.add_patch(plt.Rectangle((j, 1 - i), 1, 1, facecolor=fills[i][j], edgecolor="#cdd4dc", lw=1.2))
        ax.text(j + 0.5, 1 - i + 0.62, cells[i][j], ha="center", va="center", fontweight="bold", fontsize=17, color=INK)
        ax.text(j + 0.5, 1 - i + 0.28, desc[i][j], ha="center", va="center", fontsize=9, color=MUTE)
ax.set_xlim(-0.02, 2.02); ax.set_ylim(-0.02, 2.02)
ax.set_xticks([0.5, 1.5]); ax.set_xticklabels(["predicted +", "predicted −"], fontsize=11)
ax.set_yticks([1.5, 0.5]); ax.set_yticklabels(["actual +", "actual −"], fontsize=11, rotation=90, va="center")
ax.tick_params(length=0)
for s in ax.spines.values(): s.set_visible(False)
ax.set_title("Confusion matrix", color="#7a1f2b", fontweight="bold")
fig.tight_layout(); fig.savefig("images/confusion.svg", transparent=True, bbox_inches="tight")
print("saved images/confusion.svg")

# ---------- 8) Clustering (for the unsupervised slide) ----------
fig, ax = plt.subplots(figsize=(5.2, 4.0))
rng = np.random.default_rng(5)
for c, col, lab in [((1.1, 1.1), RED, "group A"), ((3.1, 3.0), BLUE, "group B"), ((1.0, 3.2), GREEN, "group C")]:
    p = rng.normal(c, 0.42, (22, 2))
    ax.scatter(p[:, 0], p[:, 1], color=col, s=32, alpha=0.9, label=lab)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values(): s.set_color("#cdd4dc")
ax.legend(frameon=False, fontsize=10, loc="lower right")
ax.set_title("Clustering: structure with no labels", color="#7a1f2b", fontweight="bold", fontsize=12)
fig.tight_layout(); fig.savefig("images/clustering.svg", transparent=True, bbox_inches="tight")
print("saved images/clustering.svg")

# ---------- 9) Tokenization → embedding (text to numbers) ----------
fig, ax = plt.subplots(figsize=(9.2, 2.6))
ax.set_xlim(0, 10); ax.set_ylim(0, 3); ax.axis("off")
ax.text(1.0, 1.5, '"unhappiness"', fontsize=16, fontweight="bold", ha="center", va="center", color=INK)
ax.annotate("", xy=(2.55, 1.5), xytext=(1.95, 1.5), arrowprops=dict(arrowstyle="->", lw=1.6, color=MUTE))
ax.text(2.25, 1.92, "tokenize", fontsize=9, color=MUTE, ha="center", style="italic")
toks = [("un", RED), ("happi", GREEN), ("ness", BLUE)]
tx = [3.1, 4.05, 5.0]
for (t, c), x in zip(toks, tx):
    ax.add_patch(plt.Rectangle((x - 0.42, 1.18), 0.84, 0.64, facecolor=c, alpha=0.14, edgecolor=c, lw=1.5))
    ax.text(x, 1.5, t, fontsize=13, ha="center", va="center", color=c, fontweight="bold")
ax.annotate("", xy=(6.45, 1.5), xytext=(5.65, 1.5), arrowprops=dict(arrowstyle="->", lw=1.6, color=MUTE))
ax.text(6.05, 1.92, "embed", fontsize=9, color=MUTE, ha="center", style="italic")
rng = np.random.default_rng(2)
vx = [7.1, 8.0, 8.9]
for (t, c), x in zip(toks, vx):
    ax.add_patch(plt.Rectangle((x - 0.34, 0.35), 0.68, 2.25, facecolor=c, alpha=0.08, edgecolor=c, lw=1.2))
    for j, v in enumerate(rng.uniform(-0.9, 0.9, 4)):
        ax.text(x, 2.28 - j * 0.52, f"{v:+.1f}", fontsize=10, ha="center", va="center", color=INK, family="monospace")
ax.text(8.0, 2.85, "vectors (embeddings)", fontsize=9.5, color=MUTE, ha="center", style="italic")
fig.tight_layout(); fig.savefig("images/tokenize.svg", transparent=True, bbox_inches="tight")
print("saved images/tokenize.svg")
