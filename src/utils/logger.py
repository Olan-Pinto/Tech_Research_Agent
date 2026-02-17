# This code is to help me log any errors - It was written completely by AI.
import logging
import sys
import structlog
from structlog.dev import ConsoleRenderer, set_exc_info
from structlog.processors import StackInfoRenderer, TimeStamper, add_log_level
from structlog.stdlib import add_logger_name, PositionalArgumentsFormatter

def configure_logging():
    """
    Configures structlog with processors for development-friendly console output.
    """
    # Configure the standard library logging to pipe through structlog
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO, # Default log level is INFO
    )

    # Define the processor chain for structlog
    # Order is important: processors are run sequentially
    processors = [
        add_log_level,
        add_logger_name,
        PositionalArgumentsFormatter(), # Allows using %-style formatting
        StackInfoRenderer(), # Renders stack info on error logs
        set_exc_info, # Renders exception info on error logs
        TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=False), # Adds human-readable timestamps
        ConsoleRenderer(), # Pretty, colorful console output for development
    ]

    structlog.configure(
        processors=processors,
        # The wrapper class ensures log levels are respected for filtering
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        # Use standard library logging to output the final formatted event
        logger_factory=structlog.stdlib.LoggerFactory(),
        # Context class uses a plain dictionary
        context_class=dict,
        # Caching the logger on first use is efficient
        cache_logger_on_first_use=True
    )

def get_logger(*args, **kwargs) -> "structlog.stdlib.BoundLogger":
    """
    Returns a configured structlog logger instance.
    """
    return structlog.get_logger(*args, **kwargs)

# Initial configuration call
configure_logging()
