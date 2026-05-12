# Mobilitetsmodellen

**Department of Economics, Stockholm University** | Research Software | EUPL-1.2

[![CI](https://github.com/olaflaitinen/mobilitetsmodellen/actions/workflows/ci.yml/badge.svg)](https://github.com/olaflaitinen/mobilitetsmodellen/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/olaflaitinen/mobilitetsmodellen/branch/main/graph/badge.svg)](https://codecov.io/gh/olaflaitinen/mobilitetsmodellen)
[![REUSE compliant](https://api.reuse.software/badge/github.com/olaflaitinen/mobilitetsmodellen)](https://api.reuse.software/info/github.com/olaflaitinen/mobilitetsmodellen)
[![DOI](https://zenodo.org/badge/latestdoi/olaflaitinen/mobilitetsmodellen.svg)](https://zenodo.org/record/olaflaitinen/mobilitetsmodellen)

## Abstract

Mobilitetsmodellen is a production-grade Python research-software library for estimating
intergenerational income and rank mobility in Sweden. It links the multi-generational register
(Flergenerationsregistret) to the LISA panel and tax registers, with explicit attention to
municipality-level (kommun) and cohort-level heterogeneity across birth cohorts since 1960.

The framework integrates four complementary families of estimators. Classical estimators include
the rank-rank slope (regression of child income rank on parent income rank within cohort) with
cluster-robust standard errors and cohort interactions, the intergenerational income elasticity
(IGE) in log-log form with attenuation-bias correction, and quintile-to-quintile transition
matrices with bootstrap standard errors. Modern causal estimators include double machine
learning (DoubleML) with orthogonal score construction and LGBM or XGBoost nuisance learners
under SHA-256-deterministic cross-fitting, and generalised random forests via EconML with
honest splits. A formal causal-mediation module decomposes total intergenerational persistence
into direct effects and indirect effects running through educational attainment, occupational
status, and parental wealth. Income observations are constructed at canonical life-cycle ages
35-45 for both generations to address life-cycle bias, with sensitivity analyses to averaging
windows and to attenuation from transitory income shocks. Empirical-Bayes James-Stein
shrinkage stabilises municipality-level estimates against small-sample noise and supports an
interactive WCAG 2.2 AA-compliant mobility atlas. Cross-country benchmarking modules align
Swedish results with the OECD Income Distribution Database and with mobility benchmarks from
the Equality of Opportunity Project (United States), IFS (United Kingdom), and Statistics
Norway.

## Compliance Matrix

| Standard | Status |
|----------|--------|
| EUPL-1.2 | Sole licence |
| GDPR (EU) 2016/679 Art. 6.1.e + 9.2.j | Documented in docs/gdpr.md |
| OSOR good practice | Registered |
| EC OSS Strategy 2020-2023 | Compliant |
| Interoperable Europe Act (EU) 2024/903 | Compliant |
| REUSE 3.0 (DEP5 only) | Verified by reuse lint |
| FAIR4RS | Matrix in docs/fair4rs.md |
| Swedish OSL 2009:400 ch. 24 | Documented |
| NIS2 (EU) 2022/2555 | SDLC documented in SECURITY.md |
| WCAG 2.2 AA | Atlas compliance in docs/accessibility.md |

## Installation

```bash
pip install mobilitetsmodellen
```

With uv (recommended):

```bash
uv add mobilitetsmodellen
```

Development install:

```bash
git clone https://github.com/olaflaitinen/mobilitetsmodellen.git
cd mobilitetsmodellen
uv sync --all-extras
```

## Quickstart on Synthetic Panel

```python
from mobilitetsmodellen import Config, Pipeline
from mobilitetsmodellen.seeds import set_global_seed

set_global_seed(20251008)
cfg = Config(data_root="data", estimator="rank-rank")
pipeline = Pipeline(cfg)
result = pipeline.run()
print(result)
```

Generate the synthetic panel first:

```bash
python scripts/make_synthetic_panel.py
mobilitetsmodellen rank-rank --data data/synthetic
```

## Data Policy

No real personal data, real microdata, or real kinship graphs are committed to this repository.
All fixtures are synthetic (CC0-1.0, SYNTHETIC_SEED=19960307). Access to SCB microdata
(Flergenerationsregistret, LISA, tax registers) requires SCB MONA/SAFE authorisation under
OSL 2009:400 chapter 24 and Etikprövningslagen 2003:460. See [docs/data.md](docs/data.md).

## Documentation

Full documentation: https://olaflaitinen.github.io/mobilitetsmodellen

## Citation

If you use this software, please cite it using the metadata in [CITATION.cff](CITATION.cff).

```bibtex
@software{laitinen_fredriksson_lundstrom_imanov_2024_mobilitetsmodellen,
  author  = {Laitinen-Fredriksson Lundstrom Imanov, Gustav Olaf Yunus},
  title   = {Mobilitetsmodellen: machine-learning estimators of intergenerational
             mobility in Sweden},
  year    = {2024},
  version = {0.1.0},
  license = {EUPL-1.2},
  url     = {https://github.com/olaflaitinen/mobilitetsmodellen}
}
```

## Contributing and Security

See [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), and
[GOVERNANCE.md](GOVERNANCE.md).

## Portfolio

This is module 5 of a 20-project portfolio. Sibling projects include Inkomstprognos,
Formoegenhetsanalys, Skatteprogressivitet, Arvsdynamik, Inkomstklyftan, Pensionsrattvisa,
Kapitalinkomst, Lonedynamik, Hushallsekonomi, Skattereform, Vaelfardsmodellen, and others.

## Maintainer

Gustav Olaf Yunus Laitinen-Fredriksson Lundstrom Imanov, MD, RA, PhD
Department of Economics, Stockholm University, SE-106 91 Stockholm, Sweden
ORCID: https://orcid.org/0009-0006-5184-0810
Email: olaf.laitinen@su.se
