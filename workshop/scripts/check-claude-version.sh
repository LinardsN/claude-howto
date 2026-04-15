#!/usr/bin/env bash
# Version watcher: detects new Claude Code releases and analyzes workshop impact.
# Called by GitHub Actions on a daily schedule.
# Exits 0 if no update needed, exits 1 if workshop changes proposed.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSHOP_DIR="$(dirname "$SCRIPT_DIR")"
VERSION_FILE="${WORKSHOP_DIR}/.version-tracker"

# Get current installed/known version
if [ -f "$VERSION_FILE" ]; then
    KNOWN_VERSION=$(cat "$VERSION_FILE")
else
    KNOWN_VERSION="0.0.0"
fi

echo "Known Claude Code version: $KNOWN_VERSION"

# Check latest version from npm
LATEST_VERSION=$(npm view @anthropic-ai/claude-code version 2>/dev/null || echo "unknown")

if [ "$LATEST_VERSION" = "unknown" ]; then
    echo "Could not fetch latest version from npm. Skipping."
    exit 0
fi

echo "Latest Claude Code version: $LATEST_VERSION"

# Compare versions
if [ "$KNOWN_VERSION" = "$LATEST_VERSION" ]; then
    echo "No new version. Workshop is up to date."
    exit 0
fi

echo "New version detected: $KNOWN_VERSION -> $LATEST_VERSION"

# Fetch changelog/release notes
CHANGELOG=""
CHANGELOG=$(npm view @anthropic-ai/claude-code --json 2>/dev/null | jq -r '.description // "No description"' || echo "")

# Analyze impact on workshop using Claude Code
echo "Analyzing workshop impact..."

IMPACT_PROMPT="A new version of Claude Code was released: ${LATEST_VERSION} (previous: ${KNOWN_VERSION}).

Release info: ${CHANGELOG}

Our workshop teaches 10 Claude Code features across 10 sessions:
S1: Slash Commands (built-in + custom SKILL.md)
S2: Memory (CLAUDE.md, /init, /memory, .claude/rules/)
S3: Skills (SKILL.md auto-invocation, frontmatter, supporting files)
S4: Subagents (.claude/agents/, tool restrictions, delegation)
S5: MCP (server configuration, .mcp.json, GitHub/Jira integration)
S6: Hooks (PreToolUse, PostToolUse, Stop, settings.json)
S7: Plugins (.claude-plugin/plugin.json, bundling)
S8: Checkpoints (/rewind, Esc+Esc, restore options)
S9: Advanced (planning mode, permission modes, extended thinking)
S10: CLI (print mode -p, JSON output, piping, GitHub Actions)

Analyze: which sessions (if any) need updating due to this release?
Respond ONLY with JSON: {\"impacted\": boolean, \"sessions\": [numbers], \"changes\": [\"description of each change needed\"]}"

IMPACT_RESULT=$(claude -p --output-format json "$IMPACT_PROMPT" 2>/dev/null || echo '{"impacted": false}')

echo "Impact analysis result:"
echo "$IMPACT_RESULT"

# Parse result
IMPACTED=$(echo "$IMPACT_RESULT" | jq -r '.impacted // false' 2>/dev/null || echo "false")

if [ "$IMPACTED" = "true" ] || [ "$IMPACTED" = "True" ]; then
    echo "Workshop updates needed!"

    # Update version tracker
    echo "$LATEST_VERSION" > "$VERSION_FILE"

    # Output for GitHub Actions to create PR
    SESSIONS=$(echo "$IMPACT_RESULT" | jq -r '.sessions | join(", ")' 2>/dev/null || echo "unknown")
    CHANGES=$(echo "$IMPACT_RESULT" | jq -r '.changes | join("\n- ")' 2>/dev/null || echo "unknown")

    echo "::set-output name=impacted::true"
    echo "::set-output name=sessions::${SESSIONS}"
    echo "::set-output name=changes::${CHANGES}"
    echo "::set-output name=new_version::${LATEST_VERSION}"

    exit 1  # Signal that changes are needed
else
    echo "No workshop-impacting changes in this release."
    echo "$LATEST_VERSION" > "$VERSION_FILE"
    exit 0
fi
