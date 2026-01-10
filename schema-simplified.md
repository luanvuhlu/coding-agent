# Simplified Schema Design

## 1. Pattern Schema (Individual Skills)
Minimal metadata, code references only.

```json
{
  "id": "service-layer",
  "name": "Service Layer Pattern",
  "description": "Business logic layer between controller and repository",
  "complexity": "low",
  
  "dependencies": [
    "spring-boot-starter-data-jpa"
  ],
  
  "steps": [
    {
      "title": "Create Service Class",
      "files": ["code/EntityService.java"]
    },
    {
      "title": "Inject in Controller",
      "files": ["code/EntityController.java"]
    }
  ],
  
  "notes": [
    "Keep business logic in service layer",
    "Use @Transactional for data operations"
  ]
}
```

## 2. Task Schema (Multi-Step Workflows)
Orchestrates multiple patterns into complete workflows.

```json
{
  "id": "create-crud-api",
  "name": "Create CRUD REST API",
  "description": "End-to-end API creation from database to controller",
  
  "tasks": [
    {
      "step": 1,
      "name": "Database Schema",
      "pattern": "liquibase-migration",
      "params": {
        "table": "{{entity_name}}",
        "columns": "{{columns}}"
      }
    },
    {
      "step": 2,
      "name": "Create Entity",
      "pattern": "jpa-entity",
      "params": {
        "entity": "{{entity_name}}",
        "fields": "{{columns}}"
      }
    },
    {
      "step": 3,
      "name": "Create Repository",
      "pattern": "repository-layer",
      "params": {
        "entity": "{{entity_name}}"
      }
    },
    {
      "step": 4,
      "name": "Create Service",
      "pattern": "service-layer",
      "params": {
        "entity": "{{entity_name}}"
      }
    },
    {
      "step": 5,
      "name": "Create Controller",
      "pattern": "rest-controller",
      "params": {
        "entity": "{{entity_name}}",
        "endpoints": ["GET", "POST", "PUT", "DELETE"]
      }
    },
    {
      "step": 6,
      "name": "Add Tests",
      "pattern": "controller-test",
      "params": {
        "entity": "{{entity_name}}"
      }
    }
  ],
  
  "variables": {
    "entity_name": "User",
    "columns": ["username:string", "email:string", "active:boolean"]
  }
}
```

## 3. Folder Structure

```
data/
├── patterns/          # Individual reusable skills
│   ├── jpa-entity.json
│   ├── repository-layer.json
│   ├── service-layer.json
│   ├── rest-controller.json
│   └── liquibase-migration.json
│
├── tasks/             # Multi-step workflows
│   ├── create-crud-api.json
│   ├── add-authentication.json
│   ├── setup-new-project.json
│   └── add-pagination.json
│
└── templates/         # Code templates (referenced by patterns)
    └── (referenced in pattern files)
```

## 4. Benefits

**Patterns (Skills):**
- Minimal redundancy
- Single responsibility
- Easy to maintain
- Composable

**Tasks (Workflows):**
- Define complete user journeys
- Parameterized for reuse
- Shows dependency order
- Template variable support

**What gets removed:**
- ❌ Framework field (infer from folder)
- ❌ Category/subcategory (infer from folder)
- ❌ Verbose architecture diagrams
- ❌ Keywords (generated from search)
- ❌ Prerequisites/related (separate graph)
- ❌ Redundant "type: file" markers
