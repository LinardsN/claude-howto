# Session 6 Reference: Hooks

Quick reference for hook events, configuration format, and JSON protocol.
See [06-hooks](../../06-hooks/README.md) for the full tutorial.

---

## Hook Events

| Event | When It Fires | Common Use |
|-------|---------------|------------|
| `PreToolUse` | Before Claude calls any tool | Validate inputs, block dangerous operations |
| `PreToolUse:Write` | Before Claude writes a file | File naming validation, path restrictions |
| `PreToolUse:Bash` | Before Claude runs a shell command | Command allowlisting, security checks |
| `PostToolUse` | After any tool call completes | Logging, post-processing |
| `PostToolUse:Write` | After a file is written | Auto-lint, auto-format, notifications |
| `PostToolUse:Bash` | After a shell command runs | Output validation, audit logging |
| `Notification` | When Claude produces a notification | Alerting, external integrations |
| `Stop` | When Claude finishes a response turn | Coverage reminders, summary prompts |
| `UserPromptSubmit` | When the user submits a prompt | Prompt logging, analytics |

**Tool-specific events** use the `Event:ToolName` syntax. You can match
specific tools (`:Write`, `:Bash`, `:Read`) or use the bare event name to
match all tools.

---

## settings.json Format

Hooks are configured in `.claude/settings.json` (project-level) or
`~/.claude/settings.json` (global):

```json
{
  "hooks": {
    "PreToolUse:Write": [
      {
        "type": "command",
        "command": ".claude/hooks/validate-filename.sh"
      }
    ],
    "PostToolUse:Write": [
      {
        "type": "command",
        "command": ".claude/hooks/auto-lint.sh"
      }
    ],
    "Stop": [
      {
        "type": "prompt",
        "prompt": "Check if any new code written in this turn has corresponding unit tests. If not, mention what tests are missing."
      }
    ]
  }
}
```

### Hook Definition Fields

| Field | Required | Description |
|-------|----------|-------------|
| `type` | Yes | One of: `command`, `prompt`, `agent`, `http` |
| `command` | For `command` type | Shell command or script path to execute |
| `prompt` | For `prompt` type | Natural language instruction for Claude |
| `timeout` | No | Max execution time in milliseconds (default: 10000) |
| `matcher` | No | Regex to further filter which tool invocations trigger the hook |

---

## JSON I/O Protocol (Command Hooks)

### Input (stdin)

Command hooks receive a JSON object on stdin with context about the event:

```json
{
  "event": "PreToolUse:Write",
  "tool": "Write",
  "params": {
    "file_path": "/path/to/project/src/components/TestCaseList.jsx",
    "content": "..."
  },
  "session_id": "abc123"
}
```

### Output (stdout)

Command hooks can return JSON on stdout to communicate back:

```json
{
  "action": "block",
  "message": "Filename 'TestCaseList.jsx' violates naming convention. React components must use PascalCase with .tsx extension."
}
```

For PostToolUse hooks, the output is informational (displayed to the user
but does not block anything).

---

## Exit Codes

| Code | Meaning | Effect |
|------|---------|--------|
| `0` | Success / Allow | Operation proceeds normally |
| `2` | Block (PreToolUse only) | Operation is prevented; message shown to user |
| `1` | Error | Hook failed; operation proceeds but error is logged |
| Other | Error | Treated same as exit code 1 |

**Important**: Only PreToolUse hooks can block operations (exit code 2).
PostToolUse and Stop hooks are informational -- their exit codes indicate
success or failure of the hook itself, not whether to block anything.

---

## Hook Types Comparison

| Type | Runs As | Best For | Example |
|------|---------|----------|---------|
| **command** | Shell script/command | File validation, linting, external tools | `bash .claude/hooks/lint.sh` |
| **prompt** | Claude instruction | Reminders, analysis, summaries | "Check test coverage" |
| **agent** | Sub-agent task | Complex analysis requiring AI | "Review this code for security issues" |
| **http** | HTTP request | Webhooks, external notifications | `POST https://hooks.slack.com/...` |

---

## Common Patterns

### Extract Filename from JSON Input (Bash)

```bash
#!/bin/bash
set -euo pipefail

# Read JSON from stdin
INPUT=$(cat)

# Extract file path using jq
FILE_PATH=$(echo "$INPUT" | jq -r '.params.file_path // empty')

if [ -z "$FILE_PATH" ]; then
  exit 0  # No file path, allow
fi

FILENAME=$(basename "$FILE_PATH")
```

### Conditional Blocking

```bash
# Check naming convention
if [[ "$FILENAME" =~ ^[a-z][a-z0-9-]*\.[a-z]+$ ]]; then
  exit 0  # Matches kebab-case, allow
else
  echo '{"action":"block","message":"Filename must be kebab-case"}'
  exit 2  # Block the write
fi
```

### PostToolUse Lint Runner

```bash
#!/bin/bash
set -euo pipefail

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.params.file_path // empty')

# Only lint JS/TS files
if [[ "$FILE_PATH" =~ \.(js|jsx|ts|tsx)$ ]]; then
  npx eslint --fix "$FILE_PATH" 2>&1 || true
fi

exit 0
```

---

## Debugging Hooks

- **Test manually**: `echo '{"event":"PreToolUse:Write","params":{"file_path":"test.js"}}' | bash .claude/hooks/validate-filename.sh; echo "Exit: $?"`
- **Check settings**: Verify `.claude/settings.json` is valid JSON (`cat .claude/settings.json | jq .`)
- **Watch for timeouts**: Hooks that exceed the timeout are killed and treated as errors
- **Stderr for logging**: Write debug info to stderr; only stdout is parsed as hook output
