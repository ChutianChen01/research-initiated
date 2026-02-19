# Anscombe's Quartet — Data Analysis Project

## Overview

This repository contains a complete exploratory data analysis of **Anscombe's Quartet**, a classic dataset constructed by statistician Francis Anscombe in 1973 to illustrate the importance of visualizing data before drawing conclusions.

The quartet consists of four datasets that are nearly identical in standard summary statistics (mean, variance, correlation, and regression coefficients), yet look completely different when plotted. This project computes those statistics and produces visualizations that make the differences immediately apparent.

---

## Background

Francis Anscombe created these four datasets to counter the impression that "numerical calculations are exact, but graphs are rough." The quartet is widely used in statistics education to demonstrate that:

- Summary statistics alone can be deeply misleading
- Outliers, non-linearity, and leverage points are invisible without visualization
- Exploratory data analysis (EDA) should always begin with a plot

| Dataset | Description |
|---------|-------------|
| I | Linear relationship with random noise — the "textbook" case |
| II | Non-linear (quadratic) relationship — a linear model is a poor fit |
| III | Linear relationship with one high-leverage outlier skewing the slope |
| IV | All X values are identical except one extreme point that drives the regression |

---

## Repository Structure

```
research-initiated/
├── anscombe_analysis.ipynb      # Main Jupyter notebook with full analysis
├── anscombe_plan.md             # Analysis plan (statistics, visualizations, output spec)
├── anscombe_means_variances.png # Exported bar chart: means and variances by dataset
├── anscombe_scatter_plots.png   # Exported scatter plots with regression lines (2x2 grid)
├── anscombe_quartet.tsv         # Raw data file (tab-separated)
└── README.md                    # This file
```

---

## Analysis

### Summary Statistics Computed (per dataset)

| Statistic | All four datasets |
|-----------|------------------|
| Mean of X | ≈ 9.0 |
| Mean of Y | ≈ 7.5 |
| Variance of X | ≈ 11.0 |
| Variance of Y | ≈ 4.12 |
| Correlation (r) | ≈ 0.816 |
| Regression slope | ≈ 0.5 |
| Regression intercept | ≈ 3.0 |
| R² | ≈ 0.67 |

Despite these near-identical numbers, the underlying data patterns are fundamentally different.

### Visualizations

**1. `anscombe_means_variances.png`**
Side-by-side bar charts comparing the mean and variance of X and Y across all four datasets. Confirms that the statistics are virtually indistinguishable numerically.

**2. `anscombe_scatter_plots.png`**
A 2×2 grid of scatter plots, one per dataset, each with the fitted linear regression line overlaid. Pearson r and R² are annotated on each panel. This is where the differences become obvious.

---

## Notebook Contents

The notebook `anscombe_analysis.ipynb` is organized into the following sections:

1. **Introduction** — What Anscombe's Quartet is and why it matters
2. **Data Loading** — Loaded via seaborn's built-in dataset (`sns.load_dataset('anscombe')`)
3. **Summary Statistics** — Per-group computation of mean, variance, correlation, slope, intercept, and R², displayed as a styled DataFrame
4. **Means & Variances Bar Charts** — Visual confirmation of near-identical statistics
5. **Scatter Plots with Regression Lines** — The key visualization revealing the true differences
6. **Interpretation** — Written explanation of what each dataset reveals

---

## Requirements

```
python >= 3.10
pandas
numpy
matplotlib
seaborn
scipy
jupyter
```

Install all dependencies with:

```bash
pip install pandas numpy matplotlib seaborn scipy jupyter
```

---

## Running the Notebook

```bash
jupyter notebook anscombe_analysis.ipynb
```

Or to re-execute and save outputs from the command line:

```bash
jupyter nbconvert --to notebook --execute anscombe_analysis.ipynb --output anscombe_analysis.ipynb
```

---

## Key Takeaway

> "The data may be peeked at to determine what computations to carry out."
> — Francis Anscombe, 1973

Always plot your data. Summary statistics are a starting point, not a conclusion.
