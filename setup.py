#!/usr/bin/env python3
"""
Setup script for Coding Agent package
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_path = Path(__file__).parent / "README.md"
long_description = ""
if readme_path.exists():
    long_description = readme_path.read_text()

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
    
    entry_points={
        "console_scripts": [
            "coding-agent=coding_agent.cli:main",
        ]
    },
    
    package_data={
        "coding_agent": [
            "templates/*.md",
            "templates/*.json",
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
