# main.py
import logging
import os
from datetime import datetime
from github_crawler import GitHubTrendingCrawler
from db_manager import DatabaseManager
from email_notifier import EmailNotifier

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('github_trending.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
def main():
    crawler = GitHubTrendingCrawler()
    
    # 定义要抓取的语言列表
    languages = [  # None 表示所有语言
        "python",
        "java",
        "go",
        "rust",
        "c++",
    ]
    
    # 定义时间范围
    time_ranges = ["daily"] # "weekly", "monthly"
    
    all_trending_repos = []
    
    try:
        for language in languages:
            for time_range in time_ranges:
                logger.info(f"\nFetching {time_range} trending for {language if language else 'all languages'}...")
                
                repos = crawler.fetch_trending_repositories(
                    language=language,
                    since=time_range
                )
                
                if repos:
                    all_trending_repos.extend(repos)
                    
                # 添加延时以避免请求过于频繁
                time.sleep(2)
        
        if all_trending_repos:
            # 去重（可能不同时间范围会有重复的仓库）
            unique_repos = {repo['name']: repo for repo in all_trending_repos}.values()
            unique_repos = list(unique_repos)
            
            # 保存数据
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # 保存为CSV
            csv_filename = f'github_trending_{timestamp}.csv'
            crawler.save_to_csv(unique_repos, csv_filename)
            
            # 保存为HTML
            html_filename = f'github_trending_{timestamp}.html'
            crawler.save_to_html(unique_repos, html_filename)
            
            # 打印摘要
            crawler.print_summary(unique_repos)
            
            logger.info(f"\nTotal unique repositories collected: {len(unique_repos)}")
            logger.info(f"Data saved to {csv_filename} and {html_filename}")
            
        else:
            logger.warning("No trending repositories found")
            
    except Exception as e:
        logger.error(f"An error occurred in main execution: {e}", exc_info=True)

if __name__ == "__main__":
    main()