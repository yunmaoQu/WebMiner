-- repositories_indexes.sql
-- 仓库表索引

-- 仓库名称索引
CREATE INDEX IF NOT EXISTS idx_repo_name ON repositories(name);

-- 编程语言索引
CREATE INDEX IF NOT EXISTS idx_repo_language ON repositories(language);

-- 活跃度评分索引
CREATE INDEX IF NOT EXISTS idx_activity_score ON repositories(activity_score);

-- 爬取时间索引
CREATE INDEX IF NOT EXISTS idx_crawled_at ON repositories(crawled_at);

-- 组合索引：语言和活跃度
CREATE INDEX IF NOT EXISTS idx_lang_activity ON repositories(language, activity_score);
