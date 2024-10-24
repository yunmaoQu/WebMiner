-- language_trends.sql
-- 编程语言趋势视图

CREATE VIEW IF NOT EXISTS language_trends AS
SELECT 
    language,
    COUNT(*) as repo_count,
    SUM(stars) as total_stars,
    SUM(forks) as total_forks,
    AVG(activity_score) as avg_activity_score,
    MAX(crawled_at) as last_updated,
    SUM(CASE WHEN crawled_at >= date('now', '-7 days') THEN 1 ELSE 0 END) as recent_repos_count
FROM repositories
WHERE 
    crawled_at >= date('now', '-30 days')
    AND language IS NOT NULL
GROUP BY language
HAVING repo_count > 0
ORDER BY avg_activity_score DESC;
