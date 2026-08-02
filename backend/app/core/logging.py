"""
Structured logging configuration using structlog.
Outputs JSON in production, coloured console in development.
"""

import logging
import sys
from typing import Any

import structlog
from structlog.types import EventDict, Processor

from app.core.config import settings


def _add_app_context(
    logger: logging.Logger, method_name: str, event_dict: EventDict
) -> EventDict:
    """Add global app metadata to every log entry."""
    event_dict["app"] = settings.APP_NAME
    event_dict["version"] = settings.APP_VERSION
    event_dict["env"] = settings.ENVIRONMENT
    return event_dict


def _drop_color_message_key(
    logger: logging.Logger, method_name: str, event_dict: EventDict
) -> EventDict:
    """Remove the 'color_message' key added by uvicorn."""
    event_dict.pop("color_message", None)
    return event_dict


def setup_logging() -> None:
    """Configure structlog for structured JSON logging."""

    shared_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        _add_app_context,
        _drop_color_message_key,
    ]

    if settings.ENVIRONMENT == "production":
        # JSON output for log aggregators (Datadog, CloudWatch, etc.)
        processors = shared_processors + [
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer(),
        ]
        renderer: Any = structlog.processors.JSONRenderer()
    else:
        # Coloured console output for local development
        processors = shared_processors + [
            structlog.dev.ConsoleRenderer(colors=True),
        ]
        renderer = structlog.dev.ConsoleRenderer(colors=True)

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(
            logging.DEBUG if settings.DEBUG else logging.INFO
        ),
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Configure standard library logging to route through structlog
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.DEBUG if settings.DEBUG else logging.INFO,
    )

    # Silence noisy third-party loggers
    for logger_name in ["uvicorn.access", "sqlalchemy.engine", "httpx", "httpcore"]:
        logging.getLogger(logger_name).setLevel(logging.WARNING)
