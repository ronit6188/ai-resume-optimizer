"""Application‑wide logger configuration using structlog.

All logs are emitted as JSON strings, making them easy to ship to CloudWatch,
Datadog, Loki, etc.
"""

import logging
import sys
from typing import Any

import structlog

# Basic logging for the standard library – output to stdout
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    stream=sys.stdout,
)

# structlog processors – timestamps, level, event, and optional stack info
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer(),
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

# Export a ready‑to‑use logger instance
logger = structlog.get_logger()
