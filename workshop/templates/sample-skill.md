---
name: example-qa-skill
version: 1.0.0
description: "Triggers when the user asks about generating test suites or test cases for a feature"
---

<!-- TEMPLATE: This shows the structure of a SKILL.md file -->
<!-- Students should create their own skills, not copy this one -->

# Example QA Skill

## Purpose

This skill demonstrates the SKILL.md format with:

- YAML frontmatter (name, version, description)
- The `description` field enables auto-invocation
- Supporting content below the frontmatter

## Key Frontmatter Fields

| Field | Required | Purpose |
|-------|----------|---------|
| `name` | Yes | Unique identifier |
| `version` | No | Semantic version |
| `description` | Yes | Trigger phrase for auto-invocation |

## Auto-Invocation

The `description` field is matched against user input. When someone types:
"I need a test suite for the login feature"

...and your description mentions "test suites" or "test cases", the skill
auto-invokes without the user typing a slash command.

## Supporting Files

Skills can include supporting directories:

```text
.claude/skills/my-skill/
  SKILL.md              # The skill definition
  templates/            # Output templates
  references/           # Reference material
  scripts/              # Helper scripts
```
