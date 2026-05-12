# rank_rank_validation.R
#
# R replication of rank-rank slope estimation for cross-validation against
# mobilitetsmodellen.estimators.rank_rank.
#
# Requires: arrow, dplyr, sandwich, lmtest

suppressPackageStartupMessages({
  library(arrow)
  library(dplyr)
  library(sandwich)
  library(lmtest)
})

set.seed(19960307L)

# --- Load synthetic dyads ---
dyads <- read_parquet("data/synthetic/dyads.parquet")

# --- Pooled rank-rank ---
model_pooled <- lm(child_rank ~ parent_rank, data = dyads)
coeftest(model_pooled, vcov = vcovHC(model_pooled, type = "HC3"))

# --- Clustered standard errors by kommun_code ---
model_cluster <- lm(child_rank ~ parent_rank, data = dyads)
coeftest(model_cluster, vcov = vcovCL(model_cluster, cluster = ~kommun_code, data = dyads))

# --- By cohort ---
cohort_results <- dyads |>
  group_by(child_birth_year) |>
  summarise(
    slope = coef(lm(child_rank ~ parent_rank))[2],
    n = n(),
    .groups = "drop"
  )
print(cohort_results)

# --- Export ---
write.csv(
  cohort_results,
  "replication/R_rank_rank_cohorts.csv",
  row.names = FALSE
)
message("R rank-rank validation complete.")
