# src/processors/activity.py
from typing import Dict, Any
from datetime import datetime
from src.core.processor import BaseProcessor
from src.core.base import DataContainer

class ActivityProcessor(BaseProcessor):
    """活跃度处理器"""
    
    def __init__(self):
        super().__init__()
        self.weights = {
            'stars': 0.3,
            'forks': 0.2,
            'today_stars': 0.2,
            'language_popularity': 0.15,
            'description_quality': 0.15
        }

    def process(self, data: DataContainer) -> DataContainer:
        """处理仓库数据"""
        processed_repos = []
        
        for repo in data.data:
            processed_repo = self.transform(DataContainer(repo))
            processed_repos.append(processed_repo.data)

        return DataContainer(
            data=processed_repos,
            metadata={
                **data.metadata,
                'processed_at': datetime.now().isoformat(),
                'processor': self.name
            }
        )

    def transform(self, data: DataContainer) -> DataContainer:
        """转换单个仓库数据"""
        repo = data.data
        activity_score = self._calculate_activity_score(repo)
        
        transformed_data = {
            **repo,
            'activity_score': activity_score,
            'metrics': {
                'stars_weight': self._calculate_stars_weight(repo),
                'forks_weight': self._calculate_forks_weight(repo),
                'today_stars_weight': self._calculate_today_stars_weight(repo),
                'language_weight': self._calculate_language_weight(repo),
                'description_weight': self._calculate_description_weight(repo)
            }
        }
        
        return DataContainer(transformed_data)

    def clean(self, data: DataContainer) -> DataContainer:
        """清理数据"""
        cleaned_data = {
            k: v for k, v in data.data.items()
            if v is not None and v != ''
        }
        return DataContainer(cleaned_data)

    def _calculate_activity_score(self, repo: Dict[str, Any]) -> float:
        """计算总活跃度分数"""
        scores = {
            'stars': self._calculate_stars_weight(repo),
            'forks': self._calculate_forks_weight(repo),
            'today_stars': self._calculate_today_stars_weight(repo),
            'language_popularity': self._calculate_language_weight(repo),
            'description_quality': self._calculate_description_weight(repo)
        }
        
        total_score = sum(
            scores[metric] * self.weights[metric]
            for metric in self.weights
        )
        
        return round(total_score * 100, 2)

    def _calculate_stars_weight(self, repo: Dict[str, Any]) -> float:
        """计算star权重"""
        stars = repo.get('stars', 0)
        if stars >= 10000:
            return 1.0
        return stars / 10000

    def _calculate_forks_weight(self, repo: Dict[str, Any]) -> float:
        """计算fork权重"""
        forks = repo.get('forks', 0)
        if forks >= 5000:
            return 1.0
        return forks / 5000

    def _calculate_today_stars_weight(self, repo: Dict[str, Any]) -> float:
        """计算今日star权重"""
        today_stars = repo.get('today_stars', 0)
        if today_stars >= 1000:
            return 1.0
        return today_stars / 1000

    def _calculate_language_weight(self, repo: Dict[str, Any]) -> float:
        """计算语言权重"""
        popular_languages = {
            'python': 1.0,
            'javascript': 1.0,
            'java': 0.9,
            'go': 0.9,
            'typescript': 0.9,
            'rust': 0.8,
            'c++': 0.8,
            'ruby': 0.7
        }
        language = repo.get('language', '').lower()
        return popular_languages.get(language, 0.5)

    def _calculate_description_weight(self, repo: Dict[str, Any]) -> float:
        """计算描述质量权重"""
        description = repo.get('description', '')
        if not description:
            return 0.0
        
        # 简单的质量评估
        quality = 0.0
        if len(description) >= 20:
            quality += 0.5
        if len(description) >= 50:
            quality += 0.3
        if any(keyword in description.lower() for keyword in ['api', 'framework', 'library', 'tool']):
            quality += 0.2
            
        return min(quality, 1.0)