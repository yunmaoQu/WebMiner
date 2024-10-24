

# GitHub Trending Tracker

A Python tool to track GitHub trending repositories with community activity analysis. This tool automatically collects data from GitHub trending pages, analyzes repository activity, and sends daily reports via email.

## Features

- Track GitHub trending repositories across multiple programming languages
- Analyze repository community activity (issues, commits, contributors)
- Store historical data in SQLite database
- Send daily email reports with trending analysis
- Support for GitHub Actions automation
- Extensive logging and error handling

## Installation

### From PyPI

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

## Configuration

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Edit `.env` with your settings:
```ini
GITHUB_TOKEN=your_github_token
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
RECIPIENT_EMAILS=recipient1@example.com,recipient2@example.com
```

## Usage

### Command Line

```bash
# Run the tracker
github-trending

# With specific languages
github-trending --languages python,java,javascript

# With different time period
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

## Development

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

# Run with coverage report
pytest --cov=src tests/

# Run specific test file
pytest tests/test_crawler.py
```

### Code Style

This project uses:
- Black for code formatting
- Flake8 for style guide enforcement
- MyPy for type checking
- isort for import sorting

```bash
# Format code
black src tests

# Check style
flake8 src tests

# Sort imports
isort src tests

# Type checking
mypy src
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Acknowledgments

- GitHub Trending page for providing the data
- All contributors who have helped with the project


