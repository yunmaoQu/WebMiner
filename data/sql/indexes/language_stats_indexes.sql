-- language_stats_indexes.sql
-- 语言统计表索引

-- 日期索引
CREATE INDEX IF NOT EXISTS idx_language_stats_date ON language_stats(date);

-- 语言索引
CREATE INDEX IF NOT EXISTS idx_language_stats_lang ON language_stats(language);

-- 活跃度索引
CREATE INDEX IF NOT EXISTS idx_language_stats_activity ON language_stats(average_activity_score);
