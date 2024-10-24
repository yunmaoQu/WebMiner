# src/core/crawler.py
from abc import abstractmethod
from typing import Dict, List, Optional
from .base import BaseComponent, DataContainer

class BaseCrawler(BaseComponent):
    """爬虫基类"""
    
    @abstractmethod
    def fetch(self, **kwargs) -> DataContainer:
        """获取数据"""
        pass

    @abstractmethod
    def parse(self, data: str) -> DataContainer:
        """解析数据"""
        pass

    @abstractmethod
    def validate(self, data: DataContainer) -> bool:
        """验证数据"""
        pass

    def process_response(self, response: str) -> DataContainer:
        """处理响应"""
        data = self.parse(response)
        if self.validate(data):
            return data
        raise ValueError("Invalid data received")