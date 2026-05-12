# Mediation Analysis

## Decomposition

Causal mediation analysis decomposes the total intergenerational effect into:

- **Average controlled direct effect (ACDE)**: effect of parent rank on child rank not
  running through the mediator.
- **Average causal mediation effect (ACME)**: effect running through the mediator.

    Total = ACDE + ACME

## Mediators

| Mediator | Variable | Channel |
|----------|----------|---------|
| Education | education_level | Human capital transmission |
| Occupation | occupation_code | Social class persistence |
| Parental wealth | wealth | Liquidity constraint relief |

## Product-of-Coefficients

The current implementation uses a product-of-coefficients approach for linear mediation:

    ACDE = coef(parent_rank | child_rank, mediator, X)
    alpha = coef(parent_rank | mediator, X)
    beta = coef(mediator | child_rank, parent_rank, X)
    ACME = alpha * beta

## Limitations

The product-of-coefficients approach assumes linearity and no treatment-mediator
interaction. For nonlinear settings, a simulation-based (Imai et al.) approach is planned.

## References

- Imai, Keele, and Tingley (2010): "A General Approach to Causal Mediation Analysis."
  Psychological Methods.
- Breen and Karlson (2014): "Education and Social Mobility in Europe." European
  Sociological Review.
