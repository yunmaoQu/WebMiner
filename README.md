# 🚀 GitHub Trending Tracker

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/yunmaoQu/WebMiner?style=social)](https://github.com/yunmaoQu/WebMiner)

*A powerful tool for automatically tracking GitHub trending repositories and analyzing community activity*

[Features](#✨-features) • [Installation](#📦-installation) • [Configuration](#⚙️-configuration) • [Usage](#🔨-usage) • [Development](#💻-development) • [Contributing](#🤝-contributing)

</div>

## ✨ Features

- 🔍 Track GitHub trending repositories across multiple programming languages
- 📊 Deep analysis of repository community activity (issues, commits, contributors)
- 💾 Historical data storage using SQLite database
- 📧 Automated daily trend analysis reports
- 🔄 GitHub Actions automation support
- 📝 Comprehensive logging and error handling

## 📦 Installation

### Via PyPI

```bash
pip install github-trending-tracker
```

### From Source

```bash
git clone https://github.com/yourusername/github-trending-tracker.git
cd github-trending-tracker
pip install -e .
```

### Development Installation

```bash
pip install -e ".[dev]"
```

## ⚙️ Configuration

1. Copy configuration template:
```bash
cp .env.example .env
```

2. Edit `.env` file:
```ini
GITHUB_TOKEN=your_github_token
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
RECIPIENT_EMAILS=recipient1@example.com,recipient2@example.com
```

## 🔨 Usage

### Command Line Interface

```bash
# Run tracker
github-trending

# Specify programming languages
github-trending --languages python,java,javascript

# Set time period
github-trending --period weekly
```

### As a Library

```python
from github_trending_tracker import GitHubTrendingCrawler, DatabaseManager, EmailNotifier

# Initialize components
crawler = GitHubTrendingCrawler()
db_manager = DatabaseManager()
email_notifier = EmailNotifier()

# Fetch trending repositories
repos = crawler.fetch_trending_repositories(languages=['python', 'java'])

# Save to database
db_manager.save_repositories(repos)

# Send report
email_notifier.send_trending_report(repos)
```

## 💻 Development

### Setup Development Environment

```bash
# Install development dependencies
pip install -e ".[dev]"

# Setup pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Generate coverage report
pytest --cov=src tests/

# Run specific test file
pytest tests/test_crawler.py
```

### Code Style

This project uses:
- 🎨 Black for code formatting
- 🔍 Flake8 for style enforcement
- ✅ MyPy for type checking
- 📋 isort for import sorting

```bash
# Format code
black src tests

# Check style
flake8 src tests

# Sort imports
isort src tests

# Type check
mypy src
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## 🤝 Contributing

Contributions are welcome! Feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ⭐ Give us a star if you like this project!

---

<div align="center">
Made with ❤️ by Contributors
</div>
