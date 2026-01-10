#!/usr/bin/env python3
"""
CLI entry point for Coding Agent
Usage: coding-agent init <provider>
"""

import argparse
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Coding Agent - AI-powered coding patterns and tasks",
        prog="coding-agent"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize coding-agent in current project")
    init_parser.add_argument(
        "provider",
        choices=["claude", "gpt", "copilot"],
        help="AI provider to use"
    )
    init_parser.add_argument(
        "--project-name",
        help="Project name (auto-detected if not provided)"
    )
    
    args = parser.parse_args()
    
    if args.command == "init":
        from .init import init_project
        init_project(args.provider)
    elif args.command is None:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
