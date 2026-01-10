# Coding Agent CLI - Project Structure

## Installation & Usage

```bash
# Install the package
pip install coding-agent

# Initialize in your project
cd supermarket
coding-agent init claude

# This creates:
supermarket/
├── .coding-agent/
│   ├── config.json          # Project metadata
│   ├── search_engine.py     # Keyword search tool
│   ├── patterns/            # Symlink to library patterns
│   ├── tasks/               # Symlink to library tasks
│   ├── code/                # Symlink to library code examples
│   ├── .system-prompt.md    # Instructions for Claude
│   └── README.md            # Quick reference guide
```

## How It Works

### 1. User runs init
```bash
coding-agent init claude
```

### 2. Generated `.coding-agent/.system-prompt.md`
Contains instructions for Claude about:
- How to use the search engine
- Available patterns and tasks
- Code examples location
- Best practices

### 3. Claude receives context in prompt
```
You have access to a coding pattern library with search capabilities.

To find relevant patterns/tasks, use:
  python .coding-agent/search_engine.py "your search query"

This returns JSON with top matching patterns and tasks.
Then generate code based on the examples in .coding-agent/code/
```

### 4. Claude's workflow
1. User: "Help me create api /api/products"
2. Claude runs: `python .coding-agent/search_engine.py "create api /api/products"`
3. Claude gets: `[{id: "controller-layer", keywords: [...], file_path: "..."}, ...]`
4. Claude reads actual code examples from `.coding-agent/code/`
5. Claude generates code and explains steps

## Project Structure

```
coding-agent/  (this repo)
├── coding_agent/
│   ├── __init__.py
│   ├── cli.py                 # CLI commands
│   ├── init.py                # Initialization logic
│   ├── search_engine.py       # Enhanced search (will be copied)
│   └── templates/
│       ├── system-prompt.md   # Template for Claude instructions
│       └── config.json        # Template for project config
│
├── data/
│   ├── patterns/              # Pattern library
│   ├── tasks/                 # Task library
│   ├── code/                  # Code examples
│   └── configuration/         # Config examples
│
└── setup.py                   # Package installer
```

## Files Generated in .coding-agent

### 1. config.json
```json
{
  "project_name": "supermarket",
  "ai_provider": "claude",
  "patterns_path": ".coding-agent/patterns",
  "tasks_path": ".coding-agent/tasks",
  "code_path": ".coding-agent/code",
  "config_path": ".coding-agent/configuration"
}
```

### 2. .system-prompt.md
```markdown
# Coding Agent System Prompt

You are a Spring Boot development assistant with access to a coding pattern library.

## Available Skills

### Search Patterns and Tasks
Run: python .coding-agent/search_engine.py "your query"

Examples:
- "create api /api/products/search"
- "add JWT authentication" 
- "setup database migration"

## Available Patterns
See: ls -la .coding-agent/patterns/

## Code Examples
See: ls -la .coding-agent/code/

## Workflow
1. User describes what they need
2. You search for relevant patterns/tasks
3. You examine the matched patterns
4. You generate code based on examples
5. You explain the implementation steps
```

### 3. search_engine.py
Copy of enhanced search with:
- Keyword extraction from queries
- BM25 scoring
- JSON output for Claude to parse

### 4. Symlinks to library
- `.coding-agent/patterns/ → <library>/data/patterns/`
- `.coding-agent/tasks/ → <library>/data/tasks/`
- `.coding-agent/code/ → <library>/code/`

## Commands for Claude

### Search Patterns
```bash
python .coding-agent/search_engine.py "create rest api endpoint"
```

Output:
```json
[
  {
    "id": "controller-layer",
    "name": "REST Controller Layer",
    "keywords": ["controller", "rest", "api", ...],
    "file_path": "patterns/controller-layer-simple.json",
    "score": 4.5
  },
  ...
]
```

### View Pattern Details
```bash
cat .coding-agent/patterns/controller-layer-simple.json
```

### View Code Example
```bash
cat .coding-agent/code/EntityController.java
```

## Usage Examples

### User Prompt 1: Create CRUD API
```
User: "Help me create a CRUD API for products with GET, POST, PUT, DELETE endpoints"

Claude: 
1. Searches: python .coding-agent/search_engine.py "create crud api rest endpoints"
2. Gets: [create-crud-api task, controller-layer pattern, service-layer pattern]
3. Reads: .coding-agent/code/EntityController.java and related files
4. Generates: ProductEntity, ProductRepository, ProductService, ProductController
5. Explains: Complete step-by-step implementation
```

### User Prompt 2: Add Authentication
```
User: "Secure my API with JWT authentication"

Claude:
1. Searches: python .coding-agent/search_engine.py "jwt authentication secure api"
2. Gets: [jwt-authentication pattern, add-jwt-authentication task]
3. Reads: Code examples
4. Generates: JwtService, JwtFilter, SecurityConfig
5. Explains: Integration with existing controllers
```

### User Prompt 3: Setup Project
```
User: "Set up a new Spring Boot project with logging and database"

Claude:
1. Searches: python .coding-agent/search_engine.py "setup project configuration logging"
2. Gets: [application-yaml pattern, logging-config pattern]
3. Reads: Config examples
4. Generates: application.yaml with database and logging setup
```

## Why This Architecture

✅ **Reusable** - Install once, use in multiple projects
✅ **Isolated** - Each project has its own .coding-agent folder
✅ **No re-prompting** - Claude can search and read without asking you
✅ **Predictable** - Same library across all projects
✅ **Version control safe** - .coding-agent in .gitignore
✅ **AI-native** - Search outputs JSON for easy parsing

## Implementation Path

1. Create Python package structure
2. Implement `cli.py` with `init` command
3. Implement `init.py` to generate .coding-agent folder
4. Copy `search_engine.py` template
5. Create system prompt template
6. Test with sample project
