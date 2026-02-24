"""
Phylogenetic distribution figure: cellulosomes and homologous protein systems in Bacteroidota.

Since sequence-level phylogenetics requires external tools (MAFFT, IQ-TREE, etc.), this script
produces an annotated cladogram based on the taxonomic relationships and surface-complex
strategies documented in the literature (2016-2026).

Data sources:
  - Minor et al. Front Microbiol 2024 (genome-wide survey, 305 k genomes)
  - McKee et al. Environ Microbiol Rep 2021 (PUL nomenclature review)
  - Zhivin et al. Biotechnol Biofuels 2017 (P. cellulosolvens cellulosome)
  - Wang et al. AEM 2017 (Cytophaga hutchinsonii OMP complex)

Run:  python phylogeny_tree.py
Output: phylogeny_tree.png
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import numpy as np

# ------------------------------------------------------------------
# Cladogram data
# Each entry: (y_position, indent_level, label, system_type, notes)
# system_type -> color
# ------------------------------------------------------------------
SYSTEM_COLORS = {
    "True cellulosome":       "#E53935",   # red
    "PUL / Sus-like":         "#1E88E5",   # blue
    "T9SS surface display":   "#43A047",   # green
    "Novel OMP complex":      "#FB8C00",   # orange
    "None / Free enzymes":    "#9E9E9E",   # grey
}

# (label, indent, system, key_proteins, note)
nodes = [
    # Root
    ("Bacteroidota (phylum)",           0, "PUL / Sus-like",
     "SusC / SusD ubiquitous", "All sequenced genomes encode SusC/SusD-like pairs"),

    # Class Bacteroidia
    ("  Bacteroidia (class)",           1, "PUL / Sus-like",
     "SusC/SusD (100s of PULs)", "Dominant strategy: PUL-based surface complexes"),
    ("    Bacteroidaceae",              2, "PUL / Sus-like",
     "SusC/D, SusG (GH13), BT2159", ""),
    ("      Bacteroides thetaiotaomicron", 3, "PUL / Sus-like",
     "Sus operon; ~100 PULs", "Model organism for PUL-based polysaccharide utilisation"),
    ("      Bacteroides ovatus",        3, "PUL / Sus-like",
     "Xyloglucan PUL (BACOVA_04503)", "PUL diversity; 2014 Nature paper"),
    ("      Bacteroides uniformis",     3, "PUL / Sus-like",
     "23 PULs (CRISPR screen)", "Cell Host Microbe 2022"),
    ("    Bacteroidaceae (anaerobic cellulolytic)", 2, "True cellulosome",
     "ScaA1, ScaB, 78 cohesins, >200 dockerins",
     "ONLY Bacteroidota with confirmed canonical cellulosome"),
    ("      Pseudobacteroides cellulosolvens", 3, "True cellulosome",
     "ScaA1–ScaP scaffoldins; RsgI4 (PDB:7CG5)",
     "Most complex cellulosome known (110 enzymes/complex); reversed Coh type I/II"),
    ("    Prevotellaceae",              2, "PUL / Sus-like",
     "SusC/D-like; arabinoxylan PUL",
     "No cohesin/dockerin found across 4 P. copri clades"),
    ("      Prevotella copri (4 clades)",3, "PUL / Sus-like",
     "Arabinoxylan / arabinan / galactan PULs",
     "Tett et al. 2019; EMBO J 2021"),
    ("    Porphyromonadaceae",          2, "T9SS surface display",
     "PorU sortase, PorV lipoprotein, RagA/B",
     "T9SS + remnant PUL/Sus system"),
    ("      Porphyromonas gingivalis",  3, "T9SS surface display",
     "Gingipains (T9SS); RagB (SusD-like)",
     "PNAS 2022: T9SS supramolecular caged-ring architecture"),
    ("    Tannerellaceae",              2, "T9SS surface display",
     "TfsA/TfsB S-layer (T9SS-anchored)",
     "S-layer as scaffoldin analog"),
    ("      Tannerella forsythia",      3, "T9SS surface display",
     "TfsA, TfsB (T9SS surface lattice)",
     "Periodontal pathogen; S-layer enzyme display"),

    # Class Flavobacteriia
    ("  Flavobacteriia (class)",        1, "T9SS surface display",
     "T9SS (GldJ/K/L/M/N/SprA)", "T9SS + gliding motility are the dominant strategies"),
    ("    Flavobacteriaceae",           2, "T9SS surface display",
     "SprB, ChiA, FlGH17A (T9SS-delivered)",
     "T9SS delivers diverse CAZymes + adhesins to outer membrane"),
    ("      Flavobacterium johnsoniae", 3, "T9SS surface display",
     "SprB (669 kDa adhesin), GldJ scaffold, ChiA, GH17A",
     "Textbook T9SS organism; closest to cellulosome-like surface display"),
    ("    Flavobacteriaceae (marine)",  2, "T9SS surface display",
     "PUL + T9SS (SusC/D expression in blooms)",
     "ISME J 2018: SusC/D protein expression predicts phytoplankton glycan utilisation"),
    ("      Cellulophaga lytica",       3, "T9SS surface display",
     "T9SS + PUL hybrid",
     "Both systems co-occur in some marine Flavobacteriia"),

    # Class Cytophagia
    ("  Cytophagia (class)",            1, "Novel OMP complex",
     "CHU_3220, CHU_1279 (novel OMP)", "Neither canonical PUL nor cellulosome; contact-dependent"),
    ("    Cytophagaceae",               2, "Novel OMP complex",
     "CHU_3220 (crystalline cellulose); Cel5B/Cel9C (periplasm)",
     "No cellulosome; no secreted free cellulases; novel surface OMP complex"),
    ("      Cytophaga hutchinsonii",    3, "Novel OMP complex",
     "CHU_3220, CHU_1279, Cbp2 (GH9), Cel9C",
     "Wang et al. 2017; 2024: third independent strategy for crystalline cellulose"),
    ("    Spirosomaceae",               2, "PUL / Sus-like",
     "SusC/D (diverse polysaccharides)",
     "Mainly PUL-based; no T9SS or cellulosome"),

    # Class Sphingobacteriia
    ("  Sphingobacteriia (class)",      1, "PUL / Sus-like",
     "SusC/D-like",
     "PUL-based; sparse data; no cellulosome reported"),
    ("    Saprospiraceae",              2, "None / Free enzymes",
     "Free GHs + some PUL elements",
     "Mostly free enzymes; wastewater treatment isolates"),
]

# ------------------------------------------------------------------
# Figure
# ------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(18, 13),
                         gridspec_kw={"width_ratios": [3, 1]})
fig.patch.set_facecolor("#FAFAFA")

ax_tree = axes[0]
ax_legend = axes[1]

n = len(nodes)
y_positions = list(range(n, 0, -1))

# Draw branch lines
for i, (label, indent, system, proteins, note) in enumerate(nodes):
    y = y_positions[i]
    color = SYSTEM_COLORS[system]
    x_start = indent * 0.6
    x_end = x_start + 0.45

    # Horizontal tick
    ax_tree.plot([x_start, x_end], [y, y], color=color, lw=2, solid_capstyle="round")

    # Vertical connection to parent
    if i > 0:
        # Find parent (first node above with indent - 1)
        parent_indent = indent - 1
        for j in range(i - 1, -1, -1):
            if nodes[j][1] == parent_indent:
                y_parent = y_positions[j]
                ax_tree.plot([x_start, x_start], [y, y_parent],
                             color="#BDBDBD", lw=0.8, zorder=0)
                break

    # Marker
    marker = "D" if system == "True cellulosome" else "o"
    markersize = 10 if system == "True cellulosome" else 7
    ax_tree.plot(x_end, y, marker=marker, color=color,
                 markersize=markersize, zorder=3,
                 markeredgecolor="white", markeredgewidth=0.7)

    # Text label
    fontweight = "bold" if indent <= 1 else ("semibold" if indent == 2 else "normal")
    fontsize = 10 if indent == 0 else (9 if indent == 1 else (8.5 if indent == 2 else 8))
    ax_tree.text(x_end + 0.08, y, label.strip(),
                 va="center", ha="left", fontsize=fontsize,
                 fontweight=fontweight, color="#212121")

    # Key proteins annotation (right side)
    ax_tree.text(10.5, y, proteins, va="center", ha="left",
                 fontsize=7, color=color, style="italic")

ax_tree.set_xlim(-0.2, 16)
ax_tree.set_ylim(0.2, n + 0.8)
ax_tree.axis("off")
ax_tree.set_title(
    "Phylogenetic Distribution of Cellulosomes and Functional Analogs in Bacteroidota\n"
    "(Based on literature survey 2016–2026; Minor et al. 2024; McKee et al. 2021)",
    fontsize=11, fontweight="bold", pad=10
)

# Vertical divider between tree and protein column
ax_tree.axvline(x=10.2, color="#BDBDBD", lw=0.5, ls="--")
ax_tree.text(10.5, n + 0.5, "Key Proteins / Features", fontsize=8,
             fontweight="bold", ha="left", color="#424242")

# ------------------------------------------------------------------
# Legend panel
# ------------------------------------------------------------------
ax_legend.axis("off")

legend_title = "Surface Polysaccharide Degradation Strategy"
ax_legend.text(0.05, 0.98, legend_title, fontsize=10, fontweight="bold",
               va="top", ha="left", transform=ax_legend.transAxes)

legend_items = [
    ("True cellulosome\n(cohesin–dockerin–scaffoldin)", "True cellulosome", "D"),
    ("PUL / Sus-like complex\n(SusC/D outer membrane)", "PUL / Sus-like", "o"),
    ("T9SS surface display\n(CTD-signal/A-LPS anchoring)", "T9SS surface display", "o"),
    ("Novel OMP complex\n(contact-dependent; Cytophaga)", "Novel OMP complex", "o"),
    ("None / Free enzymes\n(secreted GHs only)", "None / Free enzymes", "o"),
]

y_leg = 0.88
for text, stype, marker in legend_items:
    color = SYSTEM_COLORS[stype]
    ax_legend.plot(0.08, y_leg, marker=marker, color=color, markersize=10,
                   transform=ax_legend.transAxes, markeredgecolor="white",
                   markeredgewidth=0.5)
    ax_legend.text(0.18, y_leg, text, fontsize=8.5, va="center", ha="left",
                   transform=ax_legend.transAxes, color="#212121")
    y_leg -= 0.13

# Key conclusions box
conclusions = (
    "Key Conclusions\n"
    "─────────────────────────────────\n"
    "• TRUE cellulosomes (cohesin/dockerin/scaffoldin)\n"
    "  confirmed in ONLY 1 Bacteroidota species:\n"
    "  Pseudobacteroides cellulosolvens\n\n"
    "• PUL/SusC/SusD complexes are the universal\n"
    "  Bacteroidota functional analog — present\n"
    "  in ALL classes; most diverse in Bacteroidia\n\n"
    "• T9SS surface display is the second major\n"
    "  functional analog (Flavobacteriia +\n"
    "  Porphyromonadaceae + Tannerellaceae)\n\n"
    "• C. hutchinsonii OMP complex represents\n"
    "  a third independent strategy — molecular\n"
    "  identity still under investigation\n\n"
    "• No cohesin/dockerin genes found in\n"
    "  305,693-genome survey outside\n"
    "  P. cellulosolvens (Minor et al. 2024)"
)

ax_legend.text(0.05, 0.30, conclusions, fontsize=8, va="top", ha="left",
               transform=ax_legend.transAxes, color="#212121",
               bbox=dict(boxstyle="round,pad=0.5", facecolor="#E3F2FD",
                         edgecolor="#90CAF9", linewidth=1),
               family="monospace")

plt.tight_layout(pad=1.5)
plt.savefig("phylogeny_tree.png", dpi=150, bbox_inches="tight",
            facecolor=fig.get_facecolor())
print("Saved phylogeny_tree.png")
