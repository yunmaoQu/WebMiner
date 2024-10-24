-- repositories.sql
-- 存储GitHub仓库的基本信息和统计数据

CREATE TABLE IF NOT EXISTS repositories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,                    -- 仓库全名 (owner/repo)
    url TEXT NOT NULL,                     -- 仓库URL
    description TEXT,                      -- 仓库描述
    language TEXT,                         -- 主要编程语言
    stars INTEGER DEFAULT 0,               -- star数量
    forks INTEGER DEFAULT 0,               -- fork数量
    open_issues INTEGER DEFAULT 0,         -- 开放的issue数量
    watchers INTEGER DEFAULT 0,            -- 关注者数量
    contributors_count INTEGER DEFAULT 0,   -- 贡献者数量
    recent_commits INTEGER DEFAULT 0,       -- 最近提交数量
    activity_score REAL DEFAULT 0.0,       -- 活跃度评分
    created_at TEXT,                       -- 创建时间
    updated_at TEXT,                       -- 最后更新时间
    crawled_at TEXT,                       -- 数据爬取时间
    UNIQUE(name, crawled_at)
);
