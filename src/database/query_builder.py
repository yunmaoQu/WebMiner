from typing import List, Optional, Any
from sqlalchemy import and_, or_, desc
from sqlalchemy.orm import Query
from .models import Repository, TrendingHistory, LanguageStats, ActivityChanges

class QueryBuilder:
    """SQL 查询构建器"""
    
    @staticmethod
    def trending_repositories(
        query: Query,
        language: Optional[str] = None,
        min_stars: Optional[int] = None,
        min_activity: Optional[float] = None,
        limit: int = 20
    ) -> Query:
        """构建趋势仓库查询"""
        if language:
            query = query.filter(Repository.language == language)
        if min_stars:
            query = query.filter(Repository.stars >= min_stars)
        if min_activity:
            query = query.filter(Repository.activity_score >= min_activity)
            
        return query.order_by(desc(Repository.activity_score)).limit(limit)

    @staticmethod
    def language_statistics(
        query: Query,
        min_repos: Optional[int] = None,
        min_stars: Optional[int] = None
    ) -> Query:
        """构建语言统计查询"""
        if min_repos:
            query = query.filter(LanguageStats.repository_count >= min_repos)
        if min_stars:
            query = query.filter(LanguageStats.total_stars >= min_stars)
            
        return query.order_by(desc(LanguageStats.average_activity_score))

    @staticmethod
    def activity_changes(
        query: Query,
        min_change: Optional[float] = None,
        positive_only: bool = False
    ) -> Query:
        """构建活跃度变化查询"""
        if min_change:
            query = query.filter(ActivityChanges.activity_change >= min_change)
        if positive_only:
            query = query.filter(ActivityChanges.activity_change > 0)
            
        return query.order_by(desc(ActivityChanges.activity_change))