# Session 10 Reference: CLI and CI/CD

Quick reference for print mode, piping, output formats, and GitHub Actions
integration. See [10-cli](../../10-cli/README.md) for the full tutorial.

---

## Print Mode (claude -p)

Print mode runs Claude non-interactively: it processes a single prompt,
prints the response, and exits.

### Basic Usage

```bash
# Simple prompt
claude -p "Explain what this project does based on package.json"

# With output format
claude -p "List all API endpoints" --output-format json

# With a specific model
claude -p "Review this code" --model sonnet
```

### Output Formats

| Format | Flag | Output |
|--------|------|--------|
| Text (default) | (none) | Plain text response |
| JSON | `--output-format json` | `{"result": "...", "usage": {...}}` |
| Stream | `--output-format stream-json` | Line-delimited JSON events |

### Useful Flags

| Flag | Description | Example |
|------|-------------|---------|
| `-p "prompt"` | Print mode with inline prompt | `claude -p "summarize"` |
| `--output-format` | Response format | `--output-format json` |
| `--session-id ID` | Resume a specific session | `--session-id abc123` |
| `--continue` | Continue last session | `claude --continue -p "next step"` |
| `--max-turns N` | Limit conversation turns | `--max-turns 1` |
| `--allowedTools` | Restrict available tools | `--allowedTools Read,Grep` |

---

## Piping Content to Claude

Feed file content or command output into Claude via stdin:

```bash
# Review a file
cat src/api/routes/testcases.js | claude -p "Review this API route for security issues"

# Analyze git changes
git diff HEAD~5 | claude -p "Summarize these changes for release notes"

# Process multiple files
find src/api -name "*.js" -exec cat {} \; | claude -p "List all API endpoints with their HTTP methods"

# Chain with jq for structured output
claude -p "List project dependencies" --output-format json | jq '.result'
```

### Piping Patterns

| Pattern | Command | Use Case |
|---------|---------|----------|
| File review | `cat file \| claude -p "review"` | Code review automation |
| Diff analysis | `git diff \| claude -p "summarize"` | Release notes generation |
| Multi-file | `cat *.test.js \| claude -p "find gaps"` | Test coverage analysis |
| Output parsing | `claude -p "..." --output-format json \| jq` | Structured automation |

---

## Batch Processing Scripts

### Template: Review All API Routes

```bash
#!/bin/bash
set -euo pipefail

echo "=== API Route Review ==="
for route_file in src/api/routes/*.js; do
  echo "Reviewing: $route_file"
  cat "$route_file" | claude -p "Review this Express route file. Check for:
    - Missing error handling
    - SQL injection risks
    - Missing input validation
    Report issues as a bullet list." --max-turns 1
  echo "---"
done
```

### Template: Generate Documentation

```bash
#!/bin/bash
set -euo pipefail

# Generate API documentation from source
cat src/api/routes/*.js | claude -p "Generate API documentation in markdown format.
For each endpoint, include: method, path, request body, response format, and status codes.
" --output-format json | jq -r '.result' > docs/api-reference.md

echo "Documentation generated: docs/api-reference.md"
```

### Template: Release Notes

```bash
#!/bin/bash
set -euo pipefail

SINCE_TAG="${1:-$(git describe --tags --abbrev=0 2>/dev/null || echo 'HEAD~20')}"

git log "$SINCE_TAG"..HEAD --oneline | claude -p "Generate release notes from these
git commits. Group changes by category (Features, Bug Fixes, Improvements).
Format as markdown." > RELEASE_NOTES.md

echo "Release notes generated: RELEASE_NOTES.md"
```

---

## GitHub Actions Integration

### Basic CI Workflow

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint-and-build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Lint
        run: npx eslint src/ --max-warnings 0

      - name: Build
        run: npm run build

      - name: Security audit
        run: npm audit --audit-level=moderate
```

### CI with Test Execution

```yaml
  test:
    runs-on: ubuntu-latest
    needs: lint-and-build
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - name: Run tests
        run: npm test -- --coverage
      - name: Upload coverage
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: coverage/
```

### CI with Claude Code Review (Advanced)

```yaml
  code-review:
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Get changed files
        id: changes
        run: |
          echo "files=$(git diff --name-only origin/main...HEAD | tr '\n' ' ')" >> $GITHUB_OUTPUT

      - name: Claude review
        run: |
          for file in ${{ steps.changes.outputs.files }}; do
            echo "Reviewing: $file"
            cat "$file" | claude -p "Brief code review. Focus on bugs and security." --max-turns 1
          done
```

---

## Workflow YAML Validation

### Check Syntax Locally

```bash
# Install actionlint (GitHub Actions linter)
# brew install actionlint   (macOS)
# go install github.com/rhysd/actionlint/cmd/actionlint@latest  (Go)

actionlint .github/workflows/*.yml
```

### Common YAML Pitfalls

| Issue | Problem | Fix |
|-------|---------|-----|
| Indentation | YAML uses spaces, not tabs | Use 2-space indent consistently |
| String quoting | Special chars break unquoted strings | Quote strings with `:`, `{`, `}`, `[`, `]` |
| Multi-line | Long commands need proper syntax | Use `\|` for multi-line blocks |
| Expression syntax | `${{ }}` required for variables | Do not forget the double braces |

---

## Session Management for Automation

```bash
# Start a new named session
claude -p "Initialize QA review" --session-id "qa-batch-review"

# Continue the session
claude --continue --session-id "qa-batch-review" -p "Now review the routes"

# List sessions
claude sessions list

# Resume interactively
claude --continue --session-id "qa-batch-review"
```
