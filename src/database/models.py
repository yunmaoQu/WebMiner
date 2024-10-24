from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Repository(Base):
    """仓库模型"""
    __tablename__ = 'repositories'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    description = Column(String)
    language = Column(String)
    stars = Column(Integer, default=0)
    forks = Column(Integer, default=0)
    open_issues = Column(Integer, default=0)
    watchers = Column(Integer, default=0)
    contributors_count = Column(Integer, default=0)
    recent_commits = Column(Integer, default=0)
    activity_score = Column(Float, default=0.0)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    crawled_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    trending_history = relationship("TrendingHistory", back_populates="repository")
    
    # 联合唯一约束
    __table_args__ = (
        UniqueConstraint('name', 'crawled_at', name='uix_repo_name_crawled'),
    )

    def __repr__(self):
        return f"<Repository(name='{self.name}', language='{self.language}')>"


class TrendingHistory(Base):
    """趋势历史模型"""
    __tablename__ = 'trending_history'

    id = Column(Integer, primary_key=True)
    repository_name = Column(String, ForeignKey('repositories.name'), nullable=False)
    activity_score = Column(Float, default=0.0)
    stars = Column(Integer, default=0)
    forks = Column(Integer, default=0)
    open_issues = Column(Integer, default=0)
    watchers = Column(Integer, default=0)
    contributors_count = Column(Integer, default=0)
    date = Column(DateTime, default=datetime.utcnow)

    # 关系
    repository = relationship("Repository", back_populates="trending_history")
    
    # 联合唯一约束
    __table_args__ = (
        UniqueConstraint('repository_name', 'date', name='uix_repo_date'),
    )

    def __repr__(self):
        return f"<TrendingHistory(repo='{self.repository_name}', date='{self.date}')>"


class LanguageStats(Base):
    """语言统计模型"""
    __tablename__ = 'language_stats'

    id = Column(Integer, primary_key=True)
    language = Column(String, nullable=False)
    repository_count = Column(Integer, default=0)
    total_stars = Column(Integer, default=0)
    total_forks = Column(Integer, default=0)
    average_activity_score = Column(Float, default=0.0)
    date = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint('language', 'date', name='uix_lang_date'),
    )

    def __repr__(self):
        return f"<LanguageStats(language='{self.language}', date='{self.date}')>"


class ActivityChanges(Base):
    """活跃度变化模型"""
    __tablename__ = 'activity_changes'

    id = Column(Integer, primary_key=True)
    repository_name = Column(String, ForeignKey('repositories.name'), nullable=False)
    activity_change = Column(Float, default=0.0)
    stars_change = Column(Integer, default=0)
    forks_change = Column(Integer, default=0)
    issues_change = Column(Integer, default=0)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)

    # 关系
    repository = relationship("Repository")

    __table_args__ = (
        UniqueConstraint('repository_name', 'start_date', 'end_date', 
                        name='uix_repo_date_range'),
    )

    def __repr__(self):
        return f"<ActivityChanges(repo='{self.repository_name}', change='{self.activity_change}')>"