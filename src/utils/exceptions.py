"""
Custom exceptions for the GitHub Trending Tracker.
"""

class BaseException(Exception):
    """Base exception class for the project."""
    pass

class CrawlerException(BaseException):
    """Raised when there's an error during crawling."""
    pass

class DatabaseException(BaseException):
    """Raised when there's a database related error."""
    pass

class NotificationException(BaseException):
    """Raised when there's an error in notification system."""
    pass

class ConfigurationException(BaseException):
    """Raised when there's a configuration error."""
    pass