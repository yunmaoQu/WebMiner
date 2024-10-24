-- language_stats.sql
-- 编程语言统计信息

CREATE TABLE IF NOT EXISTS language_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    language TEXT NOT NULL,                -- 编程语言名称
    repository_count INTEGER DEFAULT 0,     -- 仓库数量
    total_stars INTEGER DEFAULT 0,         -- 总star数
    total_forks INTEGER DEFAULT 0,         -- 总fork数
    average_activity_score REAL DEFAULT 0.0, -- 平均活跃度
    date TEXT NOT NULL,                    -- 统计日期
    UNIQUE(language, date)
);
