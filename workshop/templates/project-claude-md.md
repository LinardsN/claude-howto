# QA Command Center — Project Standards

<!-- This is a TEMPLATE for the CLAUDE.md students create in Session 2 -->
<!-- Students should customize this with their own QA standards -->

## Project Overview

QA Command Center is a test management dashboard built with Express + React (Vite) + SQLite.

## Tech Stack

- **Backend**: Node.js + Express
- **Frontend**: React (via Vite)
- **Database**: SQLite
- **Package Manager**: npm

## Coding Standards

### API Response Format

All API endpoints return consistent JSON:

```json
{
  "success": true,
  "data": { ... },
  "error": null
}
```

Error responses:

```json
{
  "success": false,
  "data": null,
  "error": { "code": "NOT_FOUND", "message": "Test case not found" }
}
```

### Naming Conventions

- **Files**: kebab-case (`test-case-routes.js`, `bug-tracker.jsx`)
- **React Components**: PascalCase (`TestCaseList.jsx`, `BugForm.jsx`)
- **API Routes**: `/api/v1/<resource>` (RESTful, plural nouns)
- **Database Tables**: snake_case, plural (`test_cases`, `bug_reports`)
- **Variables**: camelCase

### QA Domain Standards (ISTQB)

#### Severity Levels

| Level | Code | Description |
|-------|------|-------------|
| Critical | S1 | System crash, data loss, security breach |
| Major | S2 | Major feature broken, no workaround |
| Minor | S3 | Feature partially broken, workaround exists |
| Trivial | S4 | Cosmetic issue, typo, UI inconsistency |

#### Priority Levels

| Level | Code | Description |
|-------|------|-------------|
| Urgent | P1 | Fix immediately |
| High | P2 | Fix in current sprint |
| Medium | P3 | Fix in next sprint |
| Low | P4 | Fix when convenient |

#### Test Case Fields

Every test case must include:

- **ID**: Auto-generated (TC-XXXX format)
- **Title**: Concise, action-oriented
- **Description**: What is being tested and why
- **Preconditions**: Required state before execution
- **Steps**: Numbered list of actions
- **Expected Result**: What should happen
- **Severity**: S1-S4
- **Priority**: P1-P4
- **Status**: Draft, Ready, In Progress, Pass, Fail, Blocked

### File Organization

```text
server/
  models/          # Database models
  routes/          # Express route handlers
  middleware/      # Express middleware
  db.js            # Database connection

client/
  src/
    components/    # Reusable UI components
    pages/         # Page-level components
    App.jsx        # Root component
    main.jsx       # Entry point
```

## Git Conventions

- Commit format: `feat(scope): description` or `fix(scope): description`
- Branch naming: `feature/<name>`, `fix/<name>`
- Always commit working code
