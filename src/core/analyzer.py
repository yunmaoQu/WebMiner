# src/core/analyzer.py
from abc import abstractmethod
from typing import Dict, List, Any
from .base import BaseComponent, DataContainer

class BaseAnalyzer(BaseComponent):
    """分析器基类"""
    
    @abstractmethod
    def analyze(self, data: DataContainer) -> Dict[str, Any]:
        """分析数据"""
        pass

    @abstractmethod
    def calculate_metrics(self, data: DataContainer) -> Dict[str, float]:
        """计算指标"""
        pass

    @abstractmethod
    def generate_insights(self, metrics: Dict[str, float]) -> List[str]:
        """生成洞察"""
        pass

    def validate_config(self) -> bool:
        """验证配置"""
        return True