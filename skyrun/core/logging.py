"""
Logging configuration for SkyRun.
"""
import logging
import sys
from pathlib import Path
from typing import Optional

from .config import settings

def setup_logging(
    level: int = logging.INFO,
    log_file: Optional[Path] = None,
    format_string: Optional[str] = None
) -> None:
    """Setup logging configuration.
    
    Args:
        level: Logging level
        log_file: Path to log file
        format_string: Custom format string for logs
    """
    if format_string is None:
        format_string = (
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            if not settings.DEBUG
            else "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
        )
    
    # Create formatter
    formatter = logging.Formatter(format_string)
    
    # Setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler (if log_file is provided)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(str(log_file))
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    # Disable propagation for third-party loggers
    for logger_name in ["urllib3", "requests"]:
        logging.getLogger(logger_name).propagate = False

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance.
    
    Args:
        name: Logger name
    
    Returns:
        Logger instance
    """
    return logging.getLogger(name)

# Setup default logging
setup_logging(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    log_file=settings.PROJECT_ROOT / "logs" / "skyrun.log"
) 