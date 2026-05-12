/*
  elasticity.do
  Stata replication code for intergenerational income elasticity (IGE) estimation.
  Matches output of mobilitetsmodellen.estimators.elasticity for validation.
*/

version 17.0
set more off
set seed 19960307

* --- Load synthetic dyads (convert Parquet to CSV first) ---
import delimited using "stata_dyads.csv", clear

* --- Drop zero and negative incomes ---
keep if child_income > 0 & parent_income > 0

* --- Log transform ---
gen log_child  = log(child_income)
gen log_parent = log(parent_income)

* --- Pooled IGE ---
reg log_child log_parent, robust
estimates store ige_pooled

* --- By cohort ---
levelsof child_birth_year, local(cohorts)
foreach c of local cohorts {
    reg log_child log_parent if child_birth_year == `c', robust
    estimates store ige_`c'
}

* --- IV variant: use lagged income as proxy (placeholder) ---
* ivregress 2sls log_child (log_parent = log_parent_lagged), robust

* --- Export ---
esttab ige_pooled using "../replication/stata_ige_pooled.csv", ///
    csv replace stats(N r2) star(* 0.10 ** 0.05 *** 0.01)

log using "../replication/stata_elasticity.log", replace text
esttab ige_*
log close
