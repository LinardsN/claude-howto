# Session 9: Power User Mode -- Advanced Features

You have been using Claude Code as a conversational coding partner: describe
what you want, review what it produces, iterate. That workflow is effective
for incremental changes, but complex features -- the kind with multiple
interconnected components, validation rules, and edge cases -- benefit from
a more structured approach.

This session introduces three power-user capabilities that scale Claude Code
to harder problems. Planning mode lets you design a feature top-down before
generating any code. Permission modes let you control how much autonomy
Claude has. Extended thinking gives Claude more room to reason through
architectural decisions. Together, these tools let you tackle features that
would otherwise require multiple back-and-forth cycles to get right.

---

## Learning Objectives

- Use `/plan` to design a complex feature before writing any code
- Review, modify, and approve a plan before execution begins
- Understand the five permission modes and when each is appropriate
- Switch between permission modes using `Shift+Tab`
- Leverage extended thinking for better architectural decisions
- Build a multi-step feature (CSV import/export) from a structured plan

## Prerequisites

- Session 8 gate passed (`./bootcamp complete-session 8` green)
- Working QA Command Center with dashboard (with charts), test cases, bugs,
  reports, and plugin
- Atlassian MCP configured
- Comfort with your project's data model and API patterns

## Schedule

| Block | Duration | Activity |
|-------|----------|----------|
| 1 | 20 min | Planning mode: design CSV import/export feature via `/plan` |
| 2 | 20 min | Execute the plan: build CSV import/export |
| 3 | 15 min | Permission modes: explore and switch between modes |
| 4 | 20 min | Build settings page with user preferences |

**Total: 75 minutes**

---

## The Feature

**Advanced features** in Claude Code give you fine-grained control over how
Claude approaches complex tasks: structured planning, adjustable autonomy,
and deeper reasoning.

Read the full reference module: [09-advanced-features](../../09-advanced-features/README.md)

Key concepts you will use today:

- **/plan command**: Tells Claude to create a structured implementation plan
  without writing any code. You review the plan, suggest modifications, and
  approve it before Claude starts coding.
- **Plan review flow**: Claude presents a plan -> you review -> modify or
  approve -> Claude executes step by step
- **Five permission modes**: control how much Claude can do without asking
  - `plan` -- Claude only plans, never executes
  - `auto` -- Claude executes approved tool calls automatically
  - `autoEdit` -- Claude auto-edits files but asks before running commands
  - `fullAuto` -- Claude runs everything without asking
  - `bypassPermissions` -- like fullAuto but also bypasses permission checks
- **Shift+Tab**: quickly switch between permission modes during a session
- **Extended thinking**: Claude uses a dedicated reasoning process for
  complex problems, producing more thoughtful architecture and implementation

---

## What You Will Build

### CSV Import/Export (Designed via /plan)

A complete CSV workflow for test cases:

**Import**: Upload a CSV file of test cases. The system parses it, validates
the data against your standards (correct severity levels, required fields
present, valid test types), maps columns to your data model, and inserts
the records into your database. Invalid rows are reported with clear error
messages.

**Export**: Select test cases (all, filtered by status, or by suite) and
download them as a well-formatted CSV with headers matching your data model.
The export should include all fields a QA engineer would need to work with
the data in a spreadsheet.

This feature is complex enough to benefit from planning mode. Think about:
column mapping, data validation, error handling for malformed CSVs, partial
imports (some rows valid, some not), and how the UI should present upload
progress and validation errors.

### Settings Page

A new React page for user preferences:

- **Default severity**: which severity level is pre-selected when creating
  new test cases or bug reports
- **Project name**: displayed in headers and exported reports
- **Test ID prefix**: the string prepended to test case IDs (e.g., "TC-",
  "QA-", or your project abbreviation)
- **Other preferences**: any settings that make sense for your workflow
  (items per page, default view, theme selection)
- Settings persist to the database and load on app startup

---

## Requirements

### Must-Have (Gate Checks)

- [ ] **CSV import works**: Upload a CSV file and see test cases appear in the database
- [ ] **CSV export works**: Download test cases as a valid CSV file with headers
- [ ] **Settings page**: Dedicated route with at least three configurable preferences
- [ ] **Settings persist**: Preferences save to the database and reload correctly on page refresh
- [ ] **Component count**: Project has at least 8 distinct React components total across all pages

### Should-Have (Bonus Points)

- [ ] **Planning mode evidence**: Git history or conversation shows use of `/plan` for the CSV feature
- [ ] **CSV validation**: Import rejects or flags rows with invalid data (wrong severity, missing required fields)
- [ ] **Error reporting**: Import UI shows which rows failed validation and why
- [ ] **Multiple permission modes**: Evidence of exploring at least 2 different permission modes during the session
- [ ] **Settings affect behavior**: Changing a preference (e.g., default severity) actually changes the default value in test case creation

---

## Rules

1. **The CSV feature MUST be designed using /plan first.** Do not jump straight
   into coding. Start by asking Claude to plan the feature. Review the plan
   it produces. Modify steps you disagree with. Only approve and execute
   once you are satisfied with the approach. This is the core learning
   objective.

2. **Explore at least two permission modes.** Switch between modes using
   `Shift+Tab` at least once during the session. Notice how the interaction
   changes. You do not need to use `bypassPermissions` -- just experience
   the difference between modes like `auto` and `autoEdit`.

3. **CSV validation must use your standards.** If your CLAUDE.md defines
   severity levels as Critical/High/Medium/Low, the CSV import should reject
   rows with "Urgent" or "P1". If your data model requires a test type field,
   the import should flag rows missing it. Your standards drive the
   validation rules.

4. **Settings must be functional, not decorative.** A settings page that
   looks nice but does not actually change app behavior is incomplete. At
   least one preference must have a visible effect elsewhere in the app.

5. **All code is vibe-coded.** Claude Code generates the CSV parsing logic,
   the file upload handling, the settings CRUD, and the React components.
   Your job is to plan well and describe precisely.

---

## Hints (Not Solutions)

- When using `/plan`, be specific about what the feature needs. Include
  edge cases in your planning prompt: "What happens when the CSV has extra
  columns? What about duplicate test case IDs? What if the file is
  empty?" The more specific your planning request, the better the plan.

- After Claude presents a plan, do not just approve it immediately. Read
  each step. Are there missing steps? Would you reorder anything? The
  value of planning mode is the review phase.

- For CSV parsing, think about which library to use (or whether to parse
  manually). Consider: does the library handle quoted fields with commas
  inside them? Does it handle different line endings?

- The settings page is simpler than the CSV feature but still benefits from
  thinking about the data model: where do settings live? How do you load
  them on startup? What is the default value for a setting that has never
  been configured?

- `Shift+Tab` cycles through permission modes. Try `autoEdit` mode for the
  settings page (let Claude edit files freely but ask before running commands)
  and `auto` mode for the CSV feature (let Claude run the plan efficiently).

---

## Jira Integration

Using the Atlassian MCP:

1. **Create stories from your /plan output.** This is a natural mapping:
   each step in Claude's plan corresponds to a user story or task. The
   plan's details become acceptance criteria.
2. **Create a "CSV Import/Export" epic** with stories for:
   - CSV parsing and validation logic
   - Import API endpoint with error handling
   - Export API endpoint with filtering
   - Import UI with file upload and progress
   - Export UI with filter selection
3. **Create a "Settings" epic** with stories for:
   - Settings data model and API
   - Settings React page
   - Integration with existing features (e.g., default severity)
4. **Link related stories** and **update status** as you work

---

## Verification

Before running `./bootcamp complete-session 9`, self-check:

1. **CSV import test**: Create a small CSV file (5-10 rows) with valid test
   case data. Upload it through your app. Do the records appear in your
   test cases list?

2. **CSV validation test**: Create a CSV with intentional errors (invalid
   severity level, missing required field). Upload it. Does the app report
   which rows are invalid and why?

3. **CSV export test**: Export your test cases as CSV. Open the file in a
   text editor or spreadsheet. Are the headers correct? Is the data complete?
   Import the exported CSV back -- does it round-trip cleanly?

4. **Settings test**: Change the default severity to a non-default value.
   Navigate to test case creation. Is the new default pre-selected? Refresh
   the page -- is the setting still correct?

5. **Component count**: Count your distinct React components across all
   pages. You need at least 8. Check your `src/components/` and `src/pages/`
   directories.

```bash
# Validate your session deliverables
./bootcamp complete-session 9
```
