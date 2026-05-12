# Cross-Country Benchmarks

## OECD IDD Harmonisation

Swedish estimates are aligned to OECD Income Distribution Database (IDD) conventions:

- Income measured as total household disposable income per equivalent adult (OECD scale).
- Life-cycle alignment at ages 35-45.
- Reference year for parental generation: 2000.

The `benchmarking.oecd.harmonise_to_oecd()` function applies these conventions.

## Benchmark Estimates

| Country | Rank-rank slope | IGE | Source |
|---------|----------------|-----|--------|
| Denmark | 0.15 | 0.15 | Eriksen and Munk (2020) |
| Finland | 0.18 | 0.18 | Bratberg et al. (2017) |
| Norway | 0.17 | 0.17 | Bratberg et al. (2017) |
| Sweden | TBD | TBD | Mobilitetsmodellen v0.1.0 |
| United Kingdom | 0.30 | 0.30 | IFS (Blanden et al.) |
| United States | 0.45 | 0.47 | Chetty et al. (2014) |

## Sources

- **Equality of Opportunity Project (US)**: Chetty, Hendren, Kline, Saez (2014).
- **IFS UK**: Blanden, Goodman, Gregg, and Machin (2004); updated by Gregg and Machin.
- **Statistics Norway**: Bratberg, Davis, Mazumder, Nybom, Raaum, and Schnitzlein (2017).
- **OECD IDD**: https://stats.oecd.org/Index.aspx?DataSetCode=IDD

## Harmonisation Notes

Cross-country comparisons require careful harmonisation of income definitions,
age-at-measurement, and equivalisation scales. Built-in benchmark figures are
approximate literature values for illustrative comparison only.
