# Claude Code Cheatsheet

Quick reference for all Claude Code features used in the bootcamp.

## Essential Commands

| Command | What It Does |
|---------|-------------|
| `claude` | Start interactive session |
| `claude -p "query"` | Print mode (single query, scriptable) |
| `claude -c` | Continue most recent session |
| `claude -r name` | Resume named session |
| `/help` | Show all commands |
| `/status` | Current session info |
| `/model` | Switch model (opus/sonnet/haiku) |
| `/cost` | Show token usage and cost |
| `/clear` | Clear conversation |
| `Ctrl+C` | Cancel current operation |

## Memory & Standards

| Command | What It Does |
|---------|-------------|
| `/init` | Create CLAUDE.md wizard |
| `/memory` | Add to CLAUDE.md memory |
| `.claude/rules/` | Path-specific rules directory |
| `@import path` | Import rules from another file |

## Skills & Agents

| Command | What It Does |
|---------|-------------|
| `/skill-name` | Invoke a custom skill |
| `/agents` | List available agents |
| `SKILL.md` | Skill definition (in `.claude/skills/`) |
| `.claude/agents/name.md` | Agent definition file |

## MCP (Model Context Protocol)

| Command | What It Does |
|---------|-------------|
| `/mcp` | Show MCP server status |
| `claude mcp add name -- cmd` | Add MCP server |
| `claude mcp list` | List configured servers |
| `claude mcp remove name` | Remove MCP server |
| `.mcp.json` | Project-scoped MCP config |

## Hooks

| Hook Event | When It Fires |
|------------|--------------|
| `PreToolUse` | Before a tool executes |
| `PostToolUse` | After a tool executes |
| `Stop` | When Claude finishes responding |
| `UserPromptSubmit` | When you submit a prompt |

Configuration: `.claude/settings.json`

## Checkpoints

| Action | How |
|--------|-----|
| View checkpoints | Press `Esc` twice |
| Rewind | `/rewind` |
| Restore options | Keep files, revert files, or fork |

## Planning Mode

| Command | What It Does |
|---------|-------------|
| `/plan description` | Start planning (read-only) |
| Review plan | Claude shows proposed steps |
| Approve | Claude executes the plan |
| `Shift+Tab` | Switch permission mode |

## Permission Modes

| Mode | Description |
|------|-------------|
| `plan` | Read-only, no changes |
| `auto` | Auto-approve safe operations |
| `autoEdit` | Auto-approve edits |
| `fullAuto` | Auto-approve everything |

## CLI Automation

```bash
# Pipe content for review
cat file.js | claude -p "review this"

# JSON output
claude -p --output-format json "query"

# Structured output
claude -p --output-format json --json-schema '{"type":"object"}' "query"

# Batch processing
for f in src/*.js; do
  cat "$f" | claude -p "summarize" >> summary.md
done

# Restricted tools
claude --tools "Read,Grep,Glob" -p "audit this"
```

## Plugin Structure

```text
.claude-plugin/
  plugin.json       # Manifest
project/
  commands/          # Slash commands (SKILL.md files)
  agents/            # Agent definitions
  hooks/             # Hook scripts
  mcp/               # MCP configurations
```

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `ANTHROPIC_API_KEY` | API authentication |
| `GITHUB_TOKEN` | GitHub MCP access |
| `CLAUDE_CODE_EFFORT_LEVEL` | low/medium/high/max |

## Bootcamp Commands

```bash
./bootcamp setup --student-id ID    # Student setup
./bootcamp start-session N          # Begin session
./bootcamp complete-session N       # Submit for grading
./bootcamp status                   # Check progress
```
