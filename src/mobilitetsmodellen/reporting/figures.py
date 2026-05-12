"""Figure generation for mobility analysis outputs."""

from __future__ import annotations

import pathlib
from typing import Any

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use("Agg")


class FigureBuilder:
    """Builder for standardised mobility analysis figures.

    Args:
        output_dir: Directory where figures are saved.
        dpi: Resolution in dots per inch.
        formats: List of output formats (e.g. ``["png", "svg", "pdf"]``).
    """

    def __init__(
        self,
        output_dir: pathlib.Path = pathlib.Path("reports/figures"),
        dpi: int = 150,
        formats: list[str] | None = None,
    ) -> None:
        self.output_dir = output_dir
        self.dpi = dpi
        self.formats = formats or ["png"]
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def rank_rank_scatter(
        self,
        parent_ranks: np.ndarray,  # type: ignore[type-arg]
        child_ranks: np.ndarray,  # type: ignore[type-arg]
        slope: float,
        intercept: float,
        title: str = "Rank-Rank Scatter",
        filename: str = "rank_rank_scatter",
    ) -> list[pathlib.Path]:
        """Plot a rank-rank scatter with fitted regression line.

        Args:
            parent_ranks: Array of parent income ranks.
            child_ranks: Array of child income ranks.
            slope: Fitted slope for overlay line.
            intercept: Fitted intercept for overlay line.
            title: Figure title.
            filename: Output filename stem (no extension).

        Returns:
            List of paths to saved figures.
        """
        fig, ax = plt.subplots(figsize=(6, 5))
        ax.scatter(parent_ranks, child_ranks, alpha=0.3, s=4, color="#1f77b4", rasterized=True)
        x_line = np.array([0.0, 1.0])
        ax.plot(x_line, intercept + slope * x_line, color="#d62728", linewidth=2)
        ax.set_xlabel("Parent income rank")
        ax.set_ylabel("Child income rank")
        ax.set_title(title)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        fig.tight_layout()
        paths = self._save(fig, filename)
        plt.close(fig)
        return paths

    def transition_heatmap(
        self,
        matrix: np.ndarray,  # type: ignore[type-arg]
        title: str = "Quintile Transition Matrix",
        filename: str = "transition_matrix",
    ) -> list[pathlib.Path]:
        """Plot a quintile-to-quintile transition probability heatmap.

        Args:
            matrix: (5, 5) transition probability matrix.
            title: Figure title.
            filename: Output filename stem.

        Returns:
            List of paths to saved figures.
        """
        fig, ax = plt.subplots(figsize=(5, 4))
        im = ax.imshow(matrix, vmin=0, vmax=1, cmap="Blues", aspect="auto")
        fig.colorbar(im, ax=ax, label="Probability")
        labels = ["Q1", "Q2", "Q3", "Q4", "Q5"]
        ax.set_xticks(range(5))
        ax.set_xticklabels(labels)
        ax.set_yticks(range(5))
        ax.set_yticklabels(labels)
        ax.set_xlabel("Child quintile")
        ax.set_ylabel("Parent quintile")
        ax.set_title(title)
        fig.tight_layout()
        paths = self._save(fig, filename)
        plt.close(fig)
        return paths

    def _save(self, fig: Any, filename: str) -> list[pathlib.Path]:
        paths = []
        for fmt in self.formats:
            out = self.output_dir / f"{filename}.{fmt}"
            fig.savefig(out, dpi=self.dpi, bbox_inches="tight")
            paths.append(out)
        return paths
