# Session 3 Deliverables: Reusable QA Workflows

Checklist of exact deliverables with acceptance criteria.

## Must-Have Deliverables

### D1: Generate-Test-Suite Skill

- [ ] `.claude/skills/generate-test-suite/SKILL.md` exists (or equivalent path)
- [ ] Frontmatter includes `name` field
- [ ] Frontmatter includes `description` field with meaningful content
- [ ] SKILL.md body contains instructions for generating test suites (not empty)

### D2: QA-Review Skill

- [ ] `.claude/skills/qa-review/SKILL.md` exists (or equivalent path)
- [ ] Frontmatter includes `name` field
- [ ] Frontmatter includes `description` field with meaningful content
- [ ] SKILL.md body contains QA review instructions (not empty)

### D3: Test Suite Page

- [ ] A React component for test suite listing exists in the client source
- [ ] The page renders without errors when the dev server is running
- [ ] The page is navigable from the application (route or link exists)

## Should-Have Deliverables (Bonus)

### D4: Supporting Files

- [ ] At least one skill has a `templates/` subdirectory with template files
- [ ] Templates are referenced from the SKILL.md body

### D5: Auto-Invocation

- [ ] Natural language input triggers the appropriate skill
- [ ] Skill descriptions contain domain-specific keywords for matching

### D6: Context Fork

- [ ] `/qa-review` skill includes `context: fork` in frontmatter or instructions
- [ ] Skill executes in isolated context without polluting main conversation

### D7: ISTQB Test Design Techniques

- [ ] Generate-test-suite skill references at least 2 ISTQB techniques by name
- [ ] Techniques include: boundary value analysis, equivalence partitioning, decision tables, or state transition testing

### D8: Test Suite Data Model

- [ ] Test suite model exists with fields: name, feature/module, status, creation date
- [ ] Test suite has a relationship to test cases (from Session 2)
- [ ] API routes exist for test suite CRUD operations

### D9: Status Badges

- [ ] Test suite page displays status indicators (pass/fail/pending or similar)
- [ ] Statuses are visually distinct (color-coded or badged)

## Acceptance Criteria Summary

| ID | Deliverable | Validation Method |
|----|-------------|-------------------|
| D1 | Generate-test-suite skill | File existence + YAML parse + body check |
| D2 | QA-review skill | File existence + YAML parse + body check |
| D3 | Test suite page | Component file existence + render check |
| D4 | Supporting files | Directory and file existence |
| D5 | Auto-invocation | Description field quality check |
| D6 | Context fork | Frontmatter field check |
| D7 | ISTQB techniques | Content pattern matching |
| D8 | Test suite model | File and route existence |
| D9 | Status badges | Component content inspection |

## Gate Command

```bash
./bootcamp complete-session 3
```

You must pass all Must-Have deliverables (D1-D3) to unlock Session 4.
