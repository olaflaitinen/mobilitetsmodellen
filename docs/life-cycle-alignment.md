# Life-Cycle Alignment

## The Life-Cycle Bias Problem

Measuring income at non-peak ages introduces attenuation bias into IGE and rank-rank
estimates. Income at age 25 poorly predicts lifetime income; income at age 50 may reflect
mean reversion. The canonical solution is to measure income at ages 35-45.

## Implementation

The `alignment.life_cycle.align()` function:

1. Filters the panel to the specified age range (default: ages 35-45 inclusive).
2. Applies an averaging window to reduce transitory income variance.
3. Returns one observation per individual representing their aligned income.

The averaging window options are:

| Window | Width | Ages included (centred at 40) |
|--------|-------|-------------------------------|
| single | 1 | 40 |
| three | 3 | 39, 40, 41 |
| five | 5 | 38, 39, 40, 41, 42 |

## Sensitivity Analyses

The `alignment_window` configuration parameter controls which window is used. Reporting
should include sensitivity analyses across all three window widths.

## References

- Haider and Solon (2006): "Life-Cycle Variation in the Association between Current and
  Lifetime Earnings." American Economic Review.
- Nybom and Stuhler (2017): "Biases in Standard Measures of Intergenerational Income
  Dependence." Journal of Human Resources.
