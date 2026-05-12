# Methodology Overview

## Mobility Concepts

Intergenerational income mobility captures the degree to which children's economic outcomes
depend on their parents' position in the income distribution. Low mobility (high persistence)
implies strong intergenerational transmission of economic status; high mobility implies greater
equality of opportunity.

The framework implements four estimator families:

1. **Rank-rank slope** (relative mobility): OLS regression of child income rank on parent
   income rank within birth cohort. Varies from 0 (perfect mobility) to 1 (no mobility).
2. **Intergenerational income elasticity (IGE)**: log-log regression; interpreted as percent
   increase in child lifetime income per one-percent increase in parent lifetime income.
3. **Transition matrix**: quintile-to-quintile probabilities; absolute upward mobility is
   P(child quintile >= Q3 | parent quintile = Q1).
4. **Double machine learning (DoubleML)**: orthogonal score with LGBM/XGBoost nuisance
   learners; accounts for nonlinear confounding in high-dimensional covariate settings.

## Identification

Identification rests on the assumption that, conditional on observable life-cycle age and
controls, the parent income rank is as good as randomly assigned within birth cohort. This is
not strictly satisfied; the methodology page documents the identifying assumptions and
limitations of each estimator.

## Life-Cycle Alignment

Income observations are constructed at canonical ages 35-45 for both generations.
See [Life-Cycle Alignment](life-cycle-alignment.md).

## Geographic Heterogeneity

Municipality-level estimates are stabilised via empirical-Bayes shrinkage.
See [Empirical Bayes](empirical-bayes.md) and [Mobility Atlas](mobility-atlas.md).

## Limitations

- Confounding by unobserved parental characteristics (assortative mating, parental wealth).
- Attenuation bias when short income windows are used; partially addressed by the averaging
  window and IV variants in the IGE estimator.
- Selection into the register (immigrants, emigrants).
- Municipality-level mobility reflects both causal neighbourhood effects and sorting.
