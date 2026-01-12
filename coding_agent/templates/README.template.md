# Coding Agent

This folder contains your project's coding pattern library and search tools.

## Quick Reference

### Search for Patterns
```bash
python search_engine.py "create rest api"
python search_engine.py "add authentication" 
python search_engine.py "database configuration"
```

### View Available Patterns
```bash
ls -la patterns/
```

### View Available Tasks
```bash
ls -la tasks/
```

### View Code Examples
```bash
ls -la code/
```

## How to Use

1. **Copy system prompt** to your AI chat tool
   ```bash
   cat SYSTEM_PROMPT.md
   ```

2. **Ask your AI** to help build features:
   - "Create a CRUD API for products"
   - "Add JWT authentication"
   - "Setup database migrations"

3. **AI will search** your local pattern library
4. **AI will generate** code based on examples
5. **You implement** with AI guidance

## Pattern Structure

Each pattern file (e.g., `controller-layer.json`) contains:
- **id** - Unique pattern identifier
- **name** - Human-readable name
- **description** - What it does
- **keywords** - Search terms
- **steps** - Implementation steps
- **dependencies** - Required Maven dependencies
- **notes** - Best practices and tips

## Task Structure

Each task file (e.g., `create-crud-api.json`) contains:
- **id** - Unique task identifier
- **name** - Human-readable name
- **description** - Complete workflow description
- **tasks** - Ordered list of pattern-based steps
- **variables** - Parameterized inputs
- **dependencies** - All required dependencies
- **checklist** - Verification steps

## File Storage

- ✅ `patterns/` - Reusable pattern components
- ✅ `tasks/` - Multi-step workflows
- ✅ `code/` - Code examples and templates
- ✅ `config.json` - Project configuration
- ✅ `search_engine.py` - Local search tool

## Next Steps

1. Review the available patterns in `patterns/`
2. Copy `SYSTEM_PROMPT.md` to your AI chat
3. Start building! 🚀

---

**Note:** This folder is auto-generated and should NOT be committed to version control.
See `.gitignore` for exclusion rules.