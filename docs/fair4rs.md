# FAIR4RS Compliance Matrix

FAIR4RS extends the FAIR data principles to research software.

## Findable

| Principle | Status | Evidence |
|-----------|--------|----------|
| F1: Software has a globally unique identifier | Compliant | DOI via Zenodo; GitHub URL |
| F2: Software is described with rich metadata | Compliant | CITATION.cff, .zenodo.json, pyproject.toml |
| F3: Metadata includes software identifier | Compliant | CITATION.cff url field |
| F4: Software is registered in searchable resource | Compliant | PyPI, Zenodo, OSOR |

## Accessible

| Principle | Status | Evidence |
|-----------|--------|----------|
| A1: Software retrievable by identifier | Compliant | pip install mobilitetsmodellen |
| A1.1: Open standard protocol | Compliant | HTTPS via GitHub/PyPI |
| A1.2: Protocol allows authentication | Compliant | GitHub/PyPI public access |
| A2: Metadata accessible even if software unavailable | Compliant | Zenodo preserves metadata |

## Interoperable

| Principle | Status | Evidence |
|-----------|--------|----------|
| I1: Software uses community standards | Compliant | PEP 517/518, SemVer, CC 1.0.0 |
| I2: Software uses FAIR data formats | Compliant | Parquet, CSV, JSON outputs |
| I3: Software includes qualified references | Compliant | CITATION.cff references block |

## Reusable

| Principle | Status | Evidence |
|-----------|--------|----------|
| R1: Software described with provenance | Compliant | NOTICE, CITATION.cff, CHANGELOG |
| R1.1: Software released with clear licence | Compliant | EUPL-1.2 via REUSE 3.0 |
| R1.2: Software associated with community standards | Compliant | CONTRIBUTING, CODE_OF_CONDUCT |
| R2: Software includes detailed provenance | Compliant | reproducibility.md; seeds |
| R3: Software meets domain community standards | Compliant | DoubleML, GRF conventions |
