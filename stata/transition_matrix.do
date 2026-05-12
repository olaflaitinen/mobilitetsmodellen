/*
  transition_matrix.do
  Stata replication for quintile-to-quintile transition matrix.
  Matches output of mobilitetsmodellen.estimators.transition_matrix for validation.
*/

version 17.0
set more off
set seed 19960307

import delimited using "stata_dyads.csv", clear

* --- Assign quintiles ---
xtile parent_q = parent_income, nq(5)
xtile child_q  = child_income,  nq(5)

* --- Tabulate transition matrix ---
tab parent_q child_q, row nofreq

* --- Bootstrap standard errors ---
bootstrap, reps(200) seed(7): tab parent_q child_q, row nofreq

* --- Export to matrix ---
matrix list r(table)
esttab using "../replication/stata_transition_matrix.csv", csv replace

log using "../replication/stata_transition_matrix.log", replace text
tab parent_q child_q, row
log close
