# Session 4 Deliverables: Specialized QA Agents

Checklist of exact deliverables with acceptance criteria.

## Must-Have Deliverables

### D1: Agent Directory

- [ ] `.claude/agents/` directory exists
- [ ] At least 2 `.md` files exist in `.claude/agents/`
- [ ] Each agent file has valid YAML frontmatter with `---` delimiters

### D2: Agent Frontmatter

- [ ] Each agent has a `description` field in frontmatter
- [ ] At least one agent has a `tools` field restricting its tool access
- [ ] Agent files have meaningful body content (system prompt, not empty)

### D3: Bug Tracker API

- [ ] Bug-related API route file exists
- [ ] GET endpoint returns a list of bugs
- [ ] POST endpoint accepts and creates a new bug

### D4: Bug Report Form

- [ ] React component for bug report submission exists
- [ ] Form includes fields for at minimum: summary, severity, description

### D5: Bug List Page

- [ ] React component for bug listing exists
- [ ] Page renders without errors when dev server is running

## Should-Have Deliverables (Bonus)

### D6: Three Specialized Agents

- [ ] Test writer agent exists with full tool access
- [ ] Bug triager agent exists with appropriate tool restrictions
- [ ] Security scanner agent restricted to `Read`, `Grep`, `Glob` only

### D7: Agent-Skill Integration

- [ ] At least one agent references a Session 3 skill in its system prompt
- [ ] Agent system prompt references CLAUDE.md standards

### D8: Severity Filtering

- [ ] Bug list page supports filtering by severity level
- [ ] Filter options match ISTQB severity levels from CLAUDE.md

### D9: Bug Data Model Quality

- [ ] Bug model includes: summary, description, severity, priority, status
- [ ] Status field supports defect lifecycle: open, in-progress, resolved, closed
- [ ] Reproduction steps field exists
- [ ] Actual vs expected behavior fields exist

### D10: Agents Discoverable

- [ ] `/agents` command in Claude Code REPL lists custom agents
- [ ] Agent descriptions are clear and specific

## Acceptance Criteria Summary

| ID | Deliverable | Validation Method |
|----|-------------|-------------------|
| D1 | Agent directory | Directory and file existence |
| D2 | Agent frontmatter | YAML parse + field check |
| D3 | Bug tracker API | HTTP request validation |
| D4 | Bug report form | Component file existence |
| D5 | Bug list page | Component existence + render check |
| D6 | Three agents | File count + tool field inspection |
| D7 | Agent-skill integration | Content pattern matching |
| D8 | Severity filtering | UI component inspection |
| D9 | Data model quality | Schema/field inspection |
| D10 | Agent discovery | `/agents` output check |

## Gate Command

```bash
./bootcamp complete-session 4
```

You must pass all Must-Have deliverables (D1-D5) to unlock Session 5.
