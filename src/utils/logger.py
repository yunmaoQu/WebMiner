# src/utils/logger.py
import logging.config
from config.settings import LOGGING

def setup_logging():
    """配置日志系统"""
    logging.config.dictConfig(LOGGING)
    return logging.getLogger(__name__)