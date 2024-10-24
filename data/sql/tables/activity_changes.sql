-- activity_changes.sql
-- 仓库活跃度变化记录

CREATE TABLE IF NOT EXISTS activity_changes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    repository_name TEXT NOT NULL,         -- 仓库名称
    activity_change REAL DEFAULT 0.0,      -- 活跃度变化
    stars_change INTEGER DEFAULT 0,        -- star变化
    forks_change INTEGER DEFAULT 0,        -- fork变化
    issues_change INTEGER DEFAULT 0,       -- issue变化
    start_date TEXT NOT NULL,             -- 开始日期
    end_date TEXT NOT NULL,               -- 结束日期
    UNIQUE(repository_name, start_date, end_date)
);
