# Replication

## Overview

This directory contains replication materials for reproducing the results of
Mobilitetsmodellen v0.1.0 on the synthetic data fixtures.

## Prerequisites

```bash
uv sync --all-extras
python scripts/make_synthetic_panel.py
```

## Run All Replication Steps

```bash
bash replication/run_all.sh
```

Dry-run (checks syntax and file existence without executing):

```bash
bash replication/run_all.sh --dry-run
```

## Expected Receipts

`expected_receipts.json` contains SHA-256 checksums of key output files. To verify:

```bash
python scripts/compare_receipts.py
```

## Replication Environment

Python 3.12, Ubuntu 22.04 LTS, OMP_NUM_THREADS=1, OPENBLAS_NUM_THREADS=1.

For full environment specification, see `replication/environment.yml` (conda) and
`uv.lock` (pip/uv).

## Stata Replication

Stata 17.0+ required. See `stata/` directory. Convert Parquet to CSV first:

```bash
python -c "
import polars as pl
pl.read_parquet('data/synthetic/dyads.parquet').write_csv('stata_dyads.csv')
"
```

Then run from `stata/`:

```bash
stata -b do rank_rank.do
stata -b do elasticity.do
stata -b do transition_matrix.do
```

## R Replication

R 4.3+ with packages: arrow, dplyr, sandwich, lmtest. Run from repo root:

```bash
Rscript R/rank_rank_validation.R
Rscript R/shrinkage_validation.R
```
