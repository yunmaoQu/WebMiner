#!/bin/bash
# data/sql/init_sql.sh

# 设置颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# SQL 文件目录
SQL_ROOT="."
TABLES_DIR="${SQL_ROOT}/tables"
INDEXES_DIR="${SQL_ROOT}/indexes"
VIEWS_DIR="${SQL_ROOT}/views"

# 创建表文件
create_table_files() {
    echo -e "${BLUE}Creating table SQL files...${NC}"
    
    # repositories.sql
    cat > "${TABLES_DIR}/repositories.sql" << 'EOF'
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
EOF

    # trending_history.sql
    cat > "${TABLES_DIR}/trending_history.sql" << 'EOF'
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
EOF

    # language_stats.sql
    cat > "${TABLES_DIR}/language_stats.sql" << 'EOF'
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
EOF

    # activity_changes.sql
    cat > "${TABLES_DIR}/activity_changes.sql" << 'EOF'
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
EOF

    echo -e "${GREEN}Table SQL files created successfully${NC}"
}

# 创建索引文件
create_index_files() {
    echo -e "${BLUE}Creating index SQL files...${NC}"
    
    # repositories_indexes.sql
    cat > "${INDEXES_DIR}/repositories_indexes.sql" << 'EOF'
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
EOF

    # trending_history_indexes.sql
    cat > "${INDEXES_DIR}/trending_history_indexes.sql" << 'EOF'
-- trending_history_indexes.sql
-- 趋势历史表索引

-- 日期索引
CREATE INDEX IF NOT EXISTS idx_trending_history_date ON trending_history(date);

-- 仓库名称索引
CREATE INDEX IF NOT EXISTS idx_trending_history_repo ON trending_history(repository_name);

-- 组合索引：仓库和日期
CREATE INDEX IF NOT EXISTS idx_repo_date ON trending_history(repository_name, date);
EOF

    # language_stats_indexes.sql
    cat > "${INDEXES_DIR}/language_stats_indexes.sql" << 'EOF'
-- language_stats_indexes.sql
-- 语言统计表索引

-- 日期索引
CREATE INDEX IF NOT EXISTS idx_language_stats_date ON language_stats(date);

-- 语言索引
CREATE INDEX IF NOT EXISTS idx_language_stats_lang ON language_stats(language);

-- 活跃度索引
CREATE INDEX IF NOT EXISTS idx_language_stats_activity ON language_stats(average_activity_score);
EOF

    # activity_changes_indexes.sql
    cat > "${INDEXES_DIR}/activity_changes_indexes.sql" << 'EOF'
-- activity_changes_indexes.sql
-- 活跃度变化表索引

-- 日期范围索引
CREATE INDEX IF NOT EXISTS idx_activity_changes_dates ON activity_changes(start_date, end_date);

-- 仓库名称索引
CREATE INDEX IF NOT EXISTS idx_activity_changes_repo ON activity_changes(repository_name);

-- 活跃度变化索引
CREATE INDEX IF NOT EXISTS idx_activity_change ON activity_changes(activity_change);
EOF

    echo -e "${GREEN}Index SQL files created successfully${NC}"
}

# 创建视图文件
create_view_files() {
    echo -e "${BLUE}Creating view SQL files...${NC}"
    
    # recent_trending_repos.sql
    cat > "${VIEWS_DIR}/recent_trending_repos.sql" << 'EOF'
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
EOF

    # language_trends.sql
    cat > "${VIEWS_DIR}/language_trends.sql" << 'EOF'
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
EOF

    echo -e "${GREEN}View SQL files created successfully${NC}"
}

# 验证SQL文件
validate_sql_files() {
    echo -e "${BLUE}Validating SQL files...${NC}"
    local has_error=0

    # 使用 sqlite3 验证每个 SQL 文件的语法
    for sql_file in $(find . -name "*.sql"); do
        if ! sqlite3 :memory: < "$sql_file" > /dev/null 2>&1; then
            echo -e "${RED}Error in $sql_file${NC}"
            sqlite3 :memory: < "$sql_file"
            has_error=1
        else
            echo -e "${GREEN}✓ $sql_file is valid${NC}"
        fi
    done

    if [ $has_error -eq 1 ]; then
        echo -e "${RED}SQL validation failed${NC}"
        exit 1
    else
        echo -e "${GREEN}All SQL files are valid${NC}"
    fi
}

# 创建测试数据
create_test_data() {
    echo -e "${BLUE}Creating test data SQL file...${NC}"
    
    cat > "${SQL_ROOT}/test_data.sql" << 'EOF'
-- test_data.sql
-- 测试数据

-- 插入示例仓库数据
INSERT INTO repositories (
    name, url, description, language, stars, forks,
    open_issues, watchers, contributors_count, recent_commits,
    activity_score, created_at, updated_at, crawled_at
) VALUES 
    ('test/repo1', 'https://github.com/test/repo1', 'Test Repository 1', 'Python', 1000, 500, 50, 1000, 20, 30, 85.5, '2023-01-01', '2023-12-01', datetime('now')),
    ('test/repo2', 'https://github.com/test/repo2', 'Test Repository 2', 'Java', 800, 400, 30, 800, 15, 25, 75.5, '2023-02-01', '2023-12-01', datetime('now'));

-- 插入趋势历史数据
INSERT INTO trending_history (
    repository_name, activity_score, stars, forks,
    open_issues, watchers, contributors_count, date
) VALUES 
    ('test/repo1', 80.0, 950, 480, 45, 950, 18, date('now', '-1 day')),
    ('test/repo2', 70.0, 750, 380, 28, 750, 14, date('now', '-1 day'));

-- 插入语言统计数据
INSERT INTO language_stats (
    language, repository_count, total_stars,
    total_forks, average_activity_score, date
) VALUES 
    ('Python', 1, 1000, 500, 85.5, date('now')),
    ('Java', 1, 800, 400, 75.5, date('now'));
EOF

    echo -e "${GREEN}Test data SQL file created successfully${NC}"
}

# 显示帮助信息
show_help() {
    echo -e "${YELLOW}Usage: $0 [OPTION]${NC}"
    echo "Options:"
    echo "  -h, --help        显示帮助信息"
    echo "  -i, --init        初始化所有SQL文件"
    echo "  -v, --validate    验证SQL文件"
    echo "  -t, --test        创建测试数据"
    echo "  --tables          只创建表定义"
    echo "  --indexes         只创建索引"
    echo "  --views           只创建视图"
}

# 主函数
main() {
    # 如果没有参数，显示帮助信息
    if [ $# -eq 0 ]; then
        show_help
        exit 1
    fi

    # 处理命令行参数
    while [ "$1" != "" ]; do
        case $1 in
            -h | --help )
                show_help
                exit 0
                ;;
            -i | --init )
                create_table_files
                create_index_files
                create_view_files
                validate_sql_files
                ;;
            -v | --validate )
                validate_sql_files
                ;;
            -t | --test )
                create_test_data
                ;;
            --tables )
                create_table_files
                ;;
            --indexes )
                create_index_files
                ;;
            --views )
                create_view_files
                ;;
            * )
                echo -e "${RED}Unknown parameter: $1${NC}"
                show_help
                exit 1
                ;;
        esac
        shift
    done
}

# 检查必要的目录
check_directories() {
    for dir in "$TABLES_DIR" "$INDEXES_DIR" "$VIEWS_DIR"; do
        if [ ! -d "$dir" ]; then
            echo -e "${BLUE}Creating directory: $dir${NC}"
            mkdir -p "$dir"
        fi
    done
}

# 运行前检查目录
check_directories

# 执行主函数
main "$@"