# Session 4: Specialized QA Agents -- Subagents

Skills are reusable workflows. Agents are specialized personas that combine skills, tool access, and domain expertise into focused assistants. In this session, you create QA-specialized agents with restricted tool access and build the bug tracker module they will operate on.

## Learning Objectives

- Create custom agent `.md` files with YAML frontmatter in `.claude/agents/`
- Restrict agent tool access for security and focus (e.g., read-only agents)
- Understand how agents delegate tasks and maintain isolated context
- Connect agents to skills from Session 3 for composable workflows
- Build a full bug tracker module with severity-based filtering

## Prerequisites

- Session 3 gate passed (`./bootcamp complete-session 3`)
- At least 2 skills in `.claude/skills/`
- Test case and test suite features working

## Schedule

| Time | Activity | Duration |
|------|----------|----------|
| 0:00 | Explore the /agents command and built-in agents | 10 min |
| 0:10 | Create custom QA agents | 30 min |
| 0:40 | Build the bug tracker module | 35 min |
| **Total** | | **75 min** |

## The Feature: Subagents

> **Reference module**: [04-subagents/README.md](../../04-subagents/README.md)

Subagents are specialized AI assistants that Claude can delegate tasks to. Each agent:

- Has its own context window (isolated from your main conversation)
- Follows a custom system prompt defined in its `.md` file
- Can be restricted to specific tools (Read, Write, Bash, Grep, etc.)
- Returns results to the main conversation when done
- Can be invoked via `/agents` or delegated to automatically

### Agent File Format

Agent files live in `.claude/agents/` as markdown files with YAML frontmatter:

```yaml
---
description: Generates comprehensive test cases using ISTQB techniques and project standards
tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
model: sonnet
permissionMode: default
---
```

The body of the file is the agent's system prompt -- its instructions, personality, and constraints.

### Key Frontmatter Fields

| Field | Purpose | Example |
|-------|---------|---------|
| `description` | What the agent does (shown in `/agents` list) | "Generates test cases using ISTQB techniques" |
| `tools` | Which tools the agent can use | `[Read, Grep, Glob]` for read-only |
| `model` | Which model the agent uses | `sonnet`, `opus`, `haiku` |
| `permissionMode` | How tool permissions are handled | `default`, `permissive`, `strict` |

### Tool Restrictions

This is one of the most powerful features. You can limit what an agent can do:

- **Full access**: `[Read, Write, Edit, Bash, Grep, Glob]` -- can read and modify files, run commands
- **Read-only**: `[Read, Grep, Glob]` -- can only read and search files, never modify
- **Analysis-only**: `[Read, Grep, Glob, Bash]` -- can read files and run commands, but not write

Tool restriction is critical for security-focused agents. A security scanner should analyze code, not modify it.

### Delegation

Claude can delegate tasks to agents in two ways:

1. **Explicit**: You ask Claude to use a specific agent via `/agents`
2. **Automatic**: Claude recognizes a task matches an agent's description and delegates

## What You Will Build

### 1. Test Writer Agent

An agent specialized in generating test cases. It should:

- Reference the `/generate-test-suite` skill from Session 3
- Follow the test case data model defined in your CLAUDE.md
- Have full file access (Read, Write, Edit, Bash, Grep, Glob) since it creates files
- Specialize in ISTQB test design techniques
- Produce test cases that integrate with your existing test case data model

### 2. Bug Triager Agent

An agent specialized in categorizing and prioritizing bugs. It should:

- Analyze bug reports and assign appropriate severity (critical, major, minor, trivial)
- Classify bugs by type (functional, performance, security, usability, compatibility)
- Suggest priority based on severity and business impact
- Have restricted tools -- it needs to read code and data but should not modify production code
- Follow the severity definitions from your CLAUDE.md

### 3. Security Scanner Agent

A read-only agent that audits code for security concerns. It should:

- Have strictly limited tools: `Read`, `Grep`, `Glob` only -- no Write, Edit, or Bash
- Scan for common vulnerabilities: SQL injection, XSS, missing input validation, hardcoded secrets
- Produce findings categorized by risk level
- Focus on the QA perspective: what security test cases should be created based on the findings?
- Never modify any files (enforced by tool restrictions)

### 4. Bug Tracker Module

A full-featured bug tracking system added to the QA Command Center:

- **Data model**: Bug entity with fields for summary, description, reproduction steps, actual vs expected behavior, severity, priority, status (open, in-progress, resolved, closed, reopened), environment, reporter, assignee
- **API routes**: Full CRUD for bugs plus filtering by severity and status
- **React bug report form**: Form to submit new bugs with all required fields
- **React bug list page**: Filterable list showing bugs with severity indicators, status badges, and sort options

## Requirements

### Must-Have (Gate Checks)

- [ ] `.claude/agents/` directory exists with at least 2 agent `.md` files
- [ ] Each agent file has valid YAML frontmatter with a `description` field
- [ ] At least one agent has a `tools` restriction in frontmatter
- [ ] Bug tracker API routes exist (GET and POST minimum)
- [ ] Bug report form React component exists
- [ ] Bug list React page exists and renders

### Should-Have (Bonus Points)

- [ ] 3 agent files: test-writer, bug-triager, security-scanner
- [ ] Security scanner agent is restricted to read-only tools (`Read`, `Grep`, `Glob`)
- [ ] At least one agent references a skill from Session 3 in its system prompt
- [ ] Bug list page supports filtering by severity
- [ ] Bug data model includes all defect lifecycle statuses (open, in-progress, resolved, closed)
- [ ] Agents appear in the `/agents` command output

## Rules

1. **Each agent must have a specific QA-domain purpose.** No generic agents like "code helper" or "general assistant." Every agent solves a QA engineering problem.

2. **At least one agent must have restricted tools.** The security scanner is the natural candidate -- it should analyze, not modify. This demonstrates the principle of least privilege.

3. **Agents should reference previous work.** Your test-writer agent should mention the generate-test-suite skill. Your bug-triager should reference the severity definitions from CLAUDE.md. Build on what you have created.

4. **Build agents before the bug tracker.** Create the agents first so you can use them (especially the bug-triager) when building and testing the bug tracker module.

## Hints (Not Solutions)

### Creating the Test Writer Agent

- Think about what makes a test writer different from a general-purpose Claude. What specific expertise should it have? What constraints should it follow?
- The agent's system prompt should reference your project's test case data model. If your CLAUDE.md says test cases have specific fields, the test writer should know about those fields.
- Consider having the agent reference the `/generate-test-suite` skill by name so it can be invoked as part of the agent's workflow.

### Creating the Bug Triager Agent

- A bug triager needs to understand severity vs priority -- they are related but different. Severity is the technical impact; priority is the business urgency. Your agent should know the difference.
- Think about what tools a triager needs. They need to read bug reports and code to understand context, but do they need to write files? Probably limited write access at most.
- The triager's system prompt should include your project's severity classification scheme from CLAUDE.md.

### Creating the Security Scanner Agent

- This is your strictest agent. It should ONLY have Read, Grep, and Glob tools. No Write, no Edit, no Bash. A security scanner that can execute arbitrary commands defeats its own purpose.
- Think about what the scanner should look for: unvalidated inputs, SQL string concatenation, missing authentication checks, hardcoded credentials, overly permissive CORS settings.
- The output should be actionable: each finding should include the file, line, risk level, and a recommendation.

### Building the Bug Tracker

- The bug tracker is the largest feature so far. Break it into steps: data model first, then API routes, then the form, then the list page.
- Ask Claude to create the bug data model following your CLAUDE.md conventions. If you defined a standard API response format, remind Claude to use it.
- Severity filtering on the list page is a great opportunity to use the values you defined in your CLAUDE.md. The filter options should match your severity levels exactly.

### Common Pitfalls

- Forgetting the `tools` field in frontmatter creates agents with default (full) tool access. Be explicit about restrictions.
- Agent system prompts that are too short give Claude no guidance. Write substantive prompts that describe the agent's expertise, constraints, and output format.
- Do not confuse agent files with skill files. Agents go in `.claude/agents/`, skills go in `.claude/skills/`.

## Verification

Before running `./bootcamp complete-session 4`, verify:

1. **Agents listed**: Run `/agents` in Claude Code and confirm your custom agents appear
2. **Tool restrictions**: Check that the security scanner (or equivalent) has restricted tools in its frontmatter
3. **Bug form works**: Open the bug report form, fill in fields, and submit
4. **Bug list renders**: Navigate to the bug list page and see submitted bugs
5. **Severity filtering**: If implemented, verify the filter works with your ISTQB severity levels
6. **Agent delegation**: Ask Claude to delegate a task to one of your agents and confirm it works

```bash
./bootcamp complete-session 4
```

## What Comes Next

In Session 5, you will connect your QA Command Center to external systems using MCP (Model Context Protocol). You will configure GitHub MCP to sync bugs to GitHub Issues and Jira MCP to manage your project. The bug tracker you built here becomes the bridge between your local app and the external QA ecosystem.
