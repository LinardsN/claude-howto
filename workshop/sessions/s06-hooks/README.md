# Session 6: Automated Quality Gates -- Hooks

You have spent the last five sessions building QA functionality with Claude Code:
slash commands, memory, skills, agents, and external integrations. But every one
of those features relies on you remembering to follow your own standards. Hooks
change that equation. They let you embed automated enforcement directly into the
Claude Code workflow so that violations are caught the moment they happen, not
during a manual review three days later.

In this session you will wire up event-driven automation that validates file
naming, triggers linting on every write, and nudges Claude to check test
coverage before signing off. You will also build the first analytics page of
your QA Command Center: a dashboard showing test metrics at a glance.

---

## Learning Objectives

- Create hooks that respond to PreToolUse, PostToolUse, and Stop events
- Distinguish between command hooks and prompt hooks (and when to use each)
- Configure hooks in `.claude/settings.json` with correct event matchers
- Build validation automation that enforces project standards without manual effort
- Display aggregated QA metrics on a React dashboard page

## Prerequisites

- Session 5 gate passed (`./bootcamp complete-session 5` green)
- Working QA Command Center with test case CRUD, bug tracker, and MCP integrations
- Atlassian MCP configured (Jira access verified in S5)
- Node.js + npm, SQLite, running dev environment

## Schedule

| Block | Duration | Activity |
|-------|----------|----------|
| 1 | 15 min | Hooks concept briefing and `.claude/settings.json` walkthrough |
| 2 | 30 min | Build validation hooks (file naming, auto-lint, coverage reminder) |
| 3 | 30 min | Build dashboard page with metrics cards and recent runs table |

**Total: 75 minutes**

---

## The Feature

**Hooks** are event-driven scripts or prompts that Claude Code executes
automatically at specific points in its workflow. They are the enforcement
layer that turns your CLAUDE.md guidelines from suggestions into guarantees.

Read the full reference module: [06-hooks](../../06-hooks/README.md)

Key concepts you will use today:

- **25+ hook events** across four lifecycle stages (PreToolUse, PostToolUse,
  Notification, Stop)
- **Four hook types**: command (shell scripts), prompt (natural language
  instructions), agent (sub-agent delegation), and HTTP (webhook calls)
- **JSON I/O protocol**: hooks receive context as JSON on stdin and return
  structured decisions on stdout
- **Exit codes**: 0 = allow, 2 = block (for PreToolUse), non-zero = error
- **Configuration**: all hooks live in `.claude/settings.json` under the
  `hooks` key, organized by event name

---

## What You Will Build

### Hook 1 -- File Naming Validator (PreToolUse:Write)

A command hook that fires before Claude creates or overwrites any file. It
inspects the target filename and blocks the operation if it violates your
project's naming conventions (the ones you defined in your Session 2 CLAUDE.md).

**Example**: if your CLAUDE.md says components use PascalCase and API routes use
kebab-case, this hook rejects `testCaseList.jsx` or `Test_Cases.js` before the
file ever hits disk.

### Hook 2 -- Auto-Lint (PostToolUse:Write)

A command hook that runs after Claude successfully writes a file. It triggers
your linter (ESLint, Prettier, or whatever your project uses) and reports any
issues back. This ensures every file Claude produces meets code quality
standards without you having to remember to ask.

### Hook 3 -- Test Coverage Reminder (Stop)

A prompt hook that activates when Claude finishes a conversation turn. It
reminds Claude to check whether any new code has corresponding tests and
to report the current coverage status. This is a lightweight nudge, not a
blocker -- it uses the prompt hook type rather than a command.

### Dashboard Page

A new React page in your QA Command Center showing:

- **Metrics cards**: total tests, pass rate, open bugs, average severity
- **Recent test runs table**: date, suite name, passed/failed/skipped counts,
  duration
- Data served from your Express API, stored in SQLite

---

## Requirements

### Must-Have (Gate Checks)

- [ ] `.claude/settings.json` exists and contains at least one hook configuration
- [ ] At least one hook script exists in `.claude/hooks/` (or your project's hook directory)
- [ ] Dashboard page renders at a dedicated route (e.g., `/dashboard`)
- [ ] Dashboard displays at least three metric values from the API
- [ ] Recent test runs table shows at least columns for date, suite name, and result counts

### Should-Have (Bonus Points)

- [ ] Multiple hook event types configured (PreToolUse + PostToolUse + Stop)
- [ ] Hooks enforce standards defined in your Session 2 CLAUDE.md (progressive dependency)
- [ ] Dashboard metrics are computed from actual database records, not hardcoded
- [ ] Auto-lint hook runs a real linter and reports results

---

## Rules

1. **Hooks must enforce YOUR standards.** The file naming hook should validate
   the naming conventions you wrote in your Session 2 CLAUDE.md. Do not invent
   new conventions -- enforce the ones you already committed to.

2. **Every hook must be testable.** You should be able to trigger each hook and
   observe its effect. A hook that silently does nothing is a hook that does
   not exist.

3. **Command hooks must handle errors gracefully.** A hook that crashes on
   unexpected input is worse than no hook at all. Think about edge cases:
   what if the filename has no extension? What if the file path is deeply
   nested?

4. **The dashboard must show real data.** Seed your database if you have no
   test runs yet, but the API endpoint must query the database, not return
   a hardcoded JSON blob.

5. **All code is vibe-coded.** Claude Code generates every line. Your job is
   to describe what you want precisely enough that Claude gets it right.

---

## Hints (Not Solutions)

- A PreToolUse:Write hook receives the file path in its JSON input. Think
  about how to extract just the filename and compare it against a naming
  pattern.

- Exit code 2 from a PreToolUse hook blocks the operation. Exit code 0
  allows it. Your hook script needs to make that decision and exit
  accordingly.

- A Stop prompt hook is just a natural language instruction, not a script.
  Think about what reminder would be most useful when Claude finishes a
  coding task.

- For the dashboard, consider what aggregate queries you need: `COUNT(*)`,
  `AVG()`, `SUM(CASE WHEN ...)`. These can power your metrics cards in a
  single API call.

- The `.claude/settings.json` hooks section uses event names as keys. Each
  event maps to an array of hook definitions. Check the reference module for
  the exact schema.

---

## Jira Integration

Using the Atlassian MCP (configured in Session 5):

1. **Create a "Quality Gates" epic** in your project board
2. **Write stories** for each deliverable:
   - File naming validation hook
   - Auto-lint hook
   - Test coverage reminder hook
   - Dashboard metrics API endpoint
   - Dashboard React page with cards and table
3. **Add acceptance criteria** to each story that match the Must-Have
   requirements above
4. **Update story status** as you complete each piece

Remember: all Jira operations happen through Claude Code prompts, not the
Jira web UI. This is how you practiced in Session 5.

---

## Verification

Before running `./bootcamp complete-session 6`, self-check:

1. **File naming hook test**: Ask Claude to create a file with a name that
   violates your CLAUDE.md conventions. Does the hook block it? Check the
   terminal output for the rejection message.

2. **Auto-lint hook test**: Ask Claude to write a file with minor style
   issues. Does the PostToolUse hook report linting results?

3. **Coverage reminder test**: Complete a coding task and observe whether
   the Stop hook prompts Claude about test coverage.

4. **Dashboard test**: Navigate to your dashboard route. Are the metrics
   cards showing numbers? Does the recent runs table have rows? Try
   adding a test run record and refreshing -- does the dashboard update?

5. **Settings check**: Open `.claude/settings.json` and verify the hooks
   section is well-formed JSON with the correct event names.

```bash
# Validate your session deliverables
./bootcamp complete-session 6
```
