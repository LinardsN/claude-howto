# Session 6 Deliverables: Automated Quality Gates

## Acceptance Criteria Checklist

### Must-Have (Required to Pass Gate)

- [ ] **Hook configuration exists**: `.claude/settings.json` contains a `hooks` key with at least one event and one hook definition
- [ ] **Hook script exists**: At least one executable script in `.claude/hooks/` (or equivalent project hook directory)
- [ ] **Dashboard route**: A React page accessible at a dedicated URL path (e.g., `/dashboard`)
- [ ] **Metrics display**: Dashboard shows at least three computed metrics (e.g., total tests, pass rate, open bugs)
- [ ] **Recent runs table**: Dashboard includes a table with columns for date, suite name, and pass/fail counts

### Should-Have (Bonus Points)

- [ ] **Multiple hook events**: Configuration includes hooks for at least two different event types (e.g., PreToolUse + PostToolUse, or PreToolUse + Stop)
- [ ] **Three hook event types**: All three events covered -- PreToolUse, PostToolUse, and Stop
- [ ] **Progressive dependency**: At least one hook enforces a standard defined in your Session 2 CLAUDE.md (naming conventions, severity levels, or code style rules)
- [ ] **Live data**: Dashboard metrics are computed from database queries, not hardcoded values
- [ ] **Real linting**: PostToolUse hook executes an actual linter (ESLint, Prettier, or equivalent) and reports results

### Jira Artifacts

- [ ] **Epic created**: "Quality Gates" (or similar) epic exists in your Jira project
- [ ] **Stories written**: At least three stories with acceptance criteria covering hooks and dashboard
- [ ] **Status updated**: Completed stories are moved to Done

---

## File Inventory

After completing this session, your project should include these new or modified files:

| File | Description |
|------|-------------|
| `.claude/settings.json` | Hook configuration with event-to-hook mappings |
| `.claude/hooks/validate-filename.sh` | PreToolUse:Write hook for file naming validation |
| `.claude/hooks/auto-lint.sh` | PostToolUse:Write hook for automatic linting |
| `src/pages/Dashboard.jsx` (or `.tsx`) | React dashboard page component |
| `src/api/routes/dashboard.js` (or `.ts`) | API endpoint serving dashboard metrics |
| Database migration or seed | Test run data for dashboard display |

File names and paths will vary based on your project structure and the
conventions you established in your CLAUDE.md.

---

## Gate Command

```bash
./bootcamp complete-session 6
```

The gate validator checks:

1. `.claude/settings.json` is valid JSON with a `hooks` section
2. At least one hook script file exists and is referenced in settings
3. A dashboard page component exists in your React source
4. The Express API has a dashboard-related route
5. Progressive dependency: hook rules reference CLAUDE.md standards from Session 2
