# Session 9 Reference: Advanced Features

Quick reference for planning mode, permission modes, and extended thinking.
See [09-advanced-features](../../09-advanced-features/README.md) for the full
tutorial.

---

## /plan Command

### Starting a Plan

Type `/plan` followed by your feature description. Claude will produce a
structured implementation plan without writing any code.

```text
/plan Build a CSV import feature for test cases that validates data against
our CLAUDE.md standards, handles errors gracefully, and provides a React
upload UI with progress feedback.
```

### Plan Review Flow

```text
1. You send /plan with feature description
2. Claude produces a numbered plan with steps, considerations, and risks
3. You review the plan:
   ├── "Looks good, proceed" → Claude starts executing step by step
   ├── "Modify step 3 to..." → Claude adjusts the plan
   ├── "Add a step for..." → Claude inserts a new step
   └── "I disagree with..." → Claude explains reasoning or adjusts
4. Once approved, Claude executes the plan sequentially
```

### What a Good Plan Includes

- **Steps**: numbered, sequential actions Claude will take
- **File changes**: which files will be created or modified
- **Data model**: schema changes or new tables/collections
- **Dependencies**: libraries to install, APIs to call
- **Edge cases**: how to handle error conditions
- **Testing**: how to verify each step works

---

## Permission Modes

### Overview

| Mode | File Edits | Commands | Permission Checks | Use Case |
|------|-----------|----------|-------------------|----------|
| `plan` | Blocked | Blocked | N/A | Planning only, no execution |
| `auto` | Approved automatically | Approved automatically | Active | Trusted execution of approved plans |
| `autoEdit` | Approved automatically | Requires approval | Active | File changes OK, review commands |
| `fullAuto` | Approved automatically | Approved automatically | Skipped | Maximum speed, trusted environment |
| `bypassPermissions` | Approved automatically | Approved automatically | Bypassed | Emergency/development only |

### Switching Modes

Press `Shift+Tab` to cycle through available permission modes. The current
mode is displayed in the Claude Code interface.

```text
Shift+Tab → plan → auto → autoEdit → fullAuto → (cycle)
```

### When to Use Each Mode

- **plan**: When designing a feature. You want Claude to think without
  acting. Good for the beginning of a complex task.
- **autoEdit**: When you trust Claude's file edits but want to review
  shell commands (npm install, database migrations, etc.). A good
  default for development work.
- **auto**: When executing an approved plan. Claude has already shown you
  what it will do; now let it work efficiently.
- **fullAuto**: When you are doing repetitive tasks (formatting, renaming,
  simple refactors) and do not want approval prompts slowing you down.
- **bypassPermissions**: Rarely needed. Only use when permission checks
  are actively blocking something you have verified is safe.

---

## Extended Thinking

Extended thinking gives Claude a dedicated reasoning phase before it
responds. This is especially useful for:

- **Architecture decisions**: choosing between implementation approaches
- **Complex data models**: designing schemas with relationships and constraints
- **Edge case analysis**: thinking through what could go wrong
- **Multi-step plans**: reasoning about step ordering and dependencies

Extended thinking activates automatically when Claude detects a complex
problem. You can encourage it by asking questions that require analysis:

```text
"Think through the implications of adding CSV import. What edge cases
should we handle? What validation rules apply?"
```

---

## CSV Feature Design Patterns

Common patterns to consider when planning CSV import/export:

### Import Pipeline

```text
File Upload → Parse CSV → Validate Headers → Validate Rows → Map to Model → Insert Records → Report Results
```

### Validation Layers

| Layer | What It Checks | Example |
|-------|---------------|---------|
| Structure | CSV is well-formed, correct number of columns | Missing comma, unclosed quote |
| Headers | Required columns present, names match expected | "Severity" not "Priority" |
| Types | Values match expected data types | Date fields contain valid dates |
| Domain | Values match your QA standards | Severity is Critical/High/Medium/Low |
| Uniqueness | No duplicate records | Test case ID already exists |

### Export Options

| Option | Description |
|--------|-------------|
| All records | Export every test case in the database |
| By status | Export only Active, or only Deprecated |
| By suite | Export test cases belonging to a specific suite |
| By date range | Export cases created or modified within a range |

---

## Settings Data Model

A simple key-value pattern works well for settings:

```text
settings table:
  key (TEXT, PRIMARY KEY)
  value (TEXT)
  updated_at (DATETIME)
```

Common settings for a QA app:

| Key | Default Value | Used By |
|-----|---------------|---------|
| `default_severity` | `Medium` | Test case creation form |
| `project_name` | `QA Command Center` | Page headers, report titles |
| `test_id_prefix` | `TC-` | Auto-generated test case IDs |
| `items_per_page` | `25` | List views (test cases, bugs) |
| `default_view` | `list` | Test case listing (list vs grid) |
| `theme` | `light` | App-wide theme |

---

## Shift+Tab Workflow

```text
Start of session:
  Mode: autoEdit (safe default)

Planning phase (/plan):
  Shift+Tab → plan mode
  "Plan the CSV import feature"
  Review and modify the plan

Execution phase:
  Shift+Tab → auto mode
  "Execute the plan"
  Claude works through steps without interruption

Testing phase:
  Shift+Tab → autoEdit mode
  "Run the tests"
  Claude edits test files freely, asks before running test commands
```
