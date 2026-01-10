# Keyword-Based Search System Design

## Concept
Each pattern/task has keywords → User prompt gets broken down → Search by keywords → Feed matching files to AI → AI decides what to use

## Example Flow

### User Prompt:
"Help me create api /api/products/search with pagination"

### Step 1: Extract Keywords
```
Extracted: ["create", "api", "products", "search", "pagination", "rest", "endpoint"]
```

### Step 2: Search Patterns by Keywords
```
Matches:
- controller-layer-simple.json     (keywords: controller, rest, api, endpoint)
- service-layer-simple.json        (keywords: service, business-logic)
- repository-layer-simple.json     (keywords: repository, data-access)
- pagination-pattern.json          (keywords: pagination, page, sort)

Matches:
- create-crud-api.json             (keywords: create, api, crud, rest)
```

### Step 3: Feed to AI
```
Context:
- 4 pattern files
- 1 task file
- Code examples from code/ folder

AI Prompt:
"User wants: 'create api /api/products/search with pagination'
Here are relevant patterns and tasks. Decide which to use and in what order."
```

### Step 4: AI Decides
```
AI Response:
"I'll use:
1. repository-layer (with pagination)
2. service-layer (search logic)
3. controller-layer (expose endpoint)

Not using: create-crud-api task (too broad, user wants one endpoint)"
```

## Implementation

### 1. Add keywords to each file

**Pattern Example:**
```json
{
  "id": "controller-layer",
  "name": "REST Controller Layer",
  "keywords": ["controller", "rest", "api", "endpoint", "http", "request", "response"],
  "description": "...",
  "steps": [...]
}
```

**Task Example:**
```json
{
  "id": "create-crud-api",
  "name": "Create CRUD REST API",
  "keywords": ["create", "crud", "api", "rest", "full-stack", "endpoint", "database"],
  "description": "...",
  "tasks": [...]
}
```

### 2. Keyword Extraction from Prompt

```python
def extract_keywords(prompt):
    # Technical keywords
    keywords = []
    
    # HTTP methods
    keywords.extend(re.findall(r'\b(GET|POST|PUT|DELETE|PATCH)\b', prompt))
    
    # Entities (after /api/)
    entity_match = re.search(r'/api/(\w+)', prompt)
    if entity_match:
        keywords.append(entity_match.group(1))
    
    # Common patterns
    patterns = {
        'crud': ['crud', 'create.*api', 'full.*endpoint'],
        'authentication': ['auth', 'jwt', 'login', 'secure', 'token'],
        'pagination': ['pagina', 'page', 'sort'],
        'validation': ['validat', 'constraint'],
        'search': ['search', 'filter', 'query'],
        'controller': ['controller', 'endpoint', 'rest'],
        'service': ['service', 'business', 'logic'],
        'repository': ['repository', 'database', 'dao']
    }
    
    for key, patterns_list in patterns.items():
        if any(re.search(p, prompt.lower()) for p in patterns_list):
            keywords.append(key)
    
    return keywords
```

### 3. Search & Rank

```python
def search_by_keywords(keywords):
    results = []
    
    for file in all_json_files:
        data = json.load(file)
        file_keywords = data.get('keywords', [])
        
        # Calculate match score
        matches = len(set(keywords) & set(file_keywords))
        
        if matches > 0:
            results.append({
                'file': file,
                'data': data,
                'score': matches,
                'type': 'pattern' if 'patterns/' in file else 'task'
            })
    
    # Sort by score
    results.sort(key=lambda x: x['score'], reverse=True)
    
    return results[:5]  # Top 5 matches
```

### 4. AI System Prompt

```
You are a Spring Boot coding assistant with access to pattern and task libraries.

User Request: "Help me create api /api/products/search with pagination"

Relevant Patterns Found:
1. [controller-layer-simple.json] - REST Controller Layer (score: 3)
2. [service-layer-simple.json] - Service Layer Pattern (score: 2)  
3. [pagination-pattern.json] - Add Pagination Support (score: 2)

Relevant Tasks Found:
1. [create-crud-api.json] - Create CRUD REST API (score: 2)

Your job:
1. Decide if this is a full workflow (use task) or custom combination (use patterns)
2. Select which patterns/tasks to use
3. Determine the order of execution
4. Generate code based on the pattern examples

Respond with your plan, then generate the code.
```

## Benefits

✅ **No pre-defined intent mapping** - Keywords are flexible
✅ **Works for variations** - "create api", "add endpoint", "build rest service" all work
✅ **AI makes final decision** - Handles edge cases naturally
✅ **Easy to extend** - Just add keywords to new patterns
✅ **Fuzzy matching** - Partial keyword matches still work

## Potential Issues

⚠️ **Keyword quality matters** - Need good keywords for each file
⚠️ **False positives** - "create" might match too many things
⚠️ **No semantic understanding** - "JWT authentication" vs "login" needs synonyms

## Solution: Enhanced Keywords

Add **synonyms** and **categories**:

```json
{
  "id": "jwt-authentication",
  "keywords": {
    "primary": ["jwt", "authentication", "token"],
    "synonyms": ["auth", "login", "secure", "bearer", "security"],
    "categories": ["security", "authentication"],
    "triggers": ["protect", "secure", "authenticate"]
  }
}
```

## Verdict

**Yes, this is very possible and actually simpler than intent detection!**

The AI becomes the "orchestrator" naturally, and you just need:
1. Good keywords on each file (one-time effort)
2. Simple keyword extraction from prompt
3. BM25-like search (already have this!)
4. Feed results to AI with good system prompt
