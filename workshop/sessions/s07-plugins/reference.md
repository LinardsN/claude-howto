# Session 7 Reference: Plugins

Quick reference for plugin manifest format, directory structure, and loading.
See [07-plugins](../../07-plugins/README.md) for the full tutorial.

---

## Plugin Directory Structure

```text
.claude-plugin/
  plugin.json              # Manifest (required)
  README.md                # Plugin documentation (recommended)
  commands/                # Slash command definitions
    new-test-case.md
    bug-report.md
  skills/                  # Skill definitions
    generate-test-suite.md
    qa-review.md
  agents/                  # Agent configurations
    test-writer.md
    bug-triager.md
  hooks/                   # Hook scripts
    validate-filename.sh
    auto-lint.sh
  mcp/                     # MCP server configurations
    servers.json
```

Files can live anywhere in your project -- the manifest references them by
relative path. The above layout is a common convention, not a requirement.

---

## Plugin Manifest (plugin.json)

```json
{
  "name": "qa-toolkit",
  "version": "1.0.0",
  "description": "QA automation toolkit for the TestDevLab Command Center",
  "author": "Your Name",
  "commands": [
    {
      "name": "new-test-case",
      "description": "Create a new test case with ISTQB-standard fields",
      "path": "commands/new-test-case.md"
    }
  ],
  "skills": [
    {
      "name": "generate-test-suite",
      "description": "Generate a test suite for a given feature area",
      "path": "skills/generate-test-suite.md"
    }
  ],
  "agents": [
    {
      "name": "test-writer",
      "description": "Specialized agent for writing test cases from requirements",
      "path": "agents/test-writer.md"
    }
  ],
  "hooks": [
    {
      "event": "PreToolUse:Write",
      "type": "command",
      "command": "hooks/validate-filename.sh",
      "description": "Validates file naming conventions before writes"
    }
  ]
}
```

### Manifest Fields

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `name` | Yes | string | Plugin identifier (kebab-case recommended) |
| `version` | Yes | string | Semantic version (e.g., `1.0.0`) |
| `description` | Yes | string | One-line description of the plugin's purpose |
| `author` | No | string | Plugin author name |
| `commands` | No | array | Slash command definitions |
| `skills` | No | array | Skill file references |
| `agents` | No | array | Agent configuration references |
| `hooks` | No | array | Hook definitions |
| `mcp` | No | array | MCP server configurations |

### Component Reference Fields

Each component in the arrays uses these fields:

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Component identifier |
| `description` | Yes | What this component does |
| `path` | Yes (commands, skills, agents) | Relative path from plugin root to the file |
| `event` | Yes (hooks) | Hook event name (e.g., `PreToolUse:Write`) |
| `type` | Yes (hooks) | Hook type (`command`, `prompt`, `agent`, `http`) |
| `command` | For command hooks | Relative path to the hook script |
| `prompt` | For prompt hooks | The prompt text |

---

## Loading a Plugin

### Via Command Line Flag

```bash
# Load plugin from a directory
claude --plugin-dir .claude-plugin/

# Load plugin from a specific path
claude --plugin-dir /path/to/qa-toolkit/
```

### What Happens on Load

1. Claude reads `plugin.json` from the specified directory
2. Commands are registered as available slash commands
3. Skills become available for invocation
4. Agent definitions are loaded for delegation
5. Hooks are registered in the hook event system
6. MCP configurations are merged with existing settings

---

## Distribution Patterns

### Copy to Another Project

```bash
# Package as tarball
tar -czf qa-toolkit-v1.0.0.tar.gz .claude-plugin/

# Extract in target project
tar -xzf qa-toolkit-v1.0.0.tar.gz
claude --plugin-dir .claude-plugin/
```

### Git Submodule

```bash
# Add as submodule in another project
git submodule add https://github.com/org/qa-toolkit.git .claude-plugin
claude --plugin-dir .claude-plugin/
```

### npm Package

```bash
# If published to npm
npm install @org/qa-toolkit
claude --plugin-dir node_modules/@org/qa-toolkit/
```

---

## Validating Your Plugin

### Check Manifest JSON

```bash
# Verify valid JSON
cat .claude-plugin/plugin.json | jq .

# Pretty-print with validation
python3 -c "import json; json.load(open('.claude-plugin/plugin.json'))"
```

### Verify Referenced Files Exist

```bash
# Extract all paths from manifest and check each one
jq -r '
  (.commands // [] | .[].path),
  (.skills // [] | .[].path),
  (.agents // [] | .[].path),
  (.hooks // [] | select(.command) | .[].command)
' .claude-plugin/plugin.json | while read path; do
  if [ -f ".claude-plugin/$path" ]; then
    echo "OK: $path"
  else
    echo "MISSING: $path"
  fi
done
```

---

## Progressive Dependency Map

Your plugin should bundle artifacts from these sessions:

```text
Session 1 (Slash Commands)  ──>  plugin.json "commands" section
Session 3 (Skills)          ──>  plugin.json "skills" section
Session 4 (Agents)          ──>  plugin.json "agents" section
Session 6 (Hooks)           ──>  plugin.json "hooks" section
```

Minimum requirement: S3 + S4 + S6 (three sessions).
Full marks: S1 + S3 + S4 + S6 (four sessions).
