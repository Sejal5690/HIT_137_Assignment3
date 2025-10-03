"""
Logging utilities with encapsulation demonstration.

This module showcases:
- Encapsulation of logging configuration and operations
- Singleton pattern for logger instance
- Clean separation of logging concerns
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


class AppLogger:
    """
    Application logger with encapsulated configuration.
    
    Demonstrates encapsulation by hiding logging setup complexity
    and providing clean interface for logging operations.
    Uses singleton pattern to ensure one logger instance.
    """
    
    _instance: Optional['AppLogger'] = None
    _logger: Optional[logging.Logger] = None
    
    def __new__(cls):
        """Singleton pattern - ensure only one logger instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize logger with private configuration."""
        if self._logger is None:
            self._setup_logger()
    
    def _setup_logger(self) -> None:
        """
        Private method to configure logger - encapsulation.
        
        Sets up logging with both console and file output.
        """
        self._logger = logging.getLogger('AIModelApp')
        self._logger.setLevel(logging.INFO)
        
        # Clear any existing handlers
        self._logger.handlers.clear()
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self._logger.addHandler(console_handler)
        
        # File handler (optional - logs to file if possible)
        try:
            log_file = Path("app_log.txt")
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            self._logger.addHandler(file_handler)
        except Exception:
            # If file logging fails, continue with console only
            pass
    
    def info(self, message: str) -> None:
        """Log info message - encapsulated logging operation."""
        if self._logger:
            self._logger.info(message)
    
    def error(self, message: str) -> None:
        """Log error message - encapsulated logging operation."""
        if self._logger:
            self._logger.error(message)
    
    def warning(self, message: str) -> None:
        """Log warning message - encapsulated logging operation."""
        if self._logger:
            self._logger.warning(message)
    
    def debug(self, message: str) -> None:
        """Log debug message - encapsulated logging operation."""
        if self._logger:
            self._logger.debug(message)
    
    def log_model_operation(self, model_name: str, operation: str, duration: float = None) -> None:
        """
        Log model-specific operations - specialized logging method.
        
        Args:
            model_name: Name of the AI model
            operation: Operation being performed
            duration: Optional duration in seconds
        """
        message = f"Model '{model_name}' - {operation}"
        if duration is not None:
            message += f" (Duration: {duration:.2f}s)"
        self.info(message)
    
    def log_user_action(self, action: str, details: str = "") -> None:
        """
        Log user interface actions - specialized logging method.
        
        Args:
            action: User action description
            details: Optional additional details
        """
        message = f"User Action: {action}"
        if details:
            message += f" - {details}"
        self.info(message)


# Global logger instance for easy access
logger = AppLogger()