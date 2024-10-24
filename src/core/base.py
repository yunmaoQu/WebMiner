# src/core/base.py
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime

class BaseComponent(ABC):
    """所有组件的基类"""
    def __init__(self):
        self.name = self.__class__.__name__
        self.created_at = datetime.now()

    @abstractmethod
    def validate_config(self) -> bool:
        """验证配置"""
        pass

class DataContainer:
    """数据容器，用于在组件间传递数据"""
    def __init__(self, data: Any, metadata: Optional[Dict] = None):
        self.data = data
        self.metadata = metadata or {}
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def update(self, data: Any) -> None:
        """更新数据"""
        self.data = data
        self.updated_at = datetime.now()

    def add_metadata(self, key: str, value: Any) -> None:
        """添加元数据"""
        self.metadata[key] = value