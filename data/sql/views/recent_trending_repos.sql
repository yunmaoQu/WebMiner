-- recent_trending_repos.sql
-- 最近趋势仓库视图

CREATE VIEW IF NOT EXISTS recent_trending_repos AS
SELECT 
    r.*,
    th.activity_score as previous_score,
    (r.activity_score - th.activity_score) as score_change,
    (r.stars - th.stars) as stars_change,
    (r.forks - th.forks) as forks_# 继续 create_view_files() 函数

    # recent_trending_repos.sql (续)
    cat > "${VIEWS_DIR}/recent_trending_repos.sql" << 'EOF'
-- recent_trending_repos.sql
-- 最近趋势仓库视图

CREATE VIEW IF NOT EXISTS recent_trending_repos AS
SELECT 
    r.*,
    th.activity_score as previous_score,
    (r.activity_score - th.activity_score) as score_change,
    (r.stars - th.stars) as stars_change,
    (r.forks - th.forks) as forks_change,
    (r.open_issues - th.open_issues) as issues_change,
    th.date as previous_date
FROM repositories r
LEFT JOIN trending_history th ON 
    th.repository_name = r.name AND 
    th.date = date(r.crawled_at, '-1 day')
WHERE r.crawled_at >= date('now', '-7 days')
ORDER BY r.activity_score DESC;
