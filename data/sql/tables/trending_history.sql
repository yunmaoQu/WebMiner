-- trending_history.sql
-- 记录仓库趋势历史数据

CREATE TABLE IF NOT EXISTS trending_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    repository_name TEXT NOT NULL,         -- 仓库名称
    activity_score REAL DEFAULT 0.0,       -- 活跃度评分
    stars INTEGER DEFAULT 0,               -- 当时的star数量
    forks INTEGER DEFAULT 0,               -- 当时的fork数量
    open_issues INTEGER DEFAULT 0,         -- 当时的开放issue数量
    watchers INTEGER DEFAULT 0,            -- 当时的关注者数量
    contributors_count INTEGER DEFAULT 0,   -- 当时的贡献者数量
    date TEXT NOT NULL,                    -- 记录日期
    UNIQUE(repository_name, date)
);
