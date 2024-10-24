# src/crawlers/github_crawler.py
import requests
from typing import Optional, Dict, List
from bs4 import BeautifulSoup
from datetime import datetime

from src.core.crawler import BaseCrawler
from src.core.base import DataContainer
from src.crawlers.extensions.rate_limiter import rate_limit
from src.crawlers.extensions.cache import cache

class GitHubCrawler(BaseCrawler):
    """GitHub趋势爬虫"""
    
    def __init__(self, token: Optional[str] = None):
        super().__init__()
        self.base_url = "https://github.com/trending"
        self.api_url = "https://api.github.com"
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'GitHub-Trending-Tracker'
        }
        if token:
            self.headers['Authorization'] = f'token {token}'

    @rate_limit(calls=30, period=60)
    @cache(ttl=300)
    def fetch(self, language: Optional[str] = None, since: str = "daily") -> DataContainer:
        """获取趋势数据"""
        url = f"{self.base_url}/{language}" if language else self.base_url
        params = {'since': since}
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return DataContainer(
                data=response.text,
                metadata={
                    'language': language,
                    'since': since,
                    'timestamp': datetime.now().isoformat()
                }
            )
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch data: {str(e)}")

    def parse(self, html: str) -> DataContainer:
        """解析HTML数据"""
        soup = BeautifulSoup(html, 'html.parser')
        repositories = []

        for article in soup.select('article.Box-row'):
            try:
                repo_data = self._extract_repository_info(article)
                if repo_data:
                    repositories.append(repo_data)
            except Exception as e:
                print(f"Error parsing repository: {str(e)}")

        return DataContainer(
            data=repositories,
            metadata={
                'count': len(repositories),
                'parsed_at': datetime.now().isoformat()
            }
        )

    def _extract_repository_info(self, article) -> Optional[Dict]:
        """提取仓库信息"""
        try:
            name = article.select_one('h2 a').get('href').strip('/')
            return {
                'name': name,
                'url': f"https://github.com/{name}",
                'description': self._get_description(article),
                'language': self._get_language(article),
                'stars': self._get_stars(article),
                'forks': self._get_forks(article),
                'today_stars': self._get_today_stars(article),
                'crawled_at': datetime.now().isoformat()
            }
        except Exception:
            return None

    def _get_description(self, article) -> Optional[str]:
        desc_elem = article.select_one('p')
        return desc_elem.text.strip() if desc_elem else None

    def _get_language(self, article) -> Optional[str]:
        lang_elem = article.select_one('[itemprop="programmingLanguage"]')
        return lang_elem.text.strip() if lang_elem else None

    def _get_stars(self, article) -> int:
        stars_elem = article.select_one('a[href$="/stargazers"]')
        return self._parse_number(stars_elem.text.strip()) if stars_elem else 0

    def _get_forks(self, article) -> int:
        forks_elem = article.select_one('a[href$="/forks"]')
        return self._parse_number(forks_elem.text.strip()) if forks_elem else 0

    def _get_today_stars(self, article) -> int:
        today_elem = article.select_one('span.d-inline-block.float-sm-right')
        return self._parse_number(today_elem.text.strip()) if today_elem else 0

    # src/crawlers/github_crawler.py (续)
    def _parse_number(self, text: str) -> int:
        """解析数字（处理k,m等单位）"""
        try:
            text = text.lower().strip().replace(',', '')
            if 'k' in text:
                return int(float(text.replace('k', '')) * 1000)
            elif 'm' in text:
                return int(float(text.replace('m', '')) * 1000000)
            return int(float(text))
        except (ValueError, TypeError):
            return 0

    def validate(self, data: DataContainer) -> bool:
        """验证数据有效性"""
        if not data.data:
            return False
        if not isinstance(data.data, list):
            return False
        return all(
            isinstance(repo, dict) and 
            'name' in repo and 
            'url' in repo 
            for repo in data.data
        )

    def validate_config(self) -> bool:
        """验证配置"""
        return all([
            self.base_url,
            self.api_url,
            self.headers.get('User-Agent')
        ])