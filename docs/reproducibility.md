# Reproducibility

## Seeds

| Constant | Value | Namespace | Usage |
|----------|-------|-----------|-------|
| SYNTHETIC_SEED | 19960307 | - | Synthetic panel generation |
| MODEL_SEED | 20251008 | - | Global random state |
| CROSSFIT_SEED | 13 | fold_assignment | DoubleML cross-fitting |
| FOREST_SEED | 123 | forest_init | Causal forest initialisation |
| BOOTSTRAP_SEED | 7 | bootstrap_sample | Bootstrap replicates |
| ATLAS_SEED | 31 | atlas_jitter | Atlas jitter |

All seeds are derived via `seeds.derive_seed(namespace, base)` which applies SHA-256 hashing
of a `namespace:base` string and returns the first 4 bytes as a 32-bit integer.

## Deterministic Fold Assignment

Cross-fitting fold assignment in `estimators.double_ml` uses SHA-256 hashing of stable
individual identifiers (PIDs), not random shuffling. This guarantees identical fold
assignments across platforms independent of OS random-state initialisation.

The fold for individual `pid` is:

    fold = SHA256("fold_assignment:{seed}:{pid}")[:4] % n_folds

## BLAS and Threading

Set `OMP_NUM_THREADS=1` and `OPENBLAS_NUM_THREADS=1` when comparing cross-platform outputs
from causal forest and DoubleML estimators. Floating-point accumulation order may differ
across thread counts, introducing differences beyond 1e-6. Document any such differences in
`replication/expected_receipts.json`.

## Container Reproducibility

A reference container environment is specified in `replication/README.md`. The container
hash is committed alongside expected output checksums in `replication/expected_receipts.json`.

## Verification

```bash
python scripts/make_synthetic_panel.py --check
bash replication/run_all.sh --dry-run
python scripts/compare_receipts.py
```
