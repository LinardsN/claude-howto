# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository has **two distinct products**:

### 1. Reference Tutorial (modules 01-10)

Documentation-as-code — 10 numbered learning modules covering Claude Code features with copy-paste templates, Mermaid diagrams, and examples. The build system validates documentation quality and generates an EPUB ebook.

### 2. AI Bootcamp Platform (`workshop/`)

A fully automated, AI-driven bootcamp where QA engineers learn Claude Code by building a real React web app ("QA Command Center"). Includes student registration, prompt monitoring via hooks, automated phase gates with progressive dependencies, AI-based scoring (0-100), Jira integration, instructor dashboard, and a version watcher that auto-updates content when Claude Code releases new features.

**Important**: The two products are independent. The reference tutorial teaches concepts; the bootcamp is an interactive platform that uses the reference tutorial as its curriculum.

## Common Commands

### Pre-commit Quality Checks

All documentation must pass four quality checks before commits (these run automatically via pre-commit hooks):

```bash
# Install pre-commit hooks (runs on every commit)
pre-commit install

# Run all checks manually
pre-commit run --all-files
```

The four checks are:
1. **markdown-lint** — Markdown structure and formatting via `markdownlint`
2. **cross-references** — Internal links, anchors, code fence syntax (Python script)
3. **mermaid-syntax** — Validates all Mermaid diagrams parse correctly (Python script)
4. **link-check** — External URLs are reachable (Python script)
5. **build-epub** — EPUB generates without errors (on `.md` changes)

### Development Environment Setup

```bash
# Install uv (Python package manager)
pip install uv

# Create virtual environment and install Python dependencies
uv venv
source .venv/bin/activate
uv pip install -r scripts/requirements-dev.txt

# Install Node.js tools (markdown linter and Mermaid validator)
npm install -g markdownlint-cli
npm install -g @mermaid-js/mermaid-cli

# Install pre-commit hooks
uv pip install pre-commit
pre-commit install
```

### Testing

Python scripts in `scripts/` have unit tests:

```bash
# Run all tests
pytest scripts/tests/ -v

# Run with coverage
pytest scripts/tests/ -v --cov=scripts --cov-report=html

# Run specific test
pytest scripts/tests/test_build_epub.py -v
```

### Code Quality

```bash
# Lint and format Python code
ruff check scripts/
ruff format scripts/

# Security scan
bandit -c scripts/pyproject.toml -r scripts/ --exclude scripts/tests/

# Type checking
mypy scripts/ --ignore-missing-imports
```

### EPUB Build

```bash
# Generate ebook (renders Mermaid diagrams via Kroki.io API)
uv run scripts/build_epub.py

# With options
uv run scripts/build_epub.py --verbose --output custom-name.epub --max-concurrent 5
```

## Directory Structure

```
├── 01-slash-commands/      # Reference tutorial: User-invoked shortcuts
├── 02-memory/              # Reference tutorial: Persistent context examples
├── 03-skills/              # Reference tutorial: Reusable capabilities
├── 04-subagents/           # Reference tutorial: Specialized AI assistants
├── 05-mcp/                 # Reference tutorial: Model Context Protocol examples
├── 06-hooks/               # Reference tutorial: Event-driven automation
├── 07-plugins/             # Reference tutorial: Bundled features
├── 08-checkpoints/         # Reference tutorial: Session snapshots
├── 09-advanced-features/   # Reference tutorial: Planning, thinking, backgrounds
├── 10-cli/                 # Reference tutorial: CLI reference
├── workshop/               # ** AI BOOTCAMP PLATFORM **
│   ├── CLAUDE.md               # Workshop development guidance (read this before editing workshop/)
│   ├── README.md               # Student-facing bootcamp overview
│   ├── INSTRUCTOR-GUIDE.md     # Cohort management + facilitation
│   ├── SCORING-RUBRIC.md       # Transparent 0-100 grading criteria
│   ├── bootcamp                # CLI entry point (chmod +x)
│   ├── demo.sh                 # Demo: spin up sample cohort with fake students
│   ├── platform/               # Core platform logic (Python)
│   │   ├── cli.py              # All CLI subcommands
│   │   ├── config.py           # Constants, paths, scoring weights
│   │   ├── database.py         # SQLite schema + CRUD
│   │   ├── registration.py     # Cohort + student management
│   │   └── student_setup.py    # Onboarding: dirs, hooks install
│   ├── hooks/                  # Claude Code hooks for prompt logging
│   │   ├── log-prompt.sh       # UserPromptSubmit hook
│   │   ├── log-response.sh     # Stop hook
│   │   └── hooks-settings.json # Template settings.json
│   ├── gates/                  # Phase gate validators (10 sessions)
│   │   ├── common.py           # Shared validation utilities
│   │   ├── gate_runner.py      # Orchestrator
│   │   └── gate_sNN_*.py       # Per-session validators
│   ├── scoring/                # Automated grading
│   │   ├── rubric.py           # Weights and thresholds
│   │   ├── prompt_analyzer.py  # Prompt quality (AI + heuristic)
│   │   ├── efficiency_analyzer.py
│   │   ├── deliverable_analyzer.py
│   │   ├── standards_analyzer.py
│   │   ├── scorer.py           # Main aggregator
│   │   └── report_generator.py # HTML/CSV/JSON reports
│   ├── sessions/               # 10 session guides (the curriculum)
│   │   ├── README.md           # Session index
│   │   └── s01-*/ through s10-*/  # Each with README.md, reference.md, deliverables.md
│   ├── templates/              # Reference templates (CLAUDE.md, skill, agent, hook, plugin, Jira)
│   ├── admin/                  # Instructor tools (dashboard, cohort report, export)
│   ├── scripts/                # Maintenance scripts
│   │   └── check-claude-version.sh  # Version watcher: daily Claude Code release check
│   ├── cheatsheet/             # Quick reference cards
│   └── tests/                  # Platform unit tests
├── scripts/
│   ├── build_epub.py               # EPUB generator (Reference tutorial)
│   ├── check_cross_references.py   # Validates internal links
│   ├── check_links.py              # Checks external URLs
│   ├── check_mermaid.py            # Validates Mermaid syntax
│   └── tests/                      # Unit tests for scripts
├── .github/workflows/
│   └── version-watcher.yml     # Daily Claude Code release detection -> auto-PR
├── .pre-commit-config.yaml     # Quality check definitions
└── README.md                   # Main reference tutorial guide
```

## AI Bootcamp Platform — Operations

### What It Is

The `workshop/` directory contains a fully-automated AI-driven bootcamp platform. It's designed for a cohort of QA engineers (TestDevLab's 500+ engineers) to learn Claude Code over 5 half-days by building a React web app called "QA Command Center". Key characteristics:

- **100% vibe-coded**: Students never write code manually — Claude generates everything
- **No copy-paste prompts**: Session guides provide goals/rules/hints; students craft their own prompts
- **Progressive dependencies**: Skills created in S3 must be used in S4 agents and bundled in S7 plugin — gate validators enforce this
- **Fully autonomous**: No instructor intervention needed. Failing gates escalate through 3 stages (basic feedback → Socratic hints → auto-unlock with 20% penalty)
- **Prompt logging**: Every student prompt is captured via `UserPromptSubmit` hook and stored in JSONL
- **AI-based scoring**: 0-100 score combining prompt quality (25%), efficiency (15%), deliverables (20%), standards (15%), final task (25%)

### Running the Demo (See How It Looks)

The demo creates 3 fake students in different progress states so you can visually explore the platform without doing the bootcamp yourself:

```bash
cd workshop
./demo.sh
```

Creates:
- **Alice** — completed S1-S3 with high-quality prompts, score ~100
- **Bob** — struggling, triggered auto-unlock at attempt 5 with 20% penalty
- **Carol** — just registered, no session started

Then explore:

```bash
./bootcamp dashboard                                 # Live view of all 3 students
./bootcamp status --student alice --detailed        # Per-session score breakdown
./bootcamp status --student alice --prompts         # See logged prompts
./bootcamp status --student bob --detailed          # See auto-unlock state
./bootcamp scores --format html --output /tmp/scores.html   # Open in browser
./bootcamp grade alice --no-ai                       # Full heuristic scoring
```

Reset with: `rm -rf ~/.claude-bootcamp`

### Running in Production (Real Bootcamp)

Full flow for a student going through the bootcamp:

```bash
cd workshop

# Admin: Open registration for a cohort
./bootcamp open-registration --cohort "cohort-2026-q2" \
  --name "TestDevLab Q2 2026" \
  --deadline "2026-12-31"

# Admin: Register students
./bootcamp register alice "Alice Anderson" alice@testdevlab.com --cohort cohort-2026-q2
./bootcamp register bob "Bob Brown" bob@testdevlab.com --cohort cohort-2026-q2

# Admin: Close registration when ready
./bootcamp close-registration --cohort cohort-2026-q2

# Student: Set up their environment (installs prompt logging hooks)
mkdir -p ~/qa-command-center
./bootcamp setup --student-id alice --project-dir ~/qa-command-center

# Student: Begin session 1
./bootcamp start-session 1

# Student: Opens Claude Code in the project directory
cd ~/qa-command-center
claude
# (Student reads workshop/sessions/s01-*/README.md and crafts own prompts)
# (Every prompt gets logged to ~/.claude-bootcamp/logs/alice/session-1/prompts.jsonl)

# Student: Submit session for gate validation
cd /path/to/workshop
./bootcamp complete-session 1 --project-dir ~/qa-command-center
# -> Gate runs, checks pass/fail, score recorded
# -> If critical checks fail: escalating feedback → hints → auto-unlock

# Student: Continue through all 10 sessions
./bootcamp start-session 2
# ... repeat
```

Admin monitoring:

```bash
./bootcamp dashboard              # Live real-time view
./bootcamp scores --format html   # Export cohort report
./bootcamp grade alice            # Full AI-powered scoring
./bootcamp unlock-session 5 --student alice --reason "npm timeout"   # Manual override
```

### Session Gating Behavior

Each session has a gate that checks specific requirements. Behavior depends on attempt count:

| Attempt | What Happens |
|---------|-------------|
| 1-2 | Show which critical checks failed, basic feedback |
| 3-4 | Show **Socratic hints** that point toward the right concept (without giving the answer) |
| 5+ | **Auto-unlock** with 20% score penalty. Student can still re-run for full credit |

Critical checks **block progression**. Bonus checks only **affect score**.

### Progressive Dependency Chain

The curriculum builds on itself. Gates enforce these cross-session dependencies:

- S1 slash commands → S7 plugin must bundle them
- S2 CLAUDE.md rules → S6 hooks must enforce them
- S3 skills → S4 agents must reference them, S7 plugin bundles them
- S4 agents → S7 plugin bundles them
- S5 MCP configs → S10 CI uses them
- S6 hooks → S7 plugin bundles them, S10 CI uses hook validation

If a student skips content, later gates will fail because the dependencies don't exist.

### Architecture Summary

```
~/.claude-bootcamp/              # Local student state
├── student-id                   # Current student ID
├── current-session              # Which session they're on
├── bootcamp.db                  # SQLite: cohorts, students, progress, scores, prompt logs
└── logs/<student-id>/session-N/
    └── prompts.jsonl            # All prompts + responses for that session

Project directory (e.g., ~/qa-command-center/)
├── .claude/
│   ├── settings.json            # Hook config pointing to log-prompt.sh + log-response.sh
│   ├── hooks/                   # Logging scripts (copied during setup)
│   ├── skills/                  # Student creates in S1, S3
│   ├── agents/                  # Student creates in S4
│   └── rules/                   # Student creates in S2
├── .claude-plugin/              # Student creates in S7
├── .mcp.json                    # Student configures in S5
├── CLAUDE.md                    # Student creates in S2
├── package.json                 # Student creates in S1
└── [Express + React code]       # Generated by Claude throughout
```

### Testing the Platform

```bash
# Run all platform unit tests
python -m pytest workshop/tests/ -v

# Lint platform code
ruff check workshop/
```

### Version Watcher

A GitHub Action (`.github/workflows/version-watcher.yml`) runs daily:

1. Checks `npm view @anthropic-ai/claude-code version` against `workshop/.version-tracker`
2. If a new version is detected, pipes the changelog to `claude -p` with a structured prompt asking which sessions are impacted
3. If impacted sessions found, creates a PR with proposed updates
4. If no impact, silently updates `.version-tracker` and exits

This keeps the workshop content automatically in sync with Claude Code releases.

---

## Content Guidelines (Reference Tutorial)

### Module Structure
Each numbered folder follows the pattern:
- **README.md** — Overview of the feature with examples
- **Example files** — Copy-paste templates (`.md` for commands, `.json` for configs, `.sh` for hooks)
- Files are organized by feature complexity and dependencies

### Mermaid Diagrams
- All diagrams must parse successfully (checked by pre-commit hook)
- EPUB build renders diagrams via Kroki.io API (requires internet)
- Use Mermaid for flowcharts, sequence diagrams, and architecture visuals

### Cross-References
- Use relative paths for internal links (e.g., `(01-slash-commands/README.md)`)
- Code fences must specify language (e.g., ` ```bash `, ` ```python `)
- Anchor links use `#heading-name` format

### Link Validation
- External URLs must be reachable (checked by pre-commit hook)
- Avoid linking to ephemeral content
- Use permalinks where possible

## Key Architecture Points

### Reference Tutorial (modules 01-10)

1. **Numbered folders indicate learning order** — The 01-10 prefix represents the recommended sequence for learning Claude Code features. This numbering is intentional; do not reorganize alphabetically.

2. **Scripts are utilities, not the product** — The Python scripts in `scripts/` support documentation quality and EPUB generation. The actual content is in the numbered module folders.

3. **Pre-commit is the gatekeeper** — All four quality checks must pass before a PR is accepted. The CI pipeline runs these same checks as a second pass.

4. **Mermaid rendering requires network** — The EPUB build calls Kroki.io API to render diagrams. Build failures here are typically network issues or invalid Mermaid syntax.

5. **This is a tutorial, not a library** — When adding content, focus on clear explanations, copy-paste examples, and visual diagrams. The value is in teaching concepts, not providing reusable code.

### Bootcamp Platform (workshop/)

1. **Two distinct directories, one repo** — `workshop/` is independent of the reference tutorial. Always read `workshop/CLAUDE.md` before modifying anything in that directory.

2. **NO copy-paste prompts in session guides** — Session guides provide goals, rules, and hints. Students must craft their own prompts. This is the core pedagogical principle — do not violate it.

3. **Progressive dependencies are enforced by gates** — When modifying gate validators, always check that cross-session references are verified (e.g., S7 plugin must bundle S3/S4/S6 artifacts).

4. **Hints are Socratic, not prescriptive** — The hint system in `workshop/platform/cli.py` points toward the right concept without giving the answer. Never add hints that say "Create X file at Y path".

5. **Hooks must never block the student** — Logging hooks always exit 0, handle missing directories with `mkdir -p`, and use `|| true` guards. A broken log should never prevent a student from working.

6. **Score penalties are visible, not hidden** — When auto-unlocking after 5 attempts, the student sees the penalty clearly and can re-run for full credit. Transparency is required.

## Commit Conventions

Follow conventional commit format:
- `feat(slash-commands): Add API documentation generator`
- `docs(memory): Improve personal preferences example`
- `fix(README): Correct table of contents link`
- `refactor(hooks): Simplify hook configuration examples`

Scope should match the folder name when applicable.
