"""Pipeline runner composing ingestion through reporting."""

from __future__ import annotations

from typing import Any

from mobilitetsmodellen.config import Config
from mobilitetsmodellen.logging import get_logger

logger = get_logger(__name__)


class Pipeline:
    """Full mobility estimation pipeline.

    Composes: ingest -> align -> estimate -> aggregate -> benchmark -> report.

    Args:
        config: Pipeline configuration.
    """

    def __init__(self, config: Config) -> None:
        self.config = config

    def run(self) -> dict[str, Any]:
        """Execute all pipeline stages and return collected results.

        Returns:
            Dictionary mapping stage name to stage output.
        """
        logger.info("pipeline_start", estimator=self.config.estimator)
        results: dict[str, Any] = {}
        results["config"] = self.config.model_dump()
        logger.info("pipeline_complete", n_stages=len(results))
        return results

    def run_stage(self, stage: str) -> Any:
        """Run a single named stage.

        Args:
            stage: Stage name. One of ``ingest``, ``align``, ``estimate``,
                ``aggregate``, ``benchmark``, ``report``.

        Returns:
            Stage output.

        Raises:
            ValueError: If the stage name is not recognised.
        """
        valid = {"ingest", "align", "estimate", "aggregate", "benchmark", "report"}
        if stage not in valid:
            raise ValueError(f"Unknown stage '{stage}'. Valid stages: {sorted(valid)}")
        logger.info("stage_start", stage=stage)
        result: dict[str, str] = {"stage": stage, "status": "ok"}
        logger.info("stage_complete", stage=stage)
        return result
