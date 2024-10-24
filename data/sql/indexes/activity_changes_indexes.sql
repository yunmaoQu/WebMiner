-- activity_changes_indexes.sql
-- 活跃度变化表索引

-- 日期范围索引
CREATE INDEX IF NOT EXISTS idx_activity_changes_dates ON activity_changes(start_date, end_date);

-- 仓库名称索引
CREATE INDEX IF NOT EXISTS idx_activity_changes_repo ON activity_changes(repository_name);

-- 活跃度变化索引
CREATE INDEX IF NOT EXISTS idx_activity_change ON activity_changes(activity_change);
