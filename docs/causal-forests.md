# Causal Forests

## Method

Causal forests (Wager and Athey, 2018; Athey and Imbens, 2019) estimate heterogeneous
treatment effects:

    CATE(x) = E[Y(1) - Y(0) | X = x]

In the mobility context, the "treatment" is parent rank and the outcome is child rank.
The CATE surface reveals which subpopulations (by covariate profile) show higher or lower
intergenerational persistence.

## Honest Splits

Honest estimation splits the sample into a training half (for tree structure) and an
estimation half (for leaf-level CATE computation). This prevents overfitting of the
effect estimate to the structure-selection sample.

## Cross-Fitting

The implementation wraps EconML's `CausalForest` with `honest=True` and derives the
random state from `seeds.derive_seed("forest_init", seed)`.

## Heterogeneity Targets

The `heterogeneity_cols` argument specifies the covariate space over which CATE is
estimated. Candidate targets include:

- Municipality fixed effects (geographic heterogeneity)
- Education of the child generation
- Parental wealth quintile
- Cohort birth year

## References

- Wager and Athey (2018): "Estimation and Inference of Heterogeneous Treatment Effects."
  JASA.
- Athey, Tibshirani, and Wager (2019): "Generalized Random Forests." Annals of Statistics.
