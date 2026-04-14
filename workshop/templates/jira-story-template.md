# Jira Story Template

<!-- TEMPLATE: Use this as a reference for creating well-described Jira stories -->
<!-- Ask Claude Code to create stories via Atlassian MCP -->

## Story Structure

### Title

`As a [role], I want [action] so that [benefit]`

Example: `As a QA engineer, I want to filter bugs by severity so that I can prioritize my testing`

### Description

#### Context

Why this story exists and what problem it solves.

#### Acceptance Criteria

```gherkin
Given [precondition]
When [action]
Then [expected result]
```

Example:

```gherkin
Given I am on the bug list page
When I select "Critical" from the severity filter
Then only bugs with severity S1 are displayed
And the count shows the filtered total
```

#### Technical Notes

- Implementation approach (if known)
- API endpoint design
- Database changes needed
- React component structure

### Story Points

| Points | Meaning |
|--------|---------|
| 1 | Trivial change, <1 hour |
| 2 | Small change, 1-2 hours |
| 3 | Medium change, 2-4 hours |
| 5 | Large change, half day |
| 8 | Complex change, full day |

### Labels

- `frontend` / `backend` / `fullstack`
- `bug-fix` / `feature` / `tech-debt`
- `session-N` (which bootcamp session)

### Links

- **Blocks**: stories that depend on this one
- **Is blocked by**: stories this depends on
- **Related to**: associated stories in same epic
