# Anscombe Plan

## Summary Statistics (per group I, II, III, IV)
- Mean of x and y
- Variance of x and y
- Correlation between x and y
- Linear regression coefficients (slope and intercept)
- R-squared value

## Visualizations
- 2x2 grid of scatter plots, one per dataset, each with the fitted regression line overlaid
- Bar chart comparing means of x and y across groups
- Bar chart comparing variances of x and y across groups
- Summary statistics table rendered as a styled DataFrame

## Output
A Jupyter notebook (`anscombe_analysis.ipynb`) containing:
1. Introduction cell explaining Anscombe's Quartet
2. Data loading cell (using seaborn's built-in dataset)
3. Summary statistics computation and display
4. All visualizations with titles and labels
5. Interpretation cell explaining why identical statistics can hide very different data patterns
