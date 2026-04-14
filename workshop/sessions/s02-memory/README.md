# Session 2: Teaching Claude Your Standards -- Memory

Claude Code is powerful, but without guidance it generates code using generic conventions. In this session, you teach Claude your team's QA standards by creating persistent memory files. Then you verify those standards are applied by building your first real feature: test case management.

## Learning Objectives

- Create a project CLAUDE.md that encodes your QA team's standards and conventions
- Use the `/init` command to bootstrap memory and `/memory` to edit it
- Create path-specific rules in `.claude/rules/` for different parts of the codebase
- Understand the 7-level memory hierarchy and how Claude resolves conflicting instructions
- Verify that Claude-generated code follows the standards you defined

## Prerequisites

- Session 1 gate passed (`./bootcamp complete-session 1`)
- QA Command Center project scaffold running from Session 1

## Schedule

| Time | Activity | Duration |
|------|----------|----------|
| 0:00 | Create and configure CLAUDE.md | 15 min |
| 0:15 | Define QA standards and path-specific rules | 30 min |
| 0:45 | Build test case CRUD (API + React page) | 30 min |
| **Total** | | **75 min** |

## The Feature: Memory

> **Reference module**: [02-memory/README.md](../../02-memory/README.md)

Memory in Claude Code is a hierarchy of persistent files that give Claude context about your project, your team's conventions, and your personal preferences. Unlike conversation context that disappears when you start a new session, memory files persist on disk and are loaded every time Claude starts.

### Memory Hierarchy (7 Levels)

Claude loads memory from multiple sources, with later levels overriding earlier ones:

| Level | Source | Scope | Example |
|-------|--------|-------|---------|
| 1 | Enterprise policy | Organization-wide | Company coding standards |
| 2 | `~/.claude/CLAUDE.md` | All your projects | Personal preferences |
| 3 | Project `CLAUDE.md` | This project | Tech stack, conventions |
| 4 | `.claude/rules/*.md` | Path-specific | Server rules vs client rules |
| 5 | Imported files (`@`) | Referenced docs | API documentation |
| 6 | `/init` output | Project bootstrap | Auto-detected conventions |
| 7 | `/memory` edits | Session additions | Conversation learnings |

For this session, you will focus on levels 3 and 4: the project CLAUDE.md and path-specific rules.

### Key Commands

| Command | Purpose |
|---------|---------|
| `/init` | Bootstrap a CLAUDE.md by analyzing your project |
| `/memory` | Open CLAUDE.md in your editor for manual editing |
| `@path/to/file` | Import content from another file into CLAUDE.md |

### The Rules Directory

Files in `.claude/rules/` apply only when Claude is working on files that match the rule's path context. This lets you define different standards for different parts of your codebase:

```text
.claude/
  rules/
    server.md      # Rules for server/ directory (API conventions, error handling)
    client.md      # Rules for client/ directory (component patterns, styling)
    tests.md       # Rules for test files (assertion style, naming)
```

## What You Will Build

### 1. CLAUDE.md with QA Standards

A comprehensive project memory file that encodes your team's QA engineering standards. Think about what a QA team needs to standardize:

- **Naming conventions**: How are test cases named? What about API endpoints? React components?
- **Data model conventions**: What fields does every test case need? What are the valid severity levels?
- **API response format**: Standard envelope (e.g., `{ success: boolean, data: ..., error: ... }`)
- **ISTQB terminology**: Severity levels (critical, major, minor, trivial), test types, defect lifecycle states
- **Code organization**: Where do models go? Controllers? React components?

### 2. Path-Specific Rules

At least one rule file in `.claude/rules/` that applies different standards to different parts of the project. For example, server-side code might require JSDoc comments while client-side code follows React component conventions.

### 3. Test Case Management Feature

A functional test case CRUD system spanning both backend and frontend:

- **Data model**: Test case entity with fields appropriate for ISTQB-aligned QA work (title, description, preconditions, steps, expected results, severity, priority, status, type)
- **API routes**: RESTful endpoints for create, read (list + detail), update, and delete test cases
- **React page**: A page that displays test cases in a list/table and provides a form to create new ones
- **SQLite storage**: Test cases persisted to a SQLite database (since this is a Node.js project, consider `better-sqlite3` or `sql.js`)

## Requirements

### Must-Have (Gate Checks)

- [ ] `CLAUDE.md` exists in the project root with meaningful content (not just a template)
- [ ] CLAUDE.md contains at least 3 distinct sections of QA standards
- [ ] `.claude/rules/` directory exists with at least 1 `.md` rule file
- [ ] Test case API routes exist and respond to HTTP requests (GET, POST minimum)
- [ ] A React page renders that displays test cases
- [ ] Test case data model includes severity field with defined levels

### Should-Have (Bonus Points)

- [ ] Path-specific rules exist for both `server/` and `client/` directories
- [ ] ISTQB severity levels are defined in CLAUDE.md and used in the data model (critical, major, minor, trivial)
- [ ] Full CRUD operations work (create, read, update, delete)
- [ ] API responses follow a standard envelope format defined in your CLAUDE.md
- [ ] The `@import` syntax is used to reference external documentation
- [ ] Test case form includes validation based on your defined standards

## Rules

1. **Define standards FIRST, build features SECOND.** Spend the first 45 minutes on CLAUDE.md and rules. Only then ask Claude to build the test case feature. This order matters because you want to verify that Claude follows your standards when generating code.

2. **Make your standards specific, not generic.** "Use good naming" is useless. "All API route handlers must be named `handleVerbNoun` (e.g., `handleCreateTestCase`, `handleListTestCases`)" is specific and verifiable.

3. **Verify compliance.** After Claude generates the test case feature, inspect the code. Does it follow your naming conventions? Does the API response format match what you specified? If not, point out the deviation and ask Claude to fix it.

4. **Use QA domain vocabulary.** Your CLAUDE.md should read like a QA team's engineering standards document, not a generic Node.js style guide. Reference ISTQB concepts: severity vs priority, test case vs test scenario, preconditions, expected results.

## Hints (Not Solutions)

### Writing Your CLAUDE.md

- Start by asking Claude to help you initialize the project memory with `/init`. Then edit the result to add your specific QA standards.
- Think about what you would put in a team wiki page titled "Engineering Standards for QA Tools." That content belongs in CLAUDE.md.
- Be prescriptive about your data model. If you define what fields a test case must have in CLAUDE.md, Claude will use exactly those fields when it builds the feature later. This is the power of memory.
- Consider defining your API response format explicitly. When every endpoint returns the same envelope, the frontend becomes predictable.

### Creating Path-Specific Rules

- Server-side rules might cover: error handling patterns, middleware conventions, database access patterns, logging requirements.
- Client-side rules might cover: component file structure, state management approach, styling methodology, accessibility requirements.
- Think about what mistakes a code generator commonly makes in each area and write rules to prevent them.

### Building Test Case CRUD

- Describe your requirements in terms of the QA domain, not in terms of code. Instead of asking for "a REST API with Express routes," describe the test case management workflow you need.
- Reference your CLAUDE.md standards when asking Claude to build features. Remind it that your standards define the data model and conventions.
- If the generated code does not follow your standards, do not just fix it manually. Point out the specific deviation to Claude and ask it to regenerate. This tests whether your memory is working.

### Common Pitfalls

- A CLAUDE.md with only 2-3 lines will not pass the gate. Write substantive standards that would actually guide an engineer.
- Forgetting to create `.claude/rules/` -- this directory does not exist by default. Ask Claude to create it with appropriate rule files.
- Building the feature before defining standards defeats the purpose. The goal is to see Claude apply YOUR rules, not its defaults.

## Verification

Before running `./bootcamp complete-session 2`, verify:

1. **CLAUDE.md exists and is substantive**: Open it and confirm it has real QA standards, not placeholder text
2. **Rules directory**: Confirm `.claude/rules/` has at least one `.md` file
3. **API works**: Use `curl` or the browser to hit your test case endpoints
4. **React page renders**: Navigate to the test case page and see the list
5. **Standards are followed**: Spot-check the generated code -- does it follow your naming conventions, response format, and data model?

```bash
./bootcamp complete-session 2
```

## What Comes Next

In Session 3, you will create reusable skills that leverage the standards you just defined. Your `/generate-test-suite` skill will use the test case data model from this session, and your `/qa-review` skill will check code against the standards in your CLAUDE.md.
