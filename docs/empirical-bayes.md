# Empirical Bayes Shrinkage

## Motivation

Municipality-level (kommun-level) rank-rank estimates have large sampling variance when
the municipality is small. Naive estimates can be misleading; empirical-Bayes shrinkage
borrows strength across municipalities to stabilise estimates.

## James-Stein Shrinkage

The James-Stein estimator shrinks group-level estimates toward the grand mean:

    theta_j_shrunk = (1 - B_j) * theta_j_raw + B_j * mu

where the shrinkage factor is:

    B_j = sigma2_j / (sigma2_j + tau2)

- `sigma2_j = se_j^2` is the within-municipality sampling variance.
- `tau2` is the between-municipality variance, estimated by method of moments.
- `mu` is the weighted grand mean.

## Key Properties

- Shrinkage factor `B_j` is monotone decreasing in `n_j` (larger municipalities
  shrink less).
- Shrinkage factor `B_j` is monotone decreasing in `tau2` (more between-group
  variance means less shrinkage toward the mean).

## Spatial Bayes

An alternative prior models spatial correlation across municipalities using a
Gaussian-Markov random field. This is available via `shrinkage="spatial"` in Config.
See `geographic.spatial` and `geographic.empirical_bayes` for implementation.

## References

- James and Stein (1961): "Estimation with Quadratic Loss." Berkeley Symposium.
- Chetty and Hendren (2018): "The Impacts of Neighborhoods on Intergenerational
  Mobility." Quarterly Journal of Economics.
