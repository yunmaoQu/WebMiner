# config/settings.py
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 数据库配置
DATABASE = {
    'name': os.getenv('DB_NAME', 'github_trending.db'),
    'path': os.path.join('data', os.getenv('DB_NAME', 'github_trending.db'))
}

# GitHub配置
GITHUB = {
    'token': os.getenv('GITHUB_TOKEN'),
    'languages': ['python', 'java', 'javascript', 'go', 'rust'],
    'trending_url': 'https://github.com/trending'
}

# 邮件配置
EMAIL = {
    'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
    'smtp_port': int(os.getenv('SMTP_PORT', '587')),
    'sender_email': os.getenv('SENDER_EMAIL'),
    'sender_password': os.getenv('SENDER_PASSWORD'),
    'recipient_emails': os.getenv('RECIPIENT_EMAILS', '').split(',')
}

# 日志配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': f'logs/github_trending_{datetime.now().strftime("%Y%m%d")}.log',
            'formatter': 'standard'
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        }
    }
}