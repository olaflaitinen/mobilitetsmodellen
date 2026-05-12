# Governance

## Model

Mobilitetsmodellen follows a **lead-maintainer model**. A single lead maintainer has final
authority over design decisions, release timing, and repository configuration.

## Lead Maintainer

Gustav Olaf Yunus Laitinen-Fredriksson Lundstrom Imanov, MD, RA, PhD
Department of Economics, Stockholm University
ORCID: https://orcid.org/0009-0006-5184-0810
Email: olaf.laitinen@su.se

## Decision Process

1. Minor changes (bug fixes, documentation, dependency bumps) may be merged by the lead
   maintainer without additional review.
2. Significant changes (new estimators, API changes, new dependencies) require at least one
   review comment from a contributor with domain expertise before merging.
3. Breaking changes require a CHANGELOG entry and a version bump.

## Releases

Releases follow [Semantic Versioning 2.0.0](https://semver.org/). Releases are tagged on the
`main` branch and published to PyPI via the GitHub Actions release workflow. Every release
produces a signed wheel, a signed sdist, a CycloneDX SBOM, and a Zenodo deposition.

## Succession

If the lead maintainer is unavailable for more than six months, the Department of Economics at
Stockholm University may appoint a successor by written notice to the repository.

## Code of Conduct

All contributors are bound by the [Contributor Covenant 2.1](CODE_OF_CONDUCT.md).
