"""Tests for the pipeline DAG and runner."""

from __future__ import annotations

import pytest

from mobilitetsmodellen.config import Config
from mobilitetsmodellen.pipelines.dag import DAG, Task
from mobilitetsmodellen.pipelines.runner import Pipeline


def test_dag_add_task() -> None:
    dag = DAG()
    dag.add(Task(name="a", fn=lambda: 1))
    assert "a" in dag._tasks


def test_dag_duplicate_raises() -> None:
    dag = DAG()
    dag.add(Task("a", fn=lambda: 1))
    with pytest.raises(ValueError, match="Duplicate"):
        dag.add(Task("a", fn=lambda: 2))


def test_dag_topological_order() -> None:
    dag = DAG()
    dag.add(Task("a", fn=lambda: 1))
    dag.add(Task("b", fn=lambda: 2, dependencies=["a"]))
    dag.add(Task("c", fn=lambda: 3, dependencies=["a", "b"]))
    order = dag.topological_order()
    assert order.index("a") < order.index("b") < order.index("c")


def test_dag_cycle_raises() -> None:
    dag = DAG()
    dag.add(Task("a", fn=lambda: 1, dependencies=["b"]))
    dag.add(Task("b", fn=lambda: 2, dependencies=["a"]))
    with pytest.raises(ValueError, match="cycle"):
        dag.topological_order()


def test_dag_run_returns_results() -> None:
    dag = DAG()
    dag.add(Task("x", fn=lambda: 42))
    dag.add(Task("y", fn=lambda: 99, dependencies=["x"]))
    results = dag.run()
    assert results["x"] == 42
    assert results["y"] == 99


def test_pipeline_run_returns_dict() -> None:
    cfg = Config()
    pipeline = Pipeline(cfg)
    result = pipeline.run()
    assert isinstance(result, dict)
    assert "config" in result


def test_pipeline_run_stage_valid() -> None:
    cfg = Config()
    pipeline = Pipeline(cfg)
    result = pipeline.run_stage("ingest")
    assert result["status"] == "ok"


def test_pipeline_run_stage_invalid() -> None:
    cfg = Config()
    pipeline = Pipeline(cfg)
    with pytest.raises(ValueError, match="Unknown stage"):
        pipeline.run_stage("nonexistent")
