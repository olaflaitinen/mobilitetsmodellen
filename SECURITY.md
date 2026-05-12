# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | Yes       |

## Reporting a Vulnerability

Please do **not** open a public GitHub issue for security vulnerabilities.

Report vulnerabilities by email to: olaf.laitinen@su.se

Include in your report:

- A description of the vulnerability and its potential impact
- Steps to reproduce or a proof-of-concept
- Affected versions
- Any suggested mitigations

## Response Timeline

- Acknowledgement within 2 business days
- Initial assessment within 7 calendar days
- Fix or mitigation within 90 calendar days (aligned with coordinated disclosure)
- Public disclosure after fix is released, crediting the reporter unless anonymity is requested

## NIS2-Aligned Secure Development Lifecycle

This project follows NIS2 (EU) 2022/2555-aligned SDLC practices:

- Dependency vulnerability scanning via `pip-audit` and `osv-scanner` in CI
- Static analysis via `bandit -r src -lll` in CI
- Code scanning via GitHub CodeQL on a weekly schedule
- Supply-chain security via Sigstore OIDC signing of releases
- SBOM (CycloneDX 1.5 JSON) published with every release
- Dependabot enabled for automated dependency updates
- Secrets scanning via gitleaks with personnummer and organisationsnummer deny-list

## No Personal Data

This repository contains no real personal data, no real microdata, and no real kinship graphs.
All data fixtures are synthetic. See [docs/gdpr.md](docs/gdpr.md) for the full GDPR analysis.
