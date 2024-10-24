import pytest
import sqlite3
from datetime import datetime
from src.database.db_manager import DatabaseManager
from src.utils.exceptions import DatabaseException

@pytest.fixture
def db_manager():
    # 使用内存数据库进行测试
    manager = DatabaseManager(':memory:')
    manager.init_database()
    return manager

@pytest.fixture
def sample_repo_data():
    return {
        'name': 'test/repo',
        'url': 'https://github.com/test/repo',
        'description': 'Test repository',
        'language': 'Python',
        'stars': 100,
        'forks': 50,
        'open_issues': 10,
        'watchers': 100,
        'contributors_count': 5,
        'recent_commits': 20,
        'activity_score': 75.5,
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat(),
        'crawled_at': datetime.now().isoformat()
    }

def test_save_repository(db_manager, sample_repo_data):
    db_manager.save_repositories([sample_repo_data])
    repos = db_manager.get_trending_analysis(days=1)
    assert len(repos) == 1
    assert repos[0][0] == sample_repo_data['name']

def test_get_trending_analysis(db_manager, sample_repo_data):
    # 保存多个仓库数据
    repos = [sample_repo_data.copy() for _ in range(3)]
    for i, repo in enumerate(repos):
        repo['name'] = f'test/repo{i}'
        repo['activity_score'] = 75.5 + i
    
    db_manager.save_repositories(repos)
    analysis = db_manager.get_trending_analysis(days=7)
    assert len(analysis) == 3
    assert analysis[0][1] > analysis[1][1]  # 验证按活跃度排序