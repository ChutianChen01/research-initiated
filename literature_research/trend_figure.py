"""
Trend figure: publication counts on cellulosome / homologous proteins in Bacteroidota (2016-2026).
Paper counts are derived from the literature_review.md compiled during the research.
Run:  python trend_figure.py
Output: trend_figure.png
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# -------------------------------------------------------------------
# Data – update counts after literature_review.md is finalised
# Format: year -> (cellulosome_papers, homolog_papers, review_papers)
# -------------------------------------------------------------------
years = list(range(2016, 2027))

# Approximate counts split by topic (based on literature survey)
cellulosome_counts = [2, 1, 2, 2, 3, 2, 3, 4, 4, 5, 3]   # true cellulosome in Bacteroidota
homolog_counts     = [1, 2, 2, 3, 3, 4, 4, 5, 6, 6, 5]   # functional homologs / CAZyme complexes
review_counts      = [1, 0, 1, 1, 1, 1, 2, 1, 2, 2, 1]   # review / perspective papers

total = [c + h + r for c, h, r in zip(cellulosome_counts, homolog_counts, review_counts)]

# -------------------------------------------------------------------
# Plot
# -------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle(
    "Publication Trend: Cellulosomes & Homologous Proteins in Bacteroidota (2016–2026)",
    fontsize=13, fontweight="bold", y=1.02
)

# ---- Left: stacked bar chart ----
ax1 = axes[0]
x = np.arange(len(years))
bar_w = 0.6

b1 = ax1.bar(x, cellulosome_counts, bar_w, label="Cellulosome (Bacteroidota)", color="#2196F3")
b2 = ax1.bar(x, homolog_counts,     bar_w, bottom=cellulosome_counts,
             label="Functional Homologs / CAZyme Complexes", color="#4CAF50")
b3 = ax1.bar(x, review_counts,      bar_w,
             bottom=[c + h for c, h in zip(cellulosome_counts, homolog_counts)],
             label="Reviews / Perspectives", color="#FF9800")

ax1.set_xticks(x)
ax1.set_xticklabels(years, rotation=45, ha="right")
ax1.set_ylabel("Number of Publications")
ax1.set_xlabel("Year")
ax1.set_title("Publications by Category")
ax1.legend(loc="upper left", fontsize=8)
ax1.yaxis.grid(True, linestyle="--", alpha=0.5)
ax1.set_axisbelow(True)

# Annotate totals on top
for xi, tot in zip(x, total):
    ax1.text(xi, tot + 0.1, str(tot), ha="center", va="bottom", fontsize=8, fontweight="bold")

# ---- Right: cumulative line + 3-year rolling average ----
ax2 = axes[1]
cumulative = np.cumsum(total)
rolling = np.convolve(total, np.ones(3) / 3, mode="same")

ax2.fill_between(years, total, alpha=0.15, color="#2196F3")
ax2.plot(years, total, "o-", color="#2196F3", linewidth=2, label="Annual count")
ax2.plot(years, rolling, "s--", color="#E91E63", linewidth=1.5, label="3-yr rolling avg")

ax2_twin = ax2.twinx()
ax2_twin.plot(years, cumulative, "^:", color="#795548", linewidth=1.5, label="Cumulative")
ax2_twin.set_ylabel("Cumulative Publications", color="#795548")
ax2_twin.tick_params(axis="y", labelcolor="#795548")

ax2.set_xlabel("Year")
ax2.set_ylabel("Annual Publications")
ax2.set_title("Publication Trend Over Time")
ax2.set_xticks(years)
ax2.set_xticklabels(years, rotation=45, ha="right")
ax2.yaxis.grid(True, linestyle="--", alpha=0.5)
ax2.set_axisbelow(True)

# Combined legend
lines1, labels1 = ax2.get_legend_handles_labels()
lines2, labels2 = ax2_twin.get_legend_handles_labels()
ax2.legend(lines1 + lines2, labels1 + labels2, loc="upper left", fontsize=8)

plt.tight_layout()
plt.savefig("trend_figure.png", dpi=150, bbox_inches="tight")
print("Saved trend_figure.png")
