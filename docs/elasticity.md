# Intergenerational Income Elasticity

## Model

The IGE is estimated as the slope in the log-log regression:

    log(child_income_i) = alpha + beta * log(parent_income_i) + epsilon_i

The slope `beta` is the intergenerational income elasticity: a 1% increase in parent
lifetime income is associated with a `beta`% increase in child lifetime income.

## Attenuation Bias

When parent income is measured over a single year, transitory variance attenuates the
estimate. The correction factor is:

    IGE_corrected = IGE_raw * (Var_perm + Var_trans) / Var_perm

where `Var_perm` is the permanent-income variance and `Var_trans` is the transitory
variance (approximated as `Var_perm / n_years`).

Set `correct_attenuation=True` and `n_years_observed=N` in `fit_elasticity()`.

## IV Variants

Instrumental-variables approaches (using lagged income or sibling income as instruments)
are planned for a future release. See `docs/deviations.md` for the current status.

## References

- Solon (1992): "Intergenerational Income Mobility in the United States."
  American Economic Review.
- Mazumder (2005): "Fortunate Sons: New Estimates of Intergenerational Mobility."
  Review of Economics and Statistics.
