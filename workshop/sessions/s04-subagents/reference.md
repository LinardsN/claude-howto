# Session 4 Reference: Subagents

Quick reference for subagents in Claude Code. For the full guide, see [04-subagents/README.md](../../04-subagents/README.md).

## Agent File Location

```text
.claude/agents/
  test-writer.md
  bug-triager.md
  security-scanner.md
```

## YAML Frontmatter

```yaml
---
description: What the agent does (shown in /agents list)
tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
model: sonnet
permissionMode: default
---
```

| Field | Required | Values |
|-------|----------|--------|
| `description` | Yes | Natural language description |
| `tools` | No | List of allowed tools (default: all) |
| `model` | No | `sonnet`, `opus`, `haiku` |
| `permissionMode` | No | `default`, `permissive`, `strict` |

## Available Tools

| Tool | Capability |
|------|-----------|
| `Read` | Read file contents |
| `Write` | Create or overwrite files |
| `Edit` | Modify existing files (find/replace) |
| `Bash` | Execute shell commands |
| `Grep` | Search file contents (regex) |
| `Glob` | Find files by pattern |

## Common Tool Restriction Patterns

| Pattern | Tools | Use Case |
|---------|-------|----------|
| **Full access** | All tools | Test writer, code generator |
| **Read-only** | `Read`, `Grep`, `Glob` | Security scanner, auditor |
| **Read + execute** | `Read`, `Grep`, `Glob`, `Bash` | Test runner, analyzer |
| **No execute** | `Read`, `Write`, `Edit`, `Grep`, `Glob` | Writer without shell |

## Managing Agents

| Action | Method |
|--------|--------|
| List agents | `/agents` in REPL |
| Create agent | Add `.md` file to `.claude/agents/` |
| Edit agent | Modify the `.md` file |
| Delete agent | Remove the `.md` file |
| Use agent | Ask Claude to delegate, or use `/agents` |

## Agent vs Skill

| Aspect | Skill (SKILL.md) | Agent (.md in agents/) |
|--------|-------------------|------------------------|
| Location | `.claude/skills/` | `.claude/agents/` |
| Context | Shares main context (unless `fork`) | Always isolated context |
| Tools | Inherits main tools | Can be restricted |
| Purpose | Reusable workflow | Specialized persona |
| Invocation | Slash command or auto-invoke | Delegation via `/agents` |

## Agent Body (System Prompt)

The markdown body below the frontmatter is the agent's system prompt. Include:

- Role and expertise description
- Specific constraints and rules
- Output format expectations
- References to project standards (CLAUDE.md)
- References to skills the agent should use

## Tips

- Restrict tools to the minimum needed -- principle of least privilege
- Write substantive system prompts (10+ lines) for better agent behavior
- Reference CLAUDE.md standards in the agent's system prompt
- Agents can invoke skills; mention skill names in the agent's instructions
- Use `model: haiku` for simple agents to save tokens; `opus` for complex analysis
