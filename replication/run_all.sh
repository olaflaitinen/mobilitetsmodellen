#!/usr/bin/env bash
# run_all.sh -- Execute full replication pipeline.
# Usage: bash replication/run_all.sh [--dry-run]

set -euo pipefail

DRY_RUN=0
for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY_RUN=1 ;;
    esac
done

step() {
    echo "==> $*"
    if [ "$DRY_RUN" -eq 0 ]; then
        "$@"
    else
        echo "    (dry-run: skipping)"
    fi
}

echo "Mobilitetsmodellen replication pipeline"
echo "DRY_RUN=${DRY_RUN}"
echo "----------------------------------------"

step python scripts/make_synthetic_panel.py

step uv run python -m mobilitetsmodellen.estimators.rank_rank 2>/dev/null || true

echo "Rank-rank estimation..."
step uv run python - <<'EOF'
import pathlib
import json
import numpy as np
import pandas as pd
import polars as pl
from mobilitetsmodellen.estimators.rank_rank import fit_rank_rank
dyads = pl.read_parquet("data/synthetic/dyads.parquet").to_pandas()
results = fit_rank_rank(dyads, child_rank_col="child_rank", parent_rank_col="parent_rank")
out = {"slope": results[0].slope, "se": results[0].se, "n": results[0].n}
print(json.dumps(out, indent=2))
pathlib.Path("replication/actual_receipts").mkdir(exist_ok=True)
pathlib.Path("replication/actual_receipts/rank_rank.json").write_text(json.dumps(out))
EOF

echo "DoubleML estimation..."
step uv run python - <<'EOF'
import pathlib
import json
import polars as pl
from mobilitetsmodellen.estimators.double_ml import fit_double_ml
dyads = pl.read_parquet("data/synthetic/dyads.parquet").to_pandas()
result = fit_double_ml(dyads, child_rank_col="child_rank", parent_rank_col="parent_rank",
                       n_folds=2, learner="random-forest", seed=13)
out = {"theta": result.theta, "se": result.se, "n": result.n}
print(json.dumps(out, indent=2))
pathlib.Path("replication/actual_receipts").mkdir(exist_ok=True)
pathlib.Path("replication/actual_receipts/double_ml.json").write_text(json.dumps(out))
EOF

step python scripts/compare_receipts.py

echo "----------------------------------------"
echo "Replication pipeline complete."
