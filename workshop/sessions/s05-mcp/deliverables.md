# Session 5 Deliverables: Connecting to the QA Ecosystem

Checklist of exact deliverables with acceptance criteria.

## Must-Have Deliverables

### D1: MCP Configuration File

- [ ] `.mcp.json` exists in the project root
- [ ] File contains valid JSON
- [ ] `mcpServers` key exists in the configuration

### D2: GitHub MCP Server

- [ ] GitHub MCP server entry exists in `.mcp.json`
- [ ] Server has `command` and `args` fields configured
- [ ] Server has `env` field with token variable
- [ ] At least one successful GitHub MCP interaction (e.g., list issues)

### D3: Atlassian/Jira MCP Server

- [ ] Atlassian MCP server entry exists in `.mcp.json`
- [ ] Server has required environment variables (site URL, email, token)
- [ ] At least one successful Jira interaction

### D4: Test Run Executor Page

- [ ] React component for test run executor exists
- [ ] Page renders without errors when dev server is running
- [ ] Page is navigable from the application

## Should-Have Deliverables (Bonus)

### D5: Bug-to-Issue Sync

- [ ] "Create GitHub Issue" button or action exists in bug tracker UI
- [ ] Clicking/triggering it creates a real GitHub issue from a local bug
- [ ] GitHub issue contains bug summary and description

### D6: Jira Project Management

- [ ] A Jira project exists (created via Claude Code, not Jira UI)
- [ ] At least 1 epic exists in the Jira project
- [ ] At least 1 story exists under an epic with acceptance criteria

### D7: Test Run Executor Features

- [ ] Page displays a list of test suites available for execution
- [ ] Status tracking exists (pending/running/passed/failed)
- [ ] Status badges are visually distinct
- [ ] Test run results show pass/fail counts

### D8: Token Security

- [ ] API tokens are in environment variables, not hardcoded in source code
- [ ] `.mcp.json` uses env field for sensitive values

## Acceptance Criteria Summary

| ID | Deliverable | Validation Method |
|----|-------------|-------------------|
| D1 | MCP config file | File existence + JSON parse |
| D2 | GitHub MCP | Config entry + MCP tool response |
| D3 | Atlassian MCP | Config entry + MCP tool response |
| D4 | Test run executor | Component existence + render check |
| D5 | Bug-to-issue sync | UI element existence + GitHub issue check |
| D6 | Jira project | Jira API query for project/epic/story |
| D7 | Executor features | Component content inspection |
| D8 | Token security | Source code scan for hardcoded tokens |

## Gate Command

```bash
./bootcamp complete-session 5
```

You must pass all Must-Have deliverables (D1-D4) to unlock Session 6.
