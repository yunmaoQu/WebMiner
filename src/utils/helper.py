"""
Helper functions for the GitHub Trending Tracker.
"""

import time
from datetime import datetime
from functools import wraps
from typing import Union, Callable, Any

def format_number(num: Union[int, float]) -> str:
    """Format large numbers for display."""
    if num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    if num >= 1_000:
        return f"{num/1_000:.1f}K"
    return str(num)

def parse_date(date_str: str) -> datetime:
    """Parse various date formats into datetime object."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Unable to parse date: {date_str}")

def validate_language(language: str) -> bool:
    """Validate if the given language is supported."""
    valid_languages = {
        "python", "java", "javascript", "go", "rust",
        "c++", "typescript", "php", "ruby", "swift"
    }
    return language.lower() in valid_languages

def rate_limit_decorator(
    calls: int = 30,
    period: float = 60.0
) -> Callable:
    """
    Rate limiting decorator.
    
    Args:
        calls (int): Number of calls allowed
        period (float): Time period in seconds
    """
    def decorator(func: Callable) -> Callable:
        last_reset = time.time()
        calls_made = 0

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            nonlocal last_reset, calls_made
            
            now = time.time()
            elapsed = now - last_reset
            
            if elapsed > period:
                calls_made = 0
                last_reset = now
            
            if calls_made >= calls:
                sleep_time = period - elapsed
                if sleep_time > 0:
                    time.sleep(sleep_time)
                calls_made = 0
                last_reset = time.time()
            
            calls_made += 1
            return func(*args, **kwargs)
            
        return wrapper
    return decorator
def ensure_data_directory():
    """确保数据目录存在"""
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    return data_dir