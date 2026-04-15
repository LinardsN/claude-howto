# Session Index

Complete guide to all 10 bootcamp sessions. Each session teaches one Claude Code feature by building functionality into your QA Command Center.

## Schedule Overview

The bootcamp is organized into 5 half-days, each containing 2 sessions with a 15-minute break between them.

| Half-Day | Sessions | Theme | Duration |
|----------|----------|-------|----------|
| **1** | S1 + S2 | Getting Started | ~3 hours |
| **2** | S3 + S4 | Building Workflows | ~3 hours |
| **3** | S5 + S6 | Integration and Automation | ~3 hours |
| **4** | S7 + S8 | Packaging and Experimentation | ~3 hours |
| **5** | S9 + S10 | Power User and Ship It | ~3 hours |

## Sessions

### Half-Day 1: Getting Started

| # | Title | Feature | What You Build | Guide |
|---|-------|---------|----------------|-------|
| 1 | First Contact | [Slash Commands](../../01-slash-commands/README.md) | Project scaffold, custom `/new-test-case` and `/bug-report` commands | [s01-slash-commands/](s01-slash-commands/README.md) |
| 2 | Teaching Claude Your Standards | [Memory](../../02-memory/README.md) | CLAUDE.md with QA standards, test case CRUD API + React page | [s02-memory/](s02-memory/README.md) |

### Half-Day 2: Building Workflows

| # | Title | Feature | What You Build | Guide |
|---|-------|---------|----------------|-------|
| 3 | Reusable QA Workflows | [Skills](../../03-skills/README.md) | `/generate-test-suite` and `/qa-review` skills, test suite page | [s03-skills/](s03-skills/README.md) |
| 4 | Specialized QA Agents | [Subagents](../../04-subagents/README.md) | Test writer, bug triager, security scanner agents; bug tracker module | [s04-subagents/](s04-subagents/README.md) |

### Half-Day 3: Integration and Automation

| # | Title | Feature | What You Build | Guide |
|---|-------|---------|----------------|-------|
| 5 | Connecting to the QA Ecosystem | [MCP](../../05-mcp/README.md) | GitHub MCP, Jira MCP, bug-to-issue sync, test run executor | [s05-mcp/](s05-mcp/README.md) |
| 6 | Guardrails and Automation | [Hooks](../../06-hooks/README.md) | Pre-commit quality hooks, notification hooks, standards enforcement | [s06-hooks/](s06-hooks/README.md) |

### Half-Day 4: Packaging and Experimentation

| # | Title | Feature | What You Build | Guide |
|---|-------|---------|----------------|-------|
| 7 | Bundle and Ship | [Plugins](../../07-plugins/README.md) | Plugin that bundles skills, agents, and hooks from previous sessions | [s07-plugins/](s07-plugins/README.md) |
| 8 | Fearless Experimentation | [Checkpoints](../../08-checkpoints/README.md) | Experimental features using checkpoint/rewind, A/B testing approaches | [s08-checkpoints/](s08-checkpoints/README.md) |

### Half-Day 5: Power User and Ship It

| # | Title | Feature | What You Build | Guide |
|---|-------|---------|----------------|-------|
| 9 | Thinking at Scale | [Advanced Features](../../09-advanced-features/README.md) | Plan mode for complex features, extended thinking, background agents | [s09-advanced/](s09-advanced/README.md) |
| 10 | Ship It | [CLI and CI/CD](../../10-cli/README.md) | CI pipeline, headless mode, final independent feature build | [s10-cli/](s10-cli/README.md) |

## How Sessions Work

### Before Each Session

1. Run `./bootcamp start-session N` to validate prerequisites and unlock the guide
2. Read the session README.md for goals, requirements, and rules
3. Check deliverables.md to know exactly what you need to produce
4. Use reference.md as a quick lookup for the feature's syntax and options

### During Each Session

- **Craft your own prompts** — guides provide goals and hints, not copy-paste solutions
- Use QA domain terminology naturally (ISTQB severity levels, test techniques, defect lifecycle)
- Build on top of what you created in previous sessions
- Self-check using the verification section before submitting

### After Each Session

1. Run `./bootcamp complete-session N` to submit for automated validation
2. Gate checks verify your deliverables against the acceptance criteria
3. Your score is recorded and the next session is unlocked

## Progressive Dependencies

Each session builds on the previous ones. Features you create early are reused later:

```text
S1 slash commands ──────────────────────────────────────> S7 plugin bundles them
S2 CLAUDE.md rules ─────────────────────────> S6 hooks enforce them
S3 skills ──────────> S4 agents reference ──> S7 plugin bundles them
S4 agents ──────────────────────────────────> S7 plugin bundles them
S5 MCP configs ─────────────────────────────────────────> S10 CI uses them
S6 hooks ───────────────────────────────────> S7 plugin bundles them
```

## Quick Links

- [Scoring Rubric](../SCORING-RUBRIC.md) — how your work is graded (0-100 scale)
- [Instructor Guide](../INSTRUCTOR-GUIDE.md) — for cohort administrators
- [Workshop Overview](../README.md) — prerequisites and setup
