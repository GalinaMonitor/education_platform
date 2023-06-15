import logging
import sys

import structlog

logger = structlog.get_logger()

# Disable uvicorn logging
logging.getLogger("uvicorn.error").disabled = True
logging.getLogger("uvicorn.access").disabled = True

# Structlog configuration
logging.basicConfig(format="%(message)s", stream=sys.stdout, level=logging.INFO)
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.dev.ConsoleRenderer(),
    ],
    logger_factory=structlog.PrintLoggerFactory(),
    # wrapper_class=structlog.make_filtering_bound_logger(logging.WARNING),
)
