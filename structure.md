

```plaintext
github-trending-tracker/
├── .github/
│   └── workflows/
│       └── github-trending.yml    # GitHub Actions 配置
├── src/
│   ├── __init__.py
│   ├── core/                    # 核心功能模块
│   │   ├── __init__.py
│   │   ├── crawler.py          # 基础爬虫
│   │   ├── processor.py        # 数据处理
│   │   └── analyzer.py         # 数据分析
│   │
│   ├── crawlers/               # 具体爬虫实现
│   │   ├── __init__.py
│   │   ├── github_crawler.py   # GitHub爬虫
│   │   └── extensions/         # 爬虫扩展
│   │       ├── __init__.py
│   │       ├── rate_limiter.py
│   │       └── cache.py
│   │
│   ├── processors/             # 数据处理器
│   │   ├── __init__.py
│   │   ├── activity.py         # 活跃度计算
│   │   ├── language.py         # 语言统计
│   │   └── trending.py         # 趋势分析
│   │
│   ├── analyzers/              # 分析器
│   │   ├── __init__.py
│   │   ├── stats.py           # 统计分析
│   │   ├── trends.py          # 趋势分析
│   │   └── patterns.py        # 模式识别
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py          # 数据模型
│   │   ├── manager.py         # 数据库管理
│   │   └── session.py         # 会话管理
│   │
│   ├── reporters/              # 报告生成器
│   │   ├── __init__.py
│   │   ├── html_reporter.py
│   │   ├── email_reporter.py
│   │   └── chart_generator.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── logger.py
│       ├── cache.py
│       └── helpers.py
│
├── examples/                    # 简化后的示例
│   ├── __init__.py
│   ├── basic_tracker.py        # 基本追踪示例
│   ├── trend_analysis.py       # 趋势分析示例
│   └── automated_report.py     # 自动报告示例
│
│
├── docs/
│   ├── api.md                   # API 文档
│   ├── schema.md                # 数据库架构文档
│   ├── deployment.md            # 部署指南
│   └── contributing.md          # 贡献指南
│
├── migrations/                  # Alembic 数据库迁移
│   ├── README
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│
├── templates/                   # 报告模板
│   ├── email/
│   │   ├── daily_report.html
│   │   └── weekly_report.html
│   └── web/
│       ├── base.html
│       └── trending.html
│
├── scripts/                     # 实用脚本
│   ├── setup_database.py
│   ├── generate_report.py
│   └── cleanup_data.py
│
├── logs/                        # 日志文件目录
│   └── .gitkeep
│
├── reports/                     # 生成的报告目录
│   └── .gitkeep
│
├── .env.example                 # 环境变量示例
├── .gitignore                  # Git 忽略文件
├── LICENSE                     # 许可证文件
├── README.md                   # 项目说明文档
├── requirements.txt            # 项目依赖
├── setup.py                    # 打包配置文件
├── pytest.ini                  # pytest 配置
└── tox.ini                     # tox 配置
```

主要目录说明：

1. **src/**: 源代码目录
   - crawler/: 爬虫模块
   - database/: 数据库模块
   - notification/: 通知模块
   - utils/: 工具模块

2. **data/**: 数据目录
   - sql/: SQL 文件
   - 数据库文件

3. **tests/**: 测试目录
   - 单元测试
   - 集成测试

4. **examples/**: 示例代码目录
   - 基本用法
   - 高级示例
   - 配置示例

5. **docs/**: 文档目录
   - API 文档
   - 架构文档
   - 部署指南

6. **migrations/**: 数据库迁移
   - Alembic 配置
   - 迁移脚本

7. **templates/**: 模板目录
   - 邮件模板
   - Web 模板

8. **scripts/**: 实用脚本
   - 设置脚本
   - 维护脚本

9. **logs/**: 日志目录

10. **reports/**: 报告目录

配置文件：
- .env.example: 环境变量示例
- requirements.txt: 项目依赖
- setup.py: 打包配置
- pytest.ini: 测试配置
- tox.ini: 测试自动化配置

