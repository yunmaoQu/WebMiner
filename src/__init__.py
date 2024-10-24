"""
GitHub Trending Tracker
~~~~~~~~~~~~~~~~~~~~~~

A tool to track GitHub trending repositories with community activity analysis.
"""

from src.crawler.github_crawler import GitHubTrendingCrawler
from src.database.db_manager import DatabaseManager
from src.notification.email_notifier import EmailNotifier
from src.utils.logger import setup_logging

__version__ = '1.0.0'
__author__ = 'Your Name'
__email__ = 'your.email@example.com'

# 设置默认日志配置
logger = setup_logging()

__all__ = [
    'GitHubTrendingCrawler',
    'DatabaseManager',
    'EmailNotifier',
    'setup_logging',
]