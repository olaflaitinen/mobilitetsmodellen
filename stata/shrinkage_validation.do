/*
  shrinkage_validation.do
  Stata validation of James-Stein shrinkage against Python implementation.
  Compares shrunken estimates from mobilitetsmodellen.geographic.empirical_bayes.
*/

version 17.0
set more off

* --- Load municipality-level estimates (exported from Python) ---
import delimited using "municipality_estimates.csv", clear
* Columns: region, estimate, se, n, shrunken_estimate (from Python)

* --- Compute grand mean (weighted by sample size) ---
summarize estimate [aw=n]
local mu = r(mean)
local overall_var = r(Var)

* --- Compute between-group variance (method of moments) ---
* tau2 = Var(theta_j) - mean(se_j^2)
gen se2 = se^2
summarize se2
local mean_within = r(mean)
local tau2 = max(`overall_var' - `mean_within', 0)

* --- Compute shrinkage factors ---
gen B_j = se2 / (se2 + `tau2')
gen shrunken_stata = (1 - B_j) * estimate + B_j * `mu'

* --- Compare to Python shrunken estimates ---
gen diff = abs(shrunken_stata - shrunken_estimate)
summarize diff
assert r(max) < 0.001

log using "../replication/stata_shrinkage_validation.log", replace text
list region estimate shrunken_stata shrunken_estimate diff in 1/10
log close
