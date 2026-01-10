# Provider-Specific Prompt Locations

When you run `coding-agent init <provider>`, the system prompt is placed in the correct location for each AI provider to auto-discover.

## File Locations

### GitHub Copilot
```bash
coding-agent init copilot
```

Creates:
- `.github/prompts/coding-agent.prompt.md` ← Copilot auto-discovers this
- `.coding-agent/` (patterns, tasks, code, search engine)

### Claude Projects
```bash
coding-agent init claude
```

Creates:
- `.claude/skills/coding-agent/SKILL.md` ← Claude auto-discovers this
- `.coding-agent/` (patterns, tasks, code, search engine)

### GPT (Generic)
```bash
coding-agent init gpt
```

Creates:
- `.gpt/prompts/coding-agent.md` ← Generic location
- `.coding-agent/` (patterns, tasks, code, search engine)

## What Gets Committed

✅ **Commit these:**
- `.github/prompts/` (for Copilot)
- `.claude/skills/` (for Claude)
- `.gpt/prompts/` (for GPT)
- `.gitignore` (updated)

❌ **Don't commit:**
- `.coding-agent/` (added to .gitignore automatically)

## Error Handling

If you try to initialize when files already exist:

```bash
$ coding-agent init claude
❌ Error: .claude/skills/coding-agent/SKILL.md already exists!
   If you want to reinitialize, delete it first: rm .claude/skills/coding-agent/SKILL.md
```

Or if `.coding-agent/` exists:

```bash
$ coding-agent init copilot
❌ Error: .coding-agent already exists!
   If you want to reinitialize, delete it first: rm -rf .coding-agent
```

## Project Structure After Init

```
your-project/
├── .github/
│   └── prompts/
│       └── coding-agent.prompt.md    ← Copilot discovers this
│
├── .claude/
│   └── skills/
│       └── coding-agent/
│           └── SKILL.md               ← Claude discovers this
│
├── .coding-agent/                     ← In .gitignore
│   ├── patterns/                      ← Symlinked to library
│   ├── tasks/                         ← Symlinked to library
│   ├── code/                          ← Symlinked to library
│   ├── search_engine.py               ← Copied from library
│   ├── README.md
│   └── config.json
│
└── .gitignore                         ← Updated
```

## Benefits

1. **Auto-discovery** - AI providers find prompts automatically
2. **No manual copying** - Prompts in standard locations
3. **Version control friendly** - Prompts are committed, data is not
4. **Team consistency** - Everyone gets the same setup
5. **Provider-specific** - Respects each AI's conventions
