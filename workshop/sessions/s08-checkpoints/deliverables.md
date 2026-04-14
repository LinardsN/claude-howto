# Session 8 Deliverables: Experiment Fearlessly

## Acceptance Criteria Checklist

### Must-Have (Required to Pass Gate)

- [ ] **Charts render**: Dashboard displays at least two chart visualizations that show data
- [ ] **Chart library installed**: `package.json` lists a chart library (Recharts, Chart.js, Nivo, Victory, or equivalent) as a dependency
- [ ] **Experimentation evidence**: Git history contains evidence that multiple approaches were tried (commit messages, branches, or library change history)
- [ ] **Dashboard functional**: Dashboard page loads without JavaScript errors and displays charts alongside the metrics cards from S6

### Should-Have (Bonus Points)

- [ ] **Multiple chart types**: At least two different visualization types used (e.g., line + bar, area + pie)
- [ ] **Cohesive layout**: Dashboard has intentional information hierarchy -- metrics at top, trends in middle, details at bottom (or equivalent thoughtful arrangement)
- [ ] **Theme variant explored**: Evidence of trying a dark theme, alternate color scheme, or significantly different layout
- [ ] **Live data in charts**: Charts pull data from your Express API endpoints, not from hardcoded arrays in the component

### Jira Artifacts

- [ ] **Decision record**: Jira comment or task documenting which libraries/layouts you compared and why you chose the winner
- [ ] **Status updated**: Dashboard stories reflect completed work

---

## File Inventory

After completing this session, your project should include new or modified files:

| File | Description |
|------|-------------|
| `package.json` | Updated with chart library dependency |
| `src/pages/Dashboard.jsx` (or `.tsx`) | Enhanced with chart components |
| `src/components/charts/` (or similar) | Chart wrapper components |
| `src/api/routes/dashboard.js` (or `.ts`) | Time-series data endpoints for charts |
| Git history | Commits showing experimentation |

File names and paths will vary based on your project structure.

---

## What "Experimentation Evidence" Means

The gate validator examines your git history for signs that you actually used
checkpoints to compare approaches. Specifically it looks for:

1. **Multiple library installs**: `package.json` or `package-lock.json` diffs showing different chart libraries at different points in history
2. **Comparative commit messages**: messages containing words like "try", "compare", "experiment", "rewind", "approach", or "A/B"
3. **Branch evidence**: branches or stashes from checkpoint saves
4. **Revert patterns**: commits that add then remove or replace a dependency

A single "add charts" commit with no experimentation trail will be flagged.

---

## Gate Command

```bash
./bootcamp complete-session 8
```

The gate validator checks:

1. `package.json` includes a chart library dependency
2. Dashboard page component contains chart-related imports
3. At least two chart visualizations exist in the dashboard
4. Git log shows evidence of experimentation (multiple approaches)
5. Dashboard API serves time-series data for charts
