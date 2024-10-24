import pytest
from unittest.mock import Mock, patch
from src.crawler.github_crawler import GitHubTrendingCrawler
from src.utils.exceptions import CrawlerException

@pytest.fixture
def crawler():
    return GitHubTrendingCrawler()

@pytest.fixture
def mock_response():
    with open('tests/fixtures/trending_page.html', 'r', encoding='utf-8') as f:
        return Mock(text=f.read(), status_code=200)

def test_fetch_trending_repositories(crawler, mock_response):
    with patch('requests.get', return_value=mock_response):
        repos = crawler.fetch_trending_repositories()
        assert len(repos) > 0
        assert all(key in repos[0] for key in [
            'name', 'url', 'description', 'language',
            'stars', 'forks', 'stars_today'
        ])

def test_fetch_trending_repositories_with_language(crawler, mock_response):
    with patch('requests.get', return_value=mock_response):
        repos = crawler.fetch_trending_repositories(language='python')
        assert len(repos) > 0
        assert all(repo['language'].lower() == 'python' for repo in repos)

def test_fetch_trending_repositories_error():
    with patch('requests.get', side_effect=Exception('Connection error')):
        with pytest.raises(CrawlerException):
            GitHubTrendingCrawler().fetch_trending_repositories()