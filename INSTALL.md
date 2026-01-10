# Installation Guide

## Install from Source (Development)

```bash
# Clone the repository
git clone https://github.com/yourusername/coding-agent-skills.git
cd coding-agent-skills

# Install in editable mode
pip install -e .

# Verify installation
coding-agent --help
```

## Initialize in Your Project

```bash
cd /path/to/your/project
coding-agent init claude
```

This creates a `.coding-agent/` folder with:
- `patterns/` - Pattern library
- `tasks/` - Task workflows  
- `code/` - Code examples
- `search_engine.py` - Search tool
- `SYSTEM_PROMPT.md` - Instructions for Claude
- `README.md` - Quick reference
- `config.json` - Project config

## Verify Installation

```bash
# Check that files were created
ls -la .coding-agent/

# Test search
python .coding-agent/search_engine.py "create rest api"
```

## Troubleshooting

### Error: "Could not find data directory"

This means the package wasn't installed correctly. Try:

```bash
# Uninstall first
pip uninstall coding-agent

# Reinstall in editable mode from repo root
cd /path/to/coding-agent-skills
pip install -e .
```

### No patterns/tasks/code folders created

Check if symlinks failed (Windows):
1. Run as Administrator, or
2. The init script will copy files instead of symlinking

### search_engine.py not found

Make sure `search_enhanced.py` exists in the repo root before installing.

## Usage

Once initialized, copy the system prompt to Claude:

```bash
cat .coding-agent/SYSTEM_PROMPT.md
```

Then ask Claude to help with your project!
