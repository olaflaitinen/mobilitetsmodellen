# Rank-Rank Slope

## Model

The rank-rank slope is estimated by:

    child_rank_i = alpha + beta * parent_rank_i + epsilon_i

where ranks are computed within birth cohort on the national income distribution.
The slope `beta` measures intergenerational persistence: 0 = perfect mobility,
1 = complete rigidity.

## Standard Errors

By default, heteroscedasticity-consistent (HC3) standard errors are used. When a
cluster column is provided (e.g. municipality), cluster-robust standard errors are
computed by the sandwich estimator.

## Cohort Interactions

Setting `cohort_col` fits separate slopes per birth cohort. This reveals whether
mobility has changed across generations, addressing Research Question 1.

## Absolute Upward Mobility

Chetty et al. (2014) define absolute upward mobility as the expected rank of a child
born to parents at the 25th percentile. From the rank-rank regression:

    AUM = alpha + 0.25 * beta

This is computed automatically from the rank-rank result.

## Bootstrap Inference

Bootstrap standard errors are available via `evaluation.bootstrap.bootstrap_ci`.

## References

- Chetty, Hendren, Kline, and Saez (2014): "Where is the Land of Opportunity?"
  Quarterly Journal of Economics.
- Bratberg et al. (2017): "A Comparison of Intergenerational Mobility Curves in
  Germany, Norway, Sweden, and the US." Scandinavian Journal of Economics.
