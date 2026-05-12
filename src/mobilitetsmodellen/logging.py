"""Structured logging configuration via structlog."""

from __future__ import annotations

import logging

import structlog


def configure_logging(level: int = logging.INFO) -> None:
    """Configure structlog for the application.

    Args:
        level: Python logging level. Defaults to ``logging.INFO``.
    """
    logging.basicConfig(
        format="%(message)s",
        level=level,
    )
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str = "mobilitetsmodellen") -> structlog.stdlib.BoundLogger:
    """Return a bound structlog logger.

    Args:
        name: Logger name.

    Returns:
        A configured :class:`structlog.stdlib.BoundLogger` instance.
    """
    return structlog.get_logger(name)  # type: ignore[no-any-return]
