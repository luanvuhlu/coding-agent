# Coding Agent - AI-Powered Coding Patterns Library

A CLI tool that gives AI assistants (Claude, GPT, Copilot) access to curated Spring Boot coding patterns and tasks.

## Installation

Install from GitHub:

```bash
pip install git+https://github.com/YOUR_USERNAME/coding-agent-skills.git
```

Or install locally for development:

```bash
git clone https://github.com/YOUR_USERNAME/coding-agent-skills.git
cd coding-agent-skills
pip install -e .
```

## Quick Start

### 1. Initialize in your project

```bash
cd /path/to/your-spring-boot-project
coding-agent init claude
```

This creates `.coding-agent/` folder with patterns, tasks, code examples, and search tool.

### 2. Copy system prompt to Claude

```bash
cat .coding-agent/SYSTEM_PROMPT.md
```

Copy the content to your Claude conversation.

### 3. Start building!

Ask Claude:
- "Create a CRUD API for products"
- "Add JWT authentication"
- "Setup PostgreSQL database configuration"

Claude autonomously searches patterns, reads examples, and generates code.

## Features

✅ **Zero dependencies** - Pure Python  
✅ **Offline search** - Fast BM25 keyword search  
✅ **Simplified patterns** - Minimal JSON, maximum clarity  
✅ **Task workflows** - Multi-step guides  
✅ **Code templates** - Real Java examples  
✅ **AI-native** - Designed for autonomous AI use  

## Available Patterns

- **controller-layer** - REST API controllers
- **service-layer** - Business logic
- **repository-layer** - Data access with JPA
- **jwt-auth** - JWT authentication
- **application-yaml** - App configuration
- **logging** - Logback setup

## Available Tasks

- **create-crud-api** - Complete CRUD API (8 steps)
- **add-authentication** - JWT security (7 steps)

## Documentation

- [Installation Guide](INSTALL.md)
- [CLI Design](CLI-DESIGN.md)
- [Keyword Search Design](keyword-search-design.md)
- [Schema Documentation](schema-simplified.md)

## License

MIT License