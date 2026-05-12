"""Manifest model for tracking ingested data sources."""

from __future__ import annotations

import datetime
import hashlib
import pathlib

from pydantic import BaseModel, ConfigDict, Field


class Manifest(BaseModel):
    """Metadata record for an ingested data file.

    Attributes:
        path: Absolute path to the data file.
        sha256: SHA-256 hex digest of the file contents.
        n_rows: Number of rows in the dataset.
        ingested_at: UTC timestamp of ingestion.
        source: Descriptive label for the data source.
    """

    model_config = ConfigDict(frozen=True)

    path: pathlib.Path
    sha256: str
    n_rows: int = Field(ge=0)
    ingested_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(tz=datetime.UTC)
    )
    source: str = ""

    @classmethod
    def from_path(cls, path: pathlib.Path, n_rows: int, source: str = "") -> Manifest:
        """Create a Manifest by hashing an existing file.

        Args:
            path: Path to the data file.
            n_rows: Number of rows in the dataset.
            source: Optional source label.

        Returns:
            A :class:`Manifest` with sha256 computed from the file.
        """
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        return cls(path=path, sha256=digest, n_rows=n_rows, source=source)
