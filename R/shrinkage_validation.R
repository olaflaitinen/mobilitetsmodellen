# shrinkage_validation.R
#
# R replication of James-Stein shrinkage for cross-validation against
# mobilitetsmodellen.geographic.empirical_bayes.

suppressPackageStartupMessages({
  library(arrow)
  library(dplyr)
})

set.seed(19960307L)

# --- Load municipality estimates (exported from Python pipeline) ---
mun_estimates <- read.csv("municipality_estimates.csv")

# --- James-Stein shrinkage ---
james_stein <- function(theta, se, ns = NULL) {
  within_var <- se^2
  if (!is.null(ns)) {
    grand_mean <- weighted.mean(theta, ns)
  } else {
    grand_mean <- mean(theta)
  }
  total_var <- var(theta)
  mean_within <- mean(within_var)
  between_var <- max(total_var - mean_within, 0)
  B <- within_var / (within_var + between_var)
  shrunken <- (1 - B) * theta + B * grand_mean
  list(shrunken = shrunken, B = B, grand_mean = grand_mean, between_var = between_var)
}

result <- james_stein(mun_estimates$estimate, mun_estimates$se, mun_estimates$n)
mun_estimates$shrunken_R <- result$shrunken
mun_estimates$shrinkage_factor_R <- result$B

# --- Compare to Python output ---
diff <- abs(mun_estimates$shrunken_R - mun_estimates$shrunken_estimate)
cat(sprintf("Max deviation from Python: %.6f\n", max(diff)))
stopifnot(max(diff) < 0.001)

write.csv(mun_estimates, "replication/R_shrinkage_validation.csv", row.names = FALSE)
message("R shrinkage validation complete.")
