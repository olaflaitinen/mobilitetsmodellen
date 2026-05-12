# Double Machine Learning

## Method

Double ML (Chernozhukov et al., 2018) estimates the partially linear regression:

    Y = theta * D + g(X) + epsilon
    D = m(X) + v

where `Y` is child rank, `D` is parent rank, and `X` is a high-dimensional covariate
vector. The orthogonal score construction debiases the estimate by partialling out `X`
using cross-fitted nuisance functions.

## Cross-Fitting

The sample is split into `n_folds` folds (default 5). For each fold `k`:

1. Estimate nuisance functions `g` and `m` on the training folds.
2. Form residuals `Y_tilde = Y - g_hat(X)` and `D_tilde = D - m_hat(X)` on fold `k`.

The final estimate is `theta = mean(D_tilde * Y_tilde) / mean(D_tilde^2)`.

## Fold Assignment

Fold assignment uses SHA-256 hashing of stable individual identifiers:

    fold = SHA256("fold_assignment:{seed}:{pid}")[:4] % n_folds

This guarantees identical fold assignments across platforms and Python versions.
See `seeds.derive_seed` and `estimators.double_ml._make_fold_assignments`.

## Nuisance Learners

| Learner | Class | Notes |
|---------|-------|-------|
| lightgbm | LGBMRegressor | Default; fast, accurate |
| xgboost | XGBRegressor | Alternative; GPU-compatible |
| random-forest | RandomForestRegressor | sklearn; no extra dependency |

## References

- Chernozhukov, Chetverikov, Demirer, Duflo, Hansen, Newey, Robins (2018):
  "Double/Debiased Machine Learning." Econometrics Journal.
