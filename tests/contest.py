# tests/conftest.py
import pytest
import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Base
from src.database.db_manager import DatabaseManager

@pytest.fixture(scope="session")
def test_db_path(tmp_path_factory):
    """创建测试数据库路径"""
    db_dir = tmp_path_factory.mktemp("data")
    return db_dir / "test.db"

@pytest.fixture(scope="session")
def test_db_url(test_db_path):
    """创建测试数据库URL"""
    return f"sqlite:///{test_db_path}"

@pytest.fixture(scope="session")
def db_engine(test_db_url):
    """创建测试数据库引擎"""
    engine = create_engine(test_db_url)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)

@pytest.fixture(scope="function")
def db_session(db_engine):
    """创建测试数据库会话"""
    Session = sessionmaker(bind=db_engine)
    session = Session()
    yield session
    session.rollback()
    session.close()

@pytest.fixture(scope="function")
def db_manager(test_db_url):
    """创建测试数据库管理器"""
    return DatabaseManager(db_url=test_db_url)

@pytest.fixture
def sample_repo_data():
    """示例仓库数据"""
    return {
        'name': 'test/repo',
        'url': 'https://github.com/test/repo',
        'description': 'Test repository',
        'language': 'Python',
        'stars': 1000,
        'forks': 500,
        'open_issues': 50,
        'watchers': 1000,
        'contributors_count': 20,
        'recent_commits': 30,
        'activity_score': 85.5
    }

@pytest.fixture
def mock_github_response():
    """模拟GitHub API响应"""
    return {
        'items': [
            {
                'full_name': 'test/repo',
                'html_url': 'https://github.com/test/repo',
                'description': 'Test repository',
                'language': 'Python',
                'stargazers_count': 1000,
                'forks_count': 500,
                'open_issues_count': 50,
                'watchers_count': 1000
            }
        ]
    }

@pytest.fixture
def clean_test_db(db_session):
    """清理测试数据库"""
    yield db_session
    for table in reversed(Base.metadata.sorted_tables):
        db_session.execute(table.delete())
    db_session.commit()