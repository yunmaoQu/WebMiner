-- trending_history_indexes.sql
-- 趋势历史表索引

-- 日期索引
CREATE INDEX IF NOT EXISTS idx_trending_history_date ON trending_history(date);

-- 仓库名称索引
CREATE INDEX IF NOT EXISTS idx_trending_history_repo ON trending_history(repository_name);

-- 组合索引：仓库和日期
CREATE INDEX IF NOT EXISTS idx_repo_date ON trending_history(repository_name, date);
