.PHONY: help lint type test cov docs build audit reuse sbom release sync clean

help:
	@echo "Available targets:"
	@echo "  lint    - Run ruff linter and formatter check"
	@echo "  type    - Run mypy strict type checking"
	@echo "  test    - Run the test suite"
	@echo "  cov     - Run tests with coverage"
	@echo "  docs    - Build MkDocs documentation"
	@echo "  build   - Build wheel and sdist"
	@echo "  audit   - Run pip-audit and bandit"
	@echo "  reuse   - Check REUSE 3.0 compliance"
	@echo "  sbom    - Generate CycloneDX SBOM"
	@echo "  release - Prepare release"
	@echo "  sync    - Sync dependencies via uv"
	@echo "  clean   - Remove build artifacts"

sync:
	uv sync --all-extras

lint:
	nox -s lint

type:
	nox -s type

test:
	nox -s test

cov:
	nox -s cov

docs:
	nox -s docs

build:
	nox -s build

audit:
	nox -s audit

reuse:
	nox -s reuse

sbom:
	nox -s sbom

release:
	nox -s release

clean:
	rm -rf dist/ build/ site/ *.egg-info/ .coverage htmlcov/ sbom.cdx.json
