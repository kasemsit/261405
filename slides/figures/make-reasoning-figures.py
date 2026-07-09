#!/usr/bin/env python3
"""Original, publish-safe figures for the reasoning/agents deck.

Run from the slides/ directory:
    python3 figures/make-reasoning-figures.py
Outputs SVGs into images/.

Curves are illustrative (schematic), not exact reproductions of any paper.
"""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import date

plt.rcParams.update({"font.size": 13, "font.family": "DejaVu Sans", "svg.fonttype": "none"})
RED, INK, GREEN, MUTE, BLUE = "#b8232f", "#1f2933", "#137333", "#7b8794", "#1a73a8"

# ---------- 1) Accuracy vs. test-time compute — REAL o1 data ----------
# Source: OpenAI, "Learning to Reason with LLMs" (o1, 2024), AIME 2024.
#   GPT-4o (no reasoning):        ~12%  (1 sample)
#   o1 single sample (pass@1):     74.4%
#   o1 consensus @ 64 samples:     83.3%
#   o1 re-rank @ 1000 samples:     93.4%
fig, ax = plt.subplots(figsize=(7.4, 4.3))
o1_x = np.array([1, 64, 1000])
o1_y = np.array([74.4, 83.3, 93.4])
ax.plot(o1_x, o1_y, color=RED, lw=2.6, marker="o", ms=8, zorder=3, label="o1 (reasoning model)")
for x, y in zip(o1_x, o1_y):
    ax.annotate(f"{y:.1f}%", (x, y), xytext=(0, 10), textcoords="offset points",
                ha="center", fontsize=11, color=RED, fontweight="bold")
ax.annotate("single sample", (1, 74.4), xytext=(6, -16), textcoords="offset points", fontsize=10, color=INK)
ax.annotate("consensus@64", (64, 83.3), xytext=(-10, -18), textcoords="offset points", fontsize=10, color=INK)
ax.annotate("re-rank@1000", (1000, 93.4), xytext=(-20, -20), textcoords="offset points", fontsize=10, color=INK)

# GPT-4o baseline (no reasoning)
ax.scatter([1], [12], s=70, color=BLUE, zorder=4)
ax.annotate("GPT-4o: 12%\n(no reasoning)", (1, 12), xytext=(8, 4), textcoords="offset points",
            fontsize=10.5, color=BLUE)

ax.set_xscale("log")
ax.set_xticks([1, 10, 64, 100, 1000])
ax.set_xticklabels(["1", "10", "64", "100", "1000"])
ax.set_xlabel("samples per problem at test time  (log scale)")
ax.set_ylabel("AIME 2024 accuracy (%)")
ax.set_ylim(0, 100)
ax.set_title("o1 on AIME 2024: reason first, then sample more", color="#7a1f2b", fontweight="bold")
for s in ["top", "right"]: ax.spines[s].set_visible(False)
for s in ax.spines.values(): s.set_color("#cdd4dc")
ax.grid(True, which="both", axis="both", color="#eef1f5", lw=0.8)
ax.legend(loc="lower right", frameon=False, fontsize=10.5)
fig.tight_layout()
fig.savefig("images/reason-scaling.svg", transparent=True, bbox_inches="tight")
print("saved images/reason-scaling.svg")

# ---------- 2) Agent task-horizon "Moore's law" — REAL METR data ----------
# Source: METR, benchmark_results_1_1.yaml (50% time horizon, in MINUTES).
#   https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/
pts = [
    (date(2023, 3, 14),  3.99,  "GPT-4"),
    (date(2024, 5, 13),  6.99,  "GPT-4o"),
    (date(2024, 9, 12),  20.33, "o1-preview"),
    (date(2024, 12, 5),  38.83, "o1"),
    (date(2025, 2, 24),  60.39, "Claude 3.7 Sonnet"),
    (date(2025, 4, 16),  119.73, "o3"),
    (date(2025, 8, 7),   203.01, "GPT-5"),
    (date(2025, 11, 18), 224.33, "Gemini 3 Pro"),
    (date(2026, 2, 5),   718.81, "Claude Opus 4.6"),
    (date(2026, 4, 7),   1044.78, "Claude Mythos"),
]
# label only a representative subset to avoid clutter
label_for = {"GPT-4", "o1", "Claude 3.7 Sonnet", "o3", "GPT-5", "Claude Opus 4.6", "Claude Mythos"}
xs = np.array([mdates.date2num(p[0]) for p in pts])
ys = np.array([p[1] for p in pts])

fig, ax = plt.subplots(figsize=(7.8, 4.4))

# fitted exponential trend line + doubling time from the real points
slope, intercept = np.polyfit(xs, np.log2(ys), 1)          # log2(min) per day
doubling_months = (1.0 / slope) / 30.44
resid = np.log2(ys) - (slope * xs + intercept)
r2 = 1 - np.sum(resid**2) / np.sum((np.log2(ys) - np.log2(ys).mean())**2)
xline = np.linspace(min(xs), max(xs) + 60, 100)
ax.plot(xline, 2 ** (slope * xline + intercept), color=MUTE, lw=2, ls="--", zorder=1,
        label=f"trend: doubling ≈ {doubling_months:.1f} months  (R²={r2:.2f})")

ax.scatter(xs, ys, s=70, color=RED, zorder=3)
for (d, y, name), x in zip(pts, xs):
    if name in label_for:
        dy = 12 if name != "Claude Opus 4.6" else -20
        ax.annotate(name, (x, y), xytext=(6, dy), textcoords="offset points",
                    fontsize=9.5, color=INK)

ax.set_yscale("log")
ax.set_yticks([4, 15, 30, 60, 120, 240, 480, 960])
ax.set_yticklabels(["4 m", "15 m", "30 m", "1 h", "2 h", "4 h", "8 h", "16 h"])
ax.set_ylabel("task length an agent finishes  (50% success)")
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax.set_title("Agent task-horizon is doubling fast  (METR)", color="#7a1f2b", fontweight="bold")
for s in ["top", "right"]: ax.spines[s].set_visible(False)
for s in ax.spines.values(): s.set_color("#cdd4dc")
ax.grid(True, which="major", axis="y", color="#eef1f5", lw=0.8)
ax.legend(loc="upper left", frameon=False, fontsize=10)
fig.tight_layout()
fig.savefig("images/agent-horizon.svg", transparent=True, bbox_inches="tight")
print(f"saved images/agent-horizon.svg  (doubling {doubling_months:.2f} mo, R2={r2:.3f})")
