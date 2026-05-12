"""Tests for the CLI entry points."""

from __future__ import annotations

from typer.testing import CliRunner

from mobilitetsmodellen.cli import app

runner = CliRunner()


def test_version() -> None:
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "0.1.0" in result.output


def test_help() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "mobilitetsmodellen" in result.output.lower()


def test_ingest_command(tmp_path: pathlib.Path) -> None:
    result = runner.invoke(app, ["ingest", str(tmp_path)])
    assert result.exit_code == 0


def test_align_command(tmp_path: pathlib.Path) -> None:
    result = runner.invoke(app, ["align", str(tmp_path)])
    assert result.exit_code == 0


def test_rank_rank_command(tmp_path: pathlib.Path) -> None:
    result = runner.invoke(app, ["rank-rank", str(tmp_path)])
    assert result.exit_code == 0


def test_elasticity_command(tmp_path: pathlib.Path) -> None:
    result = runner.invoke(app, ["elasticity", str(tmp_path)])
    assert result.exit_code == 0


def test_transition_command(tmp_path: pathlib.Path) -> None:
    result = runner.invoke(app, ["transition", str(tmp_path)])
    assert result.exit_code == 0


def test_double_ml_command(tmp_path: pathlib.Path) -> None:
    result = runner.invoke(app, ["double-ml", str(tmp_path)])
    assert result.exit_code == 0


def test_causal_forest_command(tmp_path: pathlib.Path) -> None:
    result = runner.invoke(app, ["causal-forest", str(tmp_path)])
    assert result.exit_code == 0


def test_mediation_command(tmp_path: pathlib.Path) -> None:
    result = runner.invoke(app, ["mediation", str(tmp_path)])
    assert result.exit_code == 0


def test_atlas_command(tmp_path: pathlib.Path) -> None:
    result = runner.invoke(app, ["atlas", str(tmp_path)])
    assert result.exit_code == 0


def test_benchmark_command(tmp_path: pathlib.Path) -> None:
    result = runner.invoke(app, ["benchmark", str(tmp_path)])
    assert result.exit_code == 0


def test_report_command(tmp_path: pathlib.Path) -> None:
    result = runner.invoke(app, ["report", str(tmp_path)])
    assert result.exit_code == 0


def test_repro_command() -> None:
    result = runner.invoke(app, ["repro"])
    assert result.exit_code == 0


def test_audit_command() -> None:
    result = runner.invoke(app, ["audit"])
    assert result.exit_code == 0


def test_sbom_command() -> None:
    result = runner.invoke(app, ["sbom"])
    assert result.exit_code == 0


def test_reuse_check_command() -> None:
    result = runner.invoke(app, ["reuse-check"])
    assert result.exit_code == 0


import pathlib  # noqa: E402
