# src/core/processor.py
from abc import abstractmethod
from typing import Dict, List
from .base import BaseComponent, DataContainer

class BaseProcessor(BaseComponent):
    """数据处理器基类"""
    
    @abstractmethod
    def process(self, data: DataContainer) -> DataContainer:
        """处理数据"""
        pass

    @abstractmethod
    def transform(self, data: DataContainer) -> DataContainer:
        """转换数据"""
        pass

    @abstractmethod
    def clean(self, data: DataContainer) -> DataContainer:
        """清理数据"""
        pass

    def validate_config(self) -> bool:
        """验证配置"""
        return True