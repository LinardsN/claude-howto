# Session 3 Reference: Skills

Quick reference for Agent Skills in Claude Code. For the full guide, see [03-skills/README.md](../../03-skills/README.md).

## SKILL.md File Structure

```text
.claude/skills/
  skill-name/
    SKILL.md            # Required: frontmatter + instructions
    templates/           # Optional: template files
    scripts/             # Optional: automation scripts
    docs/                # Optional: reference documentation
```

## YAML Frontmatter

```yaml
---
name: generate-test-suite
description: Generate a comprehensive test suite using ISTQB test design techniques
version: 1.0.0
---
```

| Field | Required | Purpose |
|-------|----------|---------|
| `name` | Yes | Slash command name (e.g., `/generate-test-suite`) |
| `description` | Yes | Auto-invocation matching; natural language trigger |
| `version` | No | Semantic version |
| `context` | No | Set to `fork` for isolated execution |

## Progressive Disclosure Levels

| Level | When Loaded | Cost | Contains |
|-------|------------|------|----------|
| 1 - Metadata | Always | ~100 tokens | `name` + `description` |
| 2 - Instructions | On trigger | < 5k tokens | SKILL.md body |
| 3 - Resources | As needed | Unlimited | Bundled files |

## Auto-Invocation

The `description` field drives auto-invocation. Claude matches your natural language to skill descriptions:

- **Good**: "Generate a comprehensive test suite using ISTQB test design techniques including boundary value analysis and equivalence partitioning"
- **Bad**: "Test suite skill"

Write descriptions containing keywords users would naturally say when requesting that capability.

## Context: Fork

Runs the skill in an isolated context window:

```yaml
---
name: qa-review
description: Review code from a QA perspective
context: fork
---
```

Use `context: fork` when:

- The skill produces lengthy output that would consume main context
- The skill reads many files for analysis
- You want to prevent context pollution in the main conversation

## Invocation Methods

| Method | Example |
|--------|---------|
| Slash command | `/generate-test-suite` |
| Natural language | "I need a test suite for authentication" |
| Agent delegation | Another agent references this skill |

## Supporting Files

Reference supporting files from the SKILL.md body:

```markdown
## Templates
Use the template in `templates/test-suite-template.md` as the output structure.

## Scripts
Run `scripts/analyze-endpoints.sh` to discover available API endpoints.
```

Claude reads these files on demand (Level 3) without consuming context until needed.

## Tips

- One skill per QA workflow -- keep skills focused on a single task
- Description quality directly affects auto-invocation accuracy
- Supporting templates produce more consistent output than instructions alone
- Skills from `.claude/commands/` also work; `.claude/skills/` takes precedence if both exist
- Test auto-invocation by using natural language instead of the slash command
