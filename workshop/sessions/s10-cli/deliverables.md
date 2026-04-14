# Session 10 Deliverables: Ship It

## Acceptance Criteria Checklist

### Must-Have (Required to Pass Gate)

- [ ] **CI pipeline**: `.github/workflows/` contains at least one YAML file with valid GitHub Actions syntax
- [ ] **Navigation**: App has a persistent sidebar or navbar with links to all major pages (Dashboard, Test Cases, Bugs, Reports, Import/Export, Settings)
- [ ] **Client-side routing**: Page transitions happen without full browser reloads (React Router or equivalent)
- [ ] **Responsive layout**: App is usable at both 1280px and 768px browser widths (no horizontal overflow, navigation accessible)
- [ ] **App starts**: `npm run dev` (or `npm start`) launches the application without errors
- [ ] **Component count**: At least 8 distinct React component files exist in the project

### Should-Have (Bonus Points)

- [ ] **Batch script**: A shell script using `claude -p` for automated analysis, review, or documentation generation
- [ ] **CI references Claude/MCP**: At least one CI step uses Claude Code print mode or references MCP configuration from S5
- [ ] **Professional branding**: Consistent color scheme, typography, and spacing across all pages. TestDevLab or project-specific branding visible.
- [ ] **Error states**: UI displays user-friendly messages when API calls fail (not blank screens or raw error objects)
- [ ] **Loading states**: Skeleton screens, spinners, or placeholders shown while data loads
- [ ] **Empty states**: Helpful messages shown when lists have no data
- [ ] **Start script configured**: `package.json` has a `dev` or `start` script that launches the full app

### Jira Artifacts

- [ ] **Open epics closed**: All epics from S5-S9 are marked Done (or have clear status)
- [ ] **Final epic created**: "Ship It" epic with stories for CI, navigation, polish
- [ ] **Release notes**: Generated from Jira stories (ideally via `claude -p` batch script)

---

## File Inventory

After completing this session, your project should include:

| File | Description |
|------|-------------|
| `.github/workflows/ci.yml` (or similar) | GitHub Actions CI/CD pipeline |
| `scripts/batch-review.sh` (or similar) | Batch processing script using `claude -p` |
| `src/components/Navigation.jsx` (or `.tsx`) | Navigation sidebar or navbar component |
| `src/App.jsx` (or `.tsx`) | Updated with routing and navigation layout |
| Updated page components | All pages integrated into the navigation structure |
| Updated styles | Consistent branding and responsive design |

File names and paths will vary based on your project structure.

---

## Full Application Page Inventory

By Session 10, your QA Command Center should have these pages accessible via navigation:

| Page | Built In | Route |
|------|----------|-------|
| Dashboard | S6 (enhanced S8) | `/dashboard` |
| Test Cases | S2 | `/test-cases` |
| Bug Tracker | S4 | `/bugs` |
| Test Reports | S7 | `/reports` |
| Import/Export | S9 | `/import-export` |
| Settings | S9 | `/settings` |

Additional pages are welcome. The gate checks that navigation links exist
for at least 4 distinct pages.

---

## CI Pipeline Requirements

The gate validator parses your workflow YAML and checks for:

1. **Trigger**: workflow runs on push and/or pull_request
2. **Node setup**: `actions/setup-node` or equivalent
3. **Install**: `npm ci` or `npm install` step
4. **Lint**: a step that runs a linter (eslint, or similar)
5. **Build**: a step that runs `npm run build` or equivalent

At minimum, the pipeline must have install + build steps. Full marks require
lint + build + at least one additional check (tests, audit, or Claude review).

---

## Gate Command

```bash
./bootcamp complete-session 10
```

The gate validator checks:

1. `.github/workflows/` directory exists with at least one `.yml` file
2. Workflow YAML has valid syntax and includes build-related steps
3. Navigation component exists with route links
4. App component includes routing configuration
5. `package.json` has a `dev` or `start` script
6. At least 8 React component files exist
7. Layout handles 768px width (CSS media queries or responsive framework detected)

---

## After Session 10

Session 10 completion unlocks the **Final Task** -- an independent, graded
feature build worth 25% of your total score.

See [final-task.md](final-task.md) for the complete specification.
