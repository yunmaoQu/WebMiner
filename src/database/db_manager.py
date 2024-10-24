from typing import Optional, List
from .session import get_db_session
from .query_builder import QueryBuilder
from .cache import CacheManager

class DatabaseManager:
    def __init__(
        self,
        db_url: str = 'sqlite:///data/github_trending.db',
        redis_url: Optional[str] = None
    ):
        # ... (之前的初始化代码)
        
        # 初始化缓存管理器
        self.cache = CacheManager(redis_url) if redis_url else None
        
        # 初始化查询构建器
        self.query_builder = QueryBuilder()

    @property
    def cache_enabled(self) -> bool:
        """检查缓存是否启用"""
        return self.cache is not None

    def get_trending_repositories(
        self,
        language: Optional[str] = None,
        min_stars: Optional[int] = None,
        min_activity: Optional[float] = None,
        limit: int = 20
    ) -> List[Repository]:
        """获取趋势仓库"""
        
        # 如果启用了缓存，使用缓存装饰器
        if self.cache_enabled:
            @self.cache.cache(prefix="trending", expire=300)
            def get_repos():
                with get_db_session(self) as session:
                    query = session.query(Repository)
                    query = self.query_builder.trending_repositories(
                        query,
                        language=language,
                        min_stars=min_stars,
                        min_activity=min_activity,
                        limit=limit
                    )
                    return query.all()
            return get_repos()
        
        # 未启用缓存时直接查询
        with get_db_session(self) as session:
            query = session.query(Repository)
            query = self.query_builder.trending_repositories(
                query,
                language=language,
                min_stars=min_stars,
                min_activity=min_activity,
                limit=limit
            )
            return query.all()

    def get_language_statistics(
        self,
        min_repos: Optional[int] = None,
        min_stars: Optional[int] = None
    ) -> List[LanguageStats]:
        """获取语言统计"""
        if self.cache_enabled:
            @self.cache.cache(prefix="lang_stats", expire=3600)
            def get_stats():
                with get_db_session(self) as session:
                    query = session.query(LanguageStats)
                    query = self.query_builder.language_statistics(
                        query,
                        min_repos=min_repos,
                        min_stars=min_stars
                    )
                    return query.all()
            return get_stats()

        with get_db_session(self) as session:
            query = session.query(LanguageStats)
            query = self.query_builder.language_statistics(
                query,
                min_repos=min_repos,
                min_stars=min_stars
            )
            return query.all()

    def get_activity_changes(
        self,
        min_change: Optional[float] = None,
        positive_only: bool = False
    ) -> List[ActivityChanges]:
        """获取活跃度变化"""
        if self.cache_enabled:
            @self.cache.cache(prefix="activity", expire=300)
            def get_changes():
                with get_db_session(self) as session:
                    query = session.query(ActivityChanges)
                    query = self.query_builder.activity_changes(
                        query,
                        min_change=min_change,
                        positive_only=positive_only
                    )
                    return query.all()
            return get_changes()

        with get_db_session(self) as session:
            query = session.query(ActivityChanges)
            query = self.query_builder.activity_changes(
                query,
                min_change=min_change,
                positive_only=positive_only
            )
            return query.all()

    def bulk_save_repositories(self, repositories: List[Dict[str, Any]]) -> None:
        """批量保存仓库数据"""
        try:
            with get_db_session(self) as session:
                # 批量插入或更新仓库
                for repo_data in repositories:
                    repo = session.query(Repository).filter_by(
                        name=repo_data['name']
                    ).first() or Repository()
                    
                    for key, value in repo_data.items():
                        if hasattr(repo, key):
                            setattr(repo, key, value)
                    
                    session.add(repo)
                
                # 提交事务
                session.commit()
                
                # 如果启用了缓存，清除相关缓存
                if self.cache_enabled:
                    self.cache.invalidate("trending")
                    self.cache.invalidate("lang_stats")
                    
                logger.info(f"Bulk saved {len(repositories)} repositories")
                
        except SQLAlchemyError as e:
            logger.error(f"Error in bulk save: {e}")
            raise

    def update_activity_scores(self) -> None:
        """更新所有仓库的活跃度分数"""
        try:
            with get_db_session(self) as session:
                repositories = session.query(Repository).all()
                
                for repo in repositories:
                    # 计算活跃度分数
                    activity_score = self._calculate_activity_score(
                        stars=repo.stars,
                        forks=repo.forks,
                        issues=repo.open_issues,
                        watchers=repo.watchers,
                        contributors=repo.contributors_count,
                        recent_commits=repo.recent_commits
                    )
                    
                    repo.activity_score = activity_score
                    
                session.commit()
                
                # 清除缓存
                if self.cache_enabled:
                    self.cache.invalidate("trending")
                    
                logger.info("Updated activity scores for all repositories")
                
        except SQLAlchemyError as e:
            logger.error(f"Error updating activity scores: {e}")
            raise

    def _calculate_activity_score(
        self,
        stars: int,
        forks: int,
        issues: int,
        watchers: int,
        contributors: int,
        recent_commits: int
    ) -> float:
        """
        计算仓库活跃度分数
        
        使用加权计算方法，可以根据需要调整权重
        """
        weights = {
            'stars': 0.3,
            'forks': 0.2,
            'issues': 0.1,
            'watchers': 0.1,
            'contributors': 0.15,
            'commits': 0.15
        }
        
        # 标准化各指标
        max_values = {
            'stars': 10000,
            'forks': 5000,
            'issues': 1000,
            'watchers': 10000,
            'contributors': 100,
            'commits': 1000
        }
        
        normalized_scores = {
            'stars': min(stars / max_values['stars'], 1),
            'forks': min(forks / max_values['forks'], 1),
            'issues': min(issues / max_values['issues'], 1),
            'watchers': min(watchers / max_values['watchers'], 1),
            'contributors': min(contributors / max_values['contributors'], 1),
            'commits': min(recent_commits / max_values['commits'], 1)
        }
        
        # 计算加权分数
        score = sum(
            normalized_scores[key] * weights[key]
            for key in weights
        ) * 100
        
        return round(score, 2)