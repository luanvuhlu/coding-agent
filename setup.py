#!/usr/bin/env python3
"""
Setup script for Coding Agent package
"""

from setuptools import setup, find_packages
from pathlib import Path
import os

# Read README
readme_path = Path(__file__).parent / "README.md"
long_description = ""
if readme_path.exists():
    long_description = readme_path.read_text()

# Collect all data files
def collect_data_files(directory):
    """Recursively collect all files in a directory"""
    paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            # Make path relative to package root
            rel_path = os.path.relpath(file_path, '.')
            paths.append(rel_path)
    return paths

# Collect patterns, tasks, code files
data_files = []
data_files.extend(collect_data_files('data'))
data_files.extend(collect_data_files('code'))

setup(
    name="coding-agent",
    version="0.1.0",
    description="AI-powered coding patterns and tasks library for Spring Boot projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Coding Agent",
    author_email="",
    url="https://github.com/yourusername/coding-agent",
    license="MIT",
    
    packages=find_packages(),
    include_package_data=True,
    
    # Include data files outside of packages
    data_files=[
        ('data/patterns', [f for f in data_files if f.startswith('data/patterns')]),
        ('data/tasks', [f for f in data_files if f.startswith('data/tasks')]),
        ('code', [f for f in data_files if f.startswith('code')]),
    ],
    
    entry_points={
        "console_scripts": [
            "coding-agent=coding_agent.cli:main",
        ]
    },
    
    package_data={
        "": [
            "search_engine.py",
            "data/patterns/*.json",
            "data/tasks/*.json",
            "code/*.java",
            "code/*.xml",
        ]
    },
    
    python_requires=">=3.7",
    install_requires=[],  # Zero dependencies!
    
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
