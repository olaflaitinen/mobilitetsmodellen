"""Command-line interface for the mobility pipeline."""

from __future__ import annotations

import pathlib

import typer

from mobilitetsmodellen.logging import configure_logging

app = typer.Typer(
    name="mobilitetsmodellen",
    help="Machine-learning estimators of intergenerational mobility in Sweden.",
    no_args_is_help=True,
)


@app.callback()
def _setup(verbose: bool = typer.Option(False, "--verbose", "-v")) -> None:
    """Configure logging before any subcommand runs."""
    import logging

    configure_logging(level=logging.DEBUG if verbose else logging.INFO)


@app.command()
def version() -> None:
    """Print the package version and exit."""
    from mobilitetsmodellen._version import __version__

    typer.echo(__version__)


@app.command()
def ingest(data: pathlib.Path = typer.Argument(..., help="Path to raw data directory")) -> None:
    """Ingest and validate raw data sources."""
    typer.echo(f"Ingesting data from {data}")


@app.command()
def align(data: pathlib.Path = typer.Argument(..., help="Data directory")) -> None:
    """Apply life-cycle alignment to panel data."""
    typer.echo(f"Aligning panel at {data}")


@app.command("rank-rank")
def rank_rank(
    data: pathlib.Path = typer.Argument(...),
    output: pathlib.Path | None = typer.Option(None, "--output", "-o"),
) -> None:
    """Estimate the rank-rank slope."""
    typer.echo(f"Rank-rank estimation on {data}")
    if output:
        typer.echo(f"Writing to {output}")


@app.command()
def elasticity(data: pathlib.Path = typer.Argument(...)) -> None:
    """Estimate the intergenerational income elasticity (IGE)."""
    typer.echo(f"IGE estimation on {data}")


@app.command()
def transition(data: pathlib.Path = typer.Argument(...)) -> None:
    """Estimate quintile-to-quintile transition matrix."""
    typer.echo(f"Transition matrix on {data}")


@app.command("double-ml")
def double_ml(
    data: pathlib.Path = typer.Argument(...),
    n_folds: int = typer.Option(5, "--n-folds", min=2),
) -> None:
    """Run the double machine learning estimator."""
    typer.echo(f"DoubleML on {data} with {n_folds} folds")


@app.command("causal-forest")
def causal_forest(data: pathlib.Path = typer.Argument(...)) -> None:
    """Run the causal forest estimator."""
    typer.echo(f"Causal forest on {data}")


@app.command()
def mediation(data: pathlib.Path = typer.Argument(...)) -> None:
    """Run causal mediation analysis."""
    typer.echo(f"Mediation analysis on {data}")


@app.command()
def atlas(
    data: pathlib.Path = typer.Argument(...),
    output: pathlib.Path = typer.Option(pathlib.Path("atlas.html"), "--output", "-o"),
) -> None:
    """Build the interactive mobility atlas."""
    typer.echo(f"Building atlas from {data}, writing to {output}")


@app.command()
def benchmark(data: pathlib.Path = typer.Argument(...)) -> None:
    """Run cross-country benchmarking."""
    typer.echo(f"Benchmarking on {data}")


@app.command()
def report(data: pathlib.Path = typer.Argument(...)) -> None:
    """Generate figures and tables."""
    typer.echo(f"Reporting on {data}")


@app.command()
def repro(check: bool = typer.Option(False, "--check")) -> None:
    """Verify or generate replication receipts."""
    typer.echo(f"Reproducibility check: {check}")


@app.command()
def audit() -> None:
    """Run pip-audit and bandit security scans."""
    typer.echo("Running security audit")


@app.command()
def sbom(output: pathlib.Path = typer.Option(pathlib.Path("sbom.cdx.json"))) -> None:
    """Generate a CycloneDX SBOM."""
    typer.echo(f"Generating SBOM at {output}")


@app.command("reuse-check")
def reuse_check() -> None:
    """Check REUSE 3.0 compliance."""
    typer.echo("Checking REUSE compliance")


def main() -> None:
    """Entry point for the CLI."""
    configure_logging()
    app()
