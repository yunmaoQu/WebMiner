# setup.py
from setuptools import setup, find_packages
import os

# 读取 README.md 文件内容
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# 读取 requirements.txt 文件内容
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="github-trending-tracker",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool to track GitHub trending repositories with community activity analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/github-trending-tracker",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        'dev': [
            'pytest>=6.0',
            'pytest-cov>=2.0',
            'flake8>=3.9',
            'black>=21.0',
            'mypy>=0.910',
            'isort>=5.9',
        ],
    },
    entry_points={
        'console_scripts': [
            'github-trending=src.main:main',
        ],
    },
    package_data={
        'github_trending_tracker': [
            'config/*.json',
            'config/*.yml',
        ],
    },
    include_package_data=True,
    zip_safe=False,
    project_urls={
        'Bug Reports': 'https://github.com/yourusername/github-trending-tracker/issues',
        'Source': 'https://github.com/yourusername/github-trending-tracker',
    },
)