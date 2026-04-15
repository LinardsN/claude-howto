# Session 2 Reference: Memory

Quick reference for the Claude Code memory system. For the full guide, see [02-memory/README.md](../../02-memory/README.md).

## Memory Hierarchy

| Level | Source | Scope | Override |
|-------|--------|-------|----------|
| 1 | Enterprise policy | Organization | Lowest priority |
| 2 | `~/.claude/CLAUDE.md` | All projects | Personal prefs |
| 3 | `./CLAUDE.md` | Project root | Team standards |
| 4 | `.claude/rules/*.md` | Path-specific | Targeted rules |
| 5 | `@import` references | Imported docs | Referenced content |
| 6 | `/init` output | Auto-detected | Bootstrap info |
| 7 | `/memory` additions | Session-level | Highest priority |

Later levels override earlier ones when instructions conflict.

## Key Commands

| Command | Purpose | Usage |
|---------|---------|-------|
| `/init` | Bootstrap CLAUDE.md from project analysis | Run once at project start |
| `/memory` | Open CLAUDE.md in your editor | Edit standards anytime |
| `@path` | Import file content into memory | `@docs/api-spec.md` |

### Enhanced `/init`

Set `CLAUDE_CODE_NEW_INIT=1` for the interactive multi-step flow:

```bash
CLAUDE_CODE_NEW_INIT=1 claude
/init
```

## CLAUDE.md Structure

A well-structured CLAUDE.md typically contains:

```markdown
# Project Name

## Tech Stack
- Backend: Express.js
- Frontend: React (Vite)
- Database: SQLite

## Conventions
### Naming
- API routes: /api/resource-name (kebab-case)
- Route handlers: handleVerbNoun (camelCase)
- React components: PascalCase

### API Response Format
All endpoints return: { success: boolean, data: T | null, error: string | null }

### Data Models
[Define fields, types, valid values]

## QA Standards
### Severity Levels
- Critical, Major, Minor, Trivial

### Test Case Fields
[Required fields for every test case]
```

## Rules Directory

```text
.claude/
  rules/
    server.md      # Applied when working in server/
    client.md      # Applied when working in client/
    tests.md       # Applied when working on test files
```

Rules files are plain markdown. They are loaded when Claude works on files matching the path context.

## @import Syntax

Reference external files from within CLAUDE.md:

```markdown
## API Documentation
@docs/api-reference.md

## Style Guide
@docs/style-guide.md
```

The imported file's content becomes part of Claude's context when the memory is loaded.

## Tips

- Be prescriptive, not descriptive: "Use `handleCreateTestCase`" beats "use good naming"
- Define your data model in CLAUDE.md -- Claude will use exactly those fields
- Standards defined in memory apply to ALL future conversations, not just the current one
- Path-specific rules prevent server conventions from bleeding into client code
- After defining standards, test them by asking Claude to generate code and checking compliance
