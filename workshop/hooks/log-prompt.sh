#!/usr/bin/env bash
# UserPromptSubmit hook: logs every student prompt to JSONL file.
# Receives JSON on stdin with user_prompt field.
# MUST exit 0 always — never block student work.
set -uo pipefail

BOOTCAMP_HOME="${HOME}/.claude-bootcamp"
STUDENT_ID_FILE="${BOOTCAMP_HOME}/student-id"
CURRENT_SESSION_FILE="${BOOTCAMP_HOME}/current-session"

# Read student ID (exit silently if not set up)
if [ ! -f "$STUDENT_ID_FILE" ]; then
    exit 0
fi
STUDENT_ID=$(cat "$STUDENT_ID_FILE" 2>/dev/null || true)
if [ -z "$STUDENT_ID" ]; then
    exit 0
fi

# Read current session
SESSION=$(cat "$CURRENT_SESSION_FILE" 2>/dev/null || echo "0")

# Read JSON from stdin
INPUT=$(cat)

# Extract user_prompt from JSON (portable sed-based parsing)
PROMPT=$(echo "$INPUT" | sed -n 's/.*"user_prompt"[[:space:]]*:[[:space:]]*"\(.*\)".*/\1/p' | head -1)

# Skip if no prompt captured
if [ -z "$PROMPT" ]; then
    exit 0
fi

# Create log directory
LOG_DIR="${BOOTCAMP_HOME}/logs/${STUDENT_ID}/session-${SESSION}"
mkdir -p "$LOG_DIR" 2>/dev/null || true

# Get timestamp
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date +"%Y-%m-%dT%H:%M:%S")

# Append JSONL line (escape special chars in prompt for valid JSON)
ESCAPED_PROMPT=$(echo "$PROMPT" | sed 's/\\/\\\\/g; s/"/\\"/g; s/\t/\\t/g')
echo "{\"type\":\"prompt\",\"student\":\"${STUDENT_ID}\",\"session\":${SESSION},\"timestamp\":\"${TIMESTAMP}\",\"content\":\"${ESCAPED_PROMPT}\"}" \
    >> "${LOG_DIR}/prompts.jsonl" 2>/dev/null || true

exit 0
