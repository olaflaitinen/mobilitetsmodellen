# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2024-01-01

### Added

- Initial release of Mobilitetsmodellen.
- Classical rank-rank slope estimator with cluster-robust standard errors and cohort interactions.
- Intergenerational income elasticity (IGE) estimator with attenuation-bias correction.
- Quintile-to-quintile transition-matrix estimator with bootstrap standard errors.
- Double machine learning (DoubleML) estimator with LGBM and XGBoost nuisance learners.
- Causal forest estimator wrapping EconML with honest splits and cross-fitting.
- Causal mediation analysis decomposing education, occupation, and parental-wealth channels.
- Life-cycle alignment module for canonical age-window construction (ages 35-45).
- Geographic aggregation at kommun, lan, and FA-region levels.
- Empirical-Bayes James-Stein shrinkage for municipality-level estimates.
- Spatial correlation adjustments using Moran's I and SAR/SEM models.
- Cross-country benchmarking against OECD IDD, Equality of Opportunity Project, IFS UK, and
  Statistics Norway.
- Interactive mobility atlas with WCAG 2.2 AA accessibility compliance.
- Synthetic panel generator (SYNTHETIC_SEED=19960307) with 100000 parent-child dyads.
- SHA-256-based deterministic cross-fitting fold assignment.
- Structured logging via structlog.
- Pydantic v2 configuration model.
- Typer CLI with subcommands for each pipeline stage.
- Full REUSE 3.0 compliance via DEP5.
- EUPL-1.2 licence.
- CITATION.cff and .zenodo.json metadata.
- MkDocs Material documentation with API auto-generation via mkdocstrings.
- GitHub Actions CI/CD matrix across Ubuntu 22.04, macOS 14, and Windows 2022.

[Unreleased]: https://github.com/olaflaitinen/mobilitetsmodellen/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/olaflaitinen/mobilitetsmodellen/releases/tag/v0.1.0
