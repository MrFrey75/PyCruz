import logging
import logging.handlers
import os
from typing import Optional
from .config import config


class Logger:
    def __init__(self, name: str = __name__):
        self.logger = logging.getLogger(name)
        self._setup_logger()

    def _setup_logger(self):
        """Setup centralized logging configuration"""
        # Avoid duplicate handlers
        if self.logger.handlers:
            return

        # Get logging configuration
        log_level = getattr(logging, config.get('logging.level', 'INFO').upper())
        log_file = config.get('logging.file_path', 'logs/app.log')
        max_bytes = config.get('logging.max_file_size', 10485760)  # 10MB
        backup_count = config.get('logging.backup_count', 5)
        log_format = config.get('logging.format',
                                '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Create logs directory if it doesn't exist
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        # Set logger level
        self.logger.setLevel(log_level)

        # Create formatter
        formatter = logging.Formatter(log_format)

        # File handler with rotation
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)

        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def debug(self, message: str, *args, **kwargs):
        self.logger.debug(message, *args, **kwargs)

    def info(self, message: str, *args, **kwargs):
        self.logger.info(message, *args, **kwargs)

    def warning(self, message: str, *args, **kwargs):
        self.logger.warning(message, *args, **kwargs)

    def error(self, message: str, *args, **kwargs):
        self.logger.error(message, *args, **kwargs)

    def critical(self, message: str, *args, **kwargs):
        self.logger.critical(message, *args, **kwargs)


# Global logger instance
logger = Logger(__name__)


def get_logger(name: str) -> Logger:
    """Get a logger instance for a specific module"""
    return Logger(name)