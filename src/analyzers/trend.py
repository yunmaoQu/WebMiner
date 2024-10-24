# src/analyzers/trends.py
from typing import Dict, List, Any
from collections import defaultdict
from datetime import datetime, timedelta
from src.core.analyzer import BaseAnalyzer
from src.core.base import DataContainer

class TrendAnalyzer(BaseAnalyzer):
    """趋势分析器"""
    
    def __init__(self):
        super().__init__()
        self.metrics = [
            'stars',
            'forks',
            'today_stars',
            'activity_score'
        ]

    def analyze(self, data: DataContainer) -> Dict[str, Any]:
        """分析趋势数据"""
        repositories = data.data
        
        metrics = self.calculate_metrics(DataContainer(repositories))
        insights = self.generate_insights(metrics)
        
        analysis = {
            'metrics': metrics,
            'insights': insights,
            'trends': {
                'language_trends': self._analyze_language_trends(repositories),
                'activity_trends': self._analyze_activity_trends(repositories),
                'popularity_trends': self._analyze_popularity_trends(repositories)
            },
            'timestamp': datetime.now().isoformat()
        }
        
        return analysis

    
    def calculate_metrics(self, data: DataContainer) -> Dict[str, float]:
        """计算统计指标"""
        repositories = data.data
        metrics = {}
        
        # 基本统计
        metrics['total_repositories'] = len(repositories)
        metrics['total_stars'] = sum(repo.get('stars', 0) for repo in repositories)
        metrics['total_forks'] = sum(repo.get('forks', 0) for repo in repositories)
        metrics['average_activity_score'] = (
            sum(repo.get('activity_score', 0) for repo in repositories) / 
            len(repositories) if repositories else 0
        )
        
        # 语言统计
        language_counts = defaultdict(int)
        for repo in repositories:
            language = repo.get('language', 'Unknown')
            language_counts[language] += 1
        metrics['language_distribution'] = dict(language_counts)
        
        # 活跃度分布
        activity_scores = [repo.get('activity_score', 0) for repo in repositories]
        metrics['min_activity'] = min(activity_scores) if activity_scores else 0
        metrics['max_activity'] = max(activity_scores) if activity_scores else 0
        
        return metrics

    def generate_insights(self, metrics: Dict[str, float]) -> List[str]:
        """生成数据洞察"""
        insights = []
        
        # 仓库数量洞察
        insights.append(
            f"Analyzed {metrics['total_repositories']} trending repositories"
        )
        
        # 语言分布洞察
        top_languages = sorted(
            metrics['language_distribution'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]
        
        insights.append(
            "Top languages: " + 
            ", ".join(f"{lang} ({count} repos)" for lang, count in top_languages)
        )
        
        # 活跃度洞察
        insights.append(
            f"Activity scores range from {metrics['min_activity']:.2f} "
            f"to {metrics['max_activity']:.2f}"
        )
        
        return insights

    def _analyze_language_trends(self, repositories: List[Dict]) -> Dict[str, Any]:
        """分析语言趋势"""
        language_stats = defaultdict(lambda: {
            'repos': 0,
            'total_stars': 0,
            'total_forks': 0,
            'avg_activity': 0.0,
            'repositories': []
        })
        
        for repo in repositories:
            language = repo.get('language', 'Unknown')
            stats = language_stats[language]
            stats['repos'] += 1
            stats['total_stars'] += repo.get('stars', 0)
            stats['total_forks'] += repo.get('forks', 0)
            stats['avg_activity'] = (
                stats['avg_activity'] * (stats['repos'] - 1) + 
                repo.get('activity_score', 0)
            ) / stats['repos']
            stats['repositories'].append(repo['name'])
        
        return dict(language_stats)

    def _analyze_activity_trends(self, repositories: List[Dict]) -> Dict[str, Any]:
        """分析活跃度趋势"""
        activity_ranges = {
            'high': {'min': 80, 'repos': []},
            'medium': {'min': 50, 'repos': []},
            'low': {'min': 0, 'repos': []}
        }
        
        for repo in repositories:
            score = repo.get('activity_score', 0)
            for range_name, range_data in activity_ranges.items():
                if score >= range_data['min']:
                    range_data['repos'].append({
                        'name': repo['name'],
                        'score': score,
                        'language': repo.get('language', 'Unknown')
                    })
                    break
        
        return activity_ranges

    def _analyze_popularity_trends(self, repositories: List[Dict]) -> Dict[str, Any]:
        """分析流行度趋势"""
        return {
            'most_starred': sorted(
                repositories,
                key=lambda x: x.get('stars', 0),
                reverse=True
            )[:5],
            'most_forked': sorted(
                repositories,
                key=lambda x: x.get('forks', 0),
                reverse=True
            )[:5],
            'trending_today': sorted(
                repositories,
                key=lambda x: x.get('today_stars', 0),
                reverse=True
            )[:5]
        }

    def validate_config(self) -> bool:
        """验证配置"""
        return bool(self.metrics)