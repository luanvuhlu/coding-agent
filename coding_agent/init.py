#!/usr/bin/env python3
"""
Project initialization logic for Coding Agent
Creates .coding-agent folder with patterns, tasks, and search engine
"""

import json
import shutil
import sys
from pathlib import Path


def init_project(provider, project_name=None):
    """
    Initialize coding-agent in the current project
    
    Args:
        provider: AI provider (claude, gpt, copilot)
        project_name: Optional project name (auto-detected if not provided)
    """
    cwd = Path.cwd()
    
    # Auto-detect project name
    if not project_name:
        project_name = cwd.name
    
    # Create .coding-agent directory
    coding_agent_dir = cwd / ".coding-agent"
    
    if coding_agent_dir.exists():
        print(f"❌ Error: {coding_agent_dir} already exists!")
        sys.exit(1)
    
    print(f"✨ Initializing Coding Agent in '{cwd.name}' project...")
    print(f"📁 Creating .coding-agent directory...")
    
    coding_agent_dir.mkdir(parents=True, exist_ok=True)
    
    # Resolve library root directory (support installed package and repo layout)
    package_dir = Path(__file__).parent  # coding_agent package directory
    # Prefer an ancestor that contains 'data' directory
    lib_root = None
    for candidate in (package_dir, package_dir.parent, package_dir.parent.parent):
        if (candidate / "data").exists():
            lib_root = candidate
            break
    if lib_root is None:
        # Fallback to package_dir
        lib_root = package_dir

    lib_data = lib_root / "data"
    lib_code = lib_root / "code"

    # 1. Create config.json
    print("📝 Creating config.json...")
    config = {
        "project_name": project_name,
        "ai_provider": provider,
        "version": "0.1.0",
        "patterns_path": "patterns",
        "tasks_path": "tasks",
        "code_path": "code",
        "search_engine": "search_engine.py"
    }

    with open(coding_agent_dir / "config.json", 'w') as f:
        json.dump(config, f, indent=2)

    # 2. Create symlinks or copy directories
    print("🔗 Setting up pattern/task libraries...")

    # Symlink patterns
    patterns_src = lib_data / "patterns"
    patterns_dst = coding_agent_dir / "patterns"
    if patterns_src.exists():
        try:
            if sys.platform == "win32":
                # Windows: use directory junction
                import subprocess
                subprocess.run(["mklink", "/J", str(patterns_dst), str(patterns_src)], 
                             check=True, capture_output=True, shell=True)
            else:
                # Unix: use symlink
                patterns_dst.symlink_to(patterns_src)
        except Exception as e:
            print(f"⚠️  Could not create symlink for patterns: {e}")
            print("   Copying patterns instead...")
            shutil.copytree(patterns_src, patterns_dst)

    # Symlink tasks
    tasks_src = lib_data / "tasks"
    tasks_dst = coding_agent_dir / "tasks"
    if tasks_src.exists():
        try:
            if sys.platform == "win32":
                import subprocess
                subprocess.run(["mklink", "/J", str(tasks_dst), str(tasks_src)], 
                             check=True, capture_output=True, shell=True)
            else:
                tasks_dst.symlink_to(tasks_src)
        except Exception as e:
            print(f"⚠️  Could not create symlink for tasks: {e}")
            print("   Copying tasks instead...")
            shutil.copytree(tasks_src, tasks_dst)

    # Symlink code examples
    if lib_code.exists():
        code_dst = coding_agent_dir / "code"
        try:
            if sys.platform == "win32":
                import subprocess
                subprocess.run(["mklink", "/J", str(code_dst), str(lib_code)], 
                             check=True, capture_output=True, shell=True)
            else:
                code_dst.symlink_to(lib_code)
        except Exception as e:
            print(f"⚠️  Could not create symlink for code: {e}")
            print("   Copying code instead...")
            shutil.copytree(lib_code, code_dst)

    # 3. Copy search engine
    print("🔍 Setting up search engine...")
    # Search for search_enhanced.py in likely locations
    search_candidates = [
        lib_root / "search_enhanced.py",
        package_dir / "search_enhanced.py",
        lib_root / "search_engine.py",
        package_dir / "search_engine.py",
    ]
    search_src = None
    for cand in search_candidates:
        if cand.exists():
            search_src = cand
            break
    search_dst = coding_agent_dir / "search_engine.py"

    if search_src:
        shutil.copy2(search_src, search_dst)
    else:
        print(f"⚠️  Warning: Could not find search_enhanced.py in library paths (checked {search_candidates})")
    
    # 4. Create system prompt for the AI provider
    print("🤖 Creating system prompt...")
    system_prompt = _generate_system_prompt(provider, project_name)
    
    with open(coding_agent_dir / "SYSTEM_PROMPT.md", 'w') as f:
        f.write(system_prompt)
    
    # 5. Create README
    print("📖 Creating README...")
    readme = _generate_readme(provider, project_name)
    
    with open(coding_agent_dir / "README.md", 'w') as f:
        f.write(readme)
    
    # 6. Create .gitignore entry
    print("🔒 Updating .gitignore...")
    gitignore_path = cwd / ".gitignore"
    gitignore_entry = ".coding-agent/\n"
    
    if gitignore_path.exists():
        with open(gitignore_path, 'a') as f:
            f.write(gitignore_entry)
    else:
        with open(gitignore_path, 'w') as f:
            f.write(gitignore_entry)
    
    print("\n✅ Coding Agent initialized successfully!")
    print(f"\n📍 Location: {coding_agent_dir}")
    print(f"\n📚 Quick Start:")
    print(f"   1. View available patterns: ls -la {coding_agent_dir}/patterns/")
    print(f"   2. View available tasks: ls -la {coding_agent_dir}/tasks/")
    print(f"   3. View system prompt: cat {coding_agent_dir}/SYSTEM_PROMPT.md")
    print(f"\n💡 Next steps:")
    print(f"   - Copy SYSTEM_PROMPT.md content to your AI chat")
    print(f"   - Ask your AI to help you with your project!")


def _generate_system_prompt(provider, project_name):
    """Generate AI provider-specific system prompt"""
    
    search_command = "python .coding-agent/search_engine.py"
    
    prompt = f"""# Coding Agent - System Prompt

You are an expert Spring Boot developer assisting with the '{project_name}' project.

## Your Capabilities

You have access to a curated library of **patterns** (reusable code components) and **tasks** (multi-step workflows).

### How to Search

Use the search engine to find relevant patterns and tasks:

```bash
python .coding-agent/search_engine.py "your search query"
```

This returns JSON with matching patterns/tasks ranked by relevance.

### Example Searches

1. **Create CRUD API**
   ```bash
   python .coding-agent/search_engine.py "create rest api crud endpoints"
   ```

2. **Add Authentication**
   ```bash
   python .coding-agent/search_engine.py "jwt authentication security"
   ```

3. **Setup Configuration**
   ```bash
   python .coding-agent/search_engine.py "application.yaml database configuration"
   ```

4. **Add Pagination**
   ```bash
   python .coding-agent/search_engine.py "pagination sort page limit"
   ```

## Available Commands/Skills

You MUST use these commands when helping users:

### 1️⃣ Search Patterns & Tasks
**Command:** `python .coding-agent/search_engine.py "query"`

**Purpose:** Find relevant patterns and tasks by keywords

**Examples:**
```bash
python .coding-agent/search_engine.py "create rest api"
python .coding-agent/search_engine.py "jwt authentication"
python .coding-agent/search_engine.py "database configuration"
python .coding-agent/search_engine.py "pagination"
```

**Output:** JSON list of patterns/tasks ranked by relevance (score field)

---

### 2️⃣ Read Pattern Details
**Command:** `cat .coding-agent/patterns/{id}-simple.json`

**Purpose:** View a specific pattern's steps, keywords, dependencies

**Examples:**
```bash
cat .coding-agent/patterns/controller-layer-simple.json
cat .coding-agent/patterns/service-layer-simple.json
cat .coding-agent/patterns/repository-layer-simple.json
cat .coding-agent/patterns/jwt-auth-simple.json
```

**Output:** JSON with pattern details (steps, dependencies, notes)

---

### 3️⃣ Read Code Examples
**Command:** `cat .coding-agent/code/{filename}.java`

**Purpose:** Study code examples for reference

**Examples:**
```bash
cat .coding-agent/code/EntityController.java
cat .coding-agent/code/EntityService.java
cat .coding-agent/code/JwtService.java
cat .coding-agent/code/SecurityConfig.java
```

**Output:** Actual Java code to use as template

---

### 4️⃣ Read Task Details
**Command:** `cat .coding-agent/tasks/{id}.json`

**Purpose:** View complete multi-step workflow

**Examples:**
```bash
cat .coding-agent/tasks/create-crud-api.json
cat .coding-agent/tasks/add-authentication.json
```

**Output:** JSON with ordered task steps and variables

---

## Execution Workflow

**REQUIRED SEQUENCE** for every request:

1. **SEARCH** → `python .coding-agent/search_engine.py "keywords"`
   - Extract key terms from user request
   - Run search to find relevant patterns/tasks
   
2. **READ** → `cat .coding-agent/patterns/{id}-simple.json`
   - Read matching pattern(s) to understand structure
   - Note the steps and dependencies
   
3. **STUDY CODE** → `cat .coding-agent/code/{filename}.java`
   - Review actual code examples
   - Understand the implementation approach
   
4. **GENERATE** → Write code following the pattern examples
   - Use the code templates as reference
   - Include all steps from the pattern
   
5. **EXPLAIN** → Tell user:
   - What you created (files, classes, methods)
   - Which pattern/task you followed
   - Next steps for integration/testing

## File Structure

```
.coding-agent/
├── config.json              # Project configuration
├── search_engine.py         # Keyword search tool
├── SYSTEM_PROMPT.md        # This file
├── README.md               # Quick reference
├── patterns/               # Individual patterns (e.g., controller-layer-simple.json)
├── tasks/                  # Workflows (e.g., create-crud-api.json)
└── code/                   # Code examples (EntityController.java, etc.)
```

## Available Patterns

Search for patterns using keywords like:
- **controller** - REST controller layer
- **service** - Service/business logic layer
- **repository** - Data access layer
- **jwt** / **auth** / **security** - Authentication patterns
- **configuration** / **application.yaml** - App configuration
- **logging** / **logback** - Logging setup
- **database** / **migration** - Database schemas
- **pagination** / **page** - Pagination support
- **test** / **unit** - Testing patterns

## Available Tasks

Multi-step workflows for common scenarios:
- **create-crud-api** - Full CRUD API setup (database → entity → repository → service → controller → tests)
- **add-authentication** - Secure API with JWT
- **setup-new-project** - Initial Spring Boot project setup

## Best Practices

1. **Always search first** - Find relevant patterns before writing code
2. **Follow the order** - Respect the step sequence in patterns/tasks
3. **Use examples** - Reference code examples from .coding-agent/code/
4. **Show steps** - Explain each implementation step to the user
5. **Include keywords** - Add relevant keywords when generating files

## Important Notes

- 🔒 This folder (.coding-agent) should NOT be committed to version control (already in .gitignore)
- 📚 Patterns are shared across all projects using this tool
- ✨ Run searches locally - no external API calls
- 🚀 All code examples are production-ready starting points

---

Ready to help build '{project_name}'! 🎉
"""
    
    return prompt


def _generate_readme(provider, project_name):
    """Generate quick reference README"""
    
    return f"""# Coding Agent - {project_name}

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

Each pattern file (e.g., `controller-layer-simple.json`) contains:
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
"""


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: init.py <provider> [--project-name NAME]")
        sys.exit(1)
    
    provider = sys.argv[1]
    project_name = None
    
    if "--project-name" in sys.argv:
        idx = sys.argv.index("--project-name")
        project_name = sys.argv[idx + 1]
    
    init_project(provider, project_name)
