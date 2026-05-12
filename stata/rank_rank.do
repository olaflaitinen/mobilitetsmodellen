/*
  rank_rank.do
  Stata replication code for rank-rank slope estimation.
  Matches output of mobilitetsmodellen.estimators.rank_rank for validation.
*/

version 17.0
set more off
set seed 19960307

* --- Load synthetic dyads ---
import delimited using "../data/synthetic/dyads.parquet", clear
* Note: convert Parquet to CSV first:
*   python -c "import polars as pl; pl.read_parquet('data/synthetic/dyads.parquet').write_csv('stata_dyads.csv')"

* --- Rank-rank pooled ---
reg child_rank parent_rank, robust
estimates store rank_rank_pooled

* --- Rank-rank by birth cohort ---
levelsof child_birth_year, local(cohorts)
foreach c of local cohorts {
    reg child_rank parent_rank if child_birth_year == `c', robust
    estimates store rank_rank_`c'
}

* --- Export results ---
esttab rank_rank_pooled using "../replication/stata_rank_rank_pooled.csv", ///
    csv replace stats(N r2 rmse) star(* 0.10 ** 0.05 *** 0.01)

log using "../replication/stata_rank_rank.log", replace text
esttab rank_rank_*
log close
