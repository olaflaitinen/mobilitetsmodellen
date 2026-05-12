# Contributing to Mobilitetsmodellen

Thank you for considering a contribution. Please read this guide before opening issues or pull
requests.

## Developer Certificate of Origin

All commits must carry a DCO sign-off line:

    Signed-off-by: Full Name <email@example.com>

Add it with `git commit -s`. By signing off you certify that you wrote the contribution or
otherwise have the right to submit it under the EUPL-1.2 licence.

## Commit Style

Follow [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/):

    feat: add municipality-level shrinkage estimator
    fix: correct life-cycle alignment window off-by-one
    docs: expand reproducibility seeds table
    test: add hypothesis property test for rank monotonicity
    chore: bump numpy to 2.x

Commits must be GPG-signed (`git commit -S`).

## Licence Compatibility

All contributions must be compatible with EUPL-1.2. Do not introduce dependencies under
licences incompatible with the EUPL-1.2 compatible-licence list in the Appendix.

## REUSE 3.0 Compliance

Do not add per-file SPDX comment headers. Copyright and licence declarations are managed
exclusively via `.reuse/dep5`. Run `reuse lint` before opening a PR.

## GDPR No-PII Rule

Never commit real personal data, real microdata, real kinship graphs, personnummer, or
organisationsnummer. All data fixtures must be synthetic and seeded. The gitleaks rules in
`.gitleaks.toml` enforce this at commit time.

## Reproducibility Notes for DoubleML and Cross-Fitting

- Fold assignment must use SHA-256 hashing of stable individual identifiers, not random shuffling.
  See `seeds.derive_seed` and `estimators.double_ml` for the reference implementation.
- Nuisance-learner random states must be derived via `seeds.derive_seed("nuisance_init", base)`.
- After any change to fold assignment or nuisance initialisation, re-run `test_determinism.py`
  and commit updated orthogonalised-residual checksums to `replication/expected_receipts.json`.
- Set `OMP_NUM_THREADS=1` and `OPENBLAS_NUM_THREADS=1` when comparing cross-platform outputs.

## Development Setup

```bash
uv sync --all-extras
uv run pre-commit install
uv run pytest -x -q
uv run mypy --strict src
uv run ruff check .
```

## Pull Request Checklist

- [ ] Tests added or updated; coverage does not drop below 90 percent
- [ ] `ruff check .` and `ruff format --check .` pass
- [ ] `mypy --strict src` passes
- [ ] `reuse lint` passes
- [ ] DCO sign-off on all commits
- [ ] GPG-signed commits
- [ ] No personal data committed
- [ ] CHANGELOG.md updated under [Unreleased]
