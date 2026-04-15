# Jira Epic Template

<!-- TEMPLATE: Use this as a reference for creating well-structured Jira epics -->
<!-- Ask Claude Code to create your epics via Atlassian MCP — describe what you need -->

## Epic Structure

### Title

`[Feature Area] - Brief Description`

Example: `Test Case Management - CRUD Operations and React UI`

### Description

#### Summary

One paragraph describing the feature area and its business value.

#### Scope

- What is included in this epic
- What is explicitly out of scope

#### Acceptance Criteria

- [ ] Criterion 1: Specific, measurable outcome
- [ ] Criterion 2: Specific, measurable outcome
- [ ] Criterion 3: Specific, measurable outcome

#### Technical Notes

- Key architectural decisions
- Dependencies on other epics
- Known risks or constraints

### Linked Stories

Each epic should contain 3-8 stories that break down the work:

| Story | Points | Priority |
|-------|--------|----------|
| Story title 1 | 3 | High |
| Story title 2 | 5 | Medium |
| Story title 3 | 2 | Low |

## Example Epic for QA Command Center

**Title**: Bug Tracker Module - Full CRUD with GitHub Integration

**Description**: Build a complete bug tracking module that allows QA engineers
to create, view, edit, and close bugs with severity/priority classification.
Includes GitHub issue sync via MCP integration.

**Acceptance Criteria**:

- [ ] Bug form captures: title, description, steps to reproduce, severity, priority
- [ ] Bug list page with filtering by severity and status
- [ ] "Create GitHub Issue" button syncs to configured repository
- [ ] Bug status workflow: Open -> In Progress -> Resolved -> Closed
