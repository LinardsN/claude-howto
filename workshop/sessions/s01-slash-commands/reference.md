# Session 1 Reference: Slash Commands

Quick reference for slash commands in Claude Code. For the full guide, see [01-slash-commands/README.md](../../01-slash-commands/README.md).

## Essential Built-in Commands

| Command | Purpose |
|---------|---------|
| `/help` | Show all available commands |
| `/status` | Version, model, account info |
| `/model [name]` | Switch model; use left/right arrows for effort |
| `/cost` | Token usage and cost for current session |
| `/compact [focus]` | Compress conversation; optional focus area |
| `/clear` | Clear conversation history (aliases: `/reset`, `/new`) |
| `/init` | Initialize CLAUDE.md (used in Session 2) |
| `/skills` | List all available skills |
| `/agents` | List available agents (used in Session 4) |
| `/diff` | Interactive diff viewer for uncommitted changes |
| `/context` | Visualize context usage as a colored grid |

## SKILL.md File Format

Skills live in `.claude/skills/` as directories with a `SKILL.md` file:

```text
.claude/
  skills/
    new-test-case/
      SKILL.md          # Required: frontmatter + instructions
      templates/         # Optional: supporting files
    bug-report/
      SKILL.md
```

### YAML Frontmatter

```yaml
---
name: new-test-case
description: Generate a structured QA test case with ISTQB fields
---
```

| Field | Required | Purpose |
|-------|----------|---------|
| `name` | Yes | Becomes the `/command-name` in REPL |
| `description` | Yes | Enables auto-invocation; Claude matches natural language to this |
| `version` | No | Semantic version for the skill |

### SKILL.md Body

The body contains markdown instructions that Claude follows when the skill is invoked. Include:

- What the skill should produce
- Required fields or structure
- Constraints and rules
- Output format expectations

## Invocation Methods

| Method | Example |
|--------|---------|
| **Slash command** | Type `/new-test-case` in the REPL |
| **Auto-invocation** | Say "I need a test case for login" -- Claude matches the description |
| **Explicit reference** | Mention the skill name in your prompt |

## Key CLI Flags

| Flag | Purpose |
|------|---------|
| `claude` | Start interactive REPL |
| `claude -p "prompt"` | Non-interactive single prompt |
| `claude --version` | Show installed version |
| `claude --help` | Full CLI help |
| `claude -m model` | Start with a specific model |

## Legacy: Commands Directory

Files in `.claude/commands/` still work as slash commands. The skill format (`.claude/skills/`) is the recommended approach. If both exist at the same path, the skill takes precedence.

## Tips

- Type `/` and start typing to filter the command list
- Use `/cost` periodically to monitor your token usage
- `/compact` is your friend when conversations get long -- it summarizes context to free space
- The `description` field is critical for auto-invocation; write it as a natural language sentence describing when the skill should activate
