# Session 2 Deliverables: Teaching Claude Your Standards

Checklist of exact deliverables with acceptance criteria.

## Must-Have Deliverables

### D1: CLAUDE.md File

- [ ] `CLAUDE.md` exists in the project root
- [ ] File contains at least 3 distinct sections (e.g., Tech Stack, Naming Conventions, QA Standards)
- [ ] File contains at least 30 lines of meaningful content (not just headers)
- [ ] QA-specific terminology is present (severity, priority, test case, or similar)

### D2: Rules Directory

- [ ] `.claude/rules/` directory exists
- [ ] At least 1 `.md` file exists in `.claude/rules/`
- [ ] Rule file contains meaningful content (not empty or placeholder)

### D3: Test Case API

- [ ] At least one API route file exists for test cases
- [ ] GET endpoint returns a list of test cases (HTTP 200)
- [ ] POST endpoint accepts and creates a new test case

### D4: Test Case Data Model

- [ ] Test case model includes a `severity` field
- [ ] Severity has defined levels (e.g., critical, major, minor, trivial)

### D5: Test Case React Page

- [ ] A React page/component exists for test case display
- [ ] The page renders without errors when the dev server is running

## Should-Have Deliverables (Bonus)

### D6: Path-Specific Rules

- [ ] Separate rule file for `server/` code conventions
- [ ] Separate rule file for `client/` code conventions

### D7: ISTQB Alignment

- [ ] CLAUDE.md defines ISTQB severity levels (critical, major, minor, trivial)
- [ ] Data model uses these exact severity levels

### D8: Full CRUD

- [ ] GET endpoint for listing all test cases
- [ ] GET endpoint for a single test case by ID
- [ ] POST endpoint for creating a test case
- [ ] PUT/PATCH endpoint for updating a test case
- [ ] DELETE endpoint for removing a test case

### D9: API Response Envelope

- [ ] API responses follow a standard format defined in CLAUDE.md
- [ ] Format includes at minimum: success indicator and data payload

### D10: Standards Compliance

- [ ] Generated code follows the naming conventions defined in CLAUDE.md
- [ ] API response format matches what CLAUDE.md specifies
- [ ] Data model fields match what CLAUDE.md defines

## Acceptance Criteria Summary

| ID | Deliverable | Validation Method |
|----|-------------|-------------------|
| D1 | CLAUDE.md | File existence + content analysis |
| D2 | Rules directory | Directory and file existence |
| D3 | Test case API | HTTP request validation |
| D4 | Data model | Schema/content inspection |
| D5 | React page | Component file existence |
| D6 | Path-specific rules | File existence per path |
| D7 | ISTQB alignment | Content pattern matching |
| D8 | Full CRUD | HTTP endpoint validation |
| D9 | Response envelope | API response format check |
| D10 | Standards compliance | Code pattern matching vs CLAUDE.md |

## Gate Command

```bash
./bootcamp complete-session 2
```

You must pass all Must-Have deliverables (D1-D5) to unlock Session 3.
