# Session 9 Deliverables: Power User Mode

## Acceptance Criteria Checklist

### Must-Have (Required to Pass Gate)

- [ ] **CSV import**: An API endpoint and UI that accepts a CSV file upload and inserts valid test case records into the database
- [ ] **CSV export**: An API endpoint and UI that downloads test cases as a CSV file with appropriate headers
- [ ] **Settings page**: A dedicated React page at its own route with at least three configurable preferences
- [ ] **Settings persistence**: Preferences save to the database (or equivalent persistent storage) and reload correctly after page refresh
- [ ] **Component count**: At least 8 distinct React components exist across all pages in the project

### Should-Have (Bonus Points)

- [ ] **Planning mode evidence**: Conversation history or git commits show that `/plan` was used to design the CSV feature before coding
- [ ] **CSV validation**: Import validates data against project standards (severity levels, required fields) and reports invalid rows
- [ ] **Error reporting UI**: Import interface displays which rows failed and why, rather than silently dropping them
- [ ] **Permission mode exploration**: Evidence of switching between at least 2 permission modes during the session
- [ ] **Functional settings**: At least one preference (e.g., default severity) has a visible effect elsewhere in the app

### Jira Artifacts

- [ ] **Epics created**: "CSV Import/Export" and "Settings" (or combined) epics in Jira
- [ ] **Stories from plan**: Stories that map to `/plan` output steps with acceptance criteria
- [ ] **Status updated**: Completed work reflected in Jira ticket status

---

## File Inventory

After completing this session, your project should include:

| File | Description |
|------|-------------|
| `src/pages/Settings.jsx` (or `.tsx`) | Settings page component |
| `src/pages/ImportExport.jsx` (or similar) | CSV import/export UI |
| `src/components/CsvUpload.jsx` (or similar) | File upload component |
| `src/api/routes/settings.js` (or `.ts`) | Settings CRUD API |
| `src/api/routes/import-export.js` (or similar) | CSV import/export API endpoints |
| Database migration or schema update | Settings table and any CSV-related changes |

File names and paths will vary based on your project structure.

---

## Component Count Verification

The gate checks for at least 8 distinct React components. Here is what typically
accumulates across sessions 1-9:

| Session | Typical Components |
|---------|-------------------|
| S2 | TestCaseList, TestCaseForm, TestCaseDetail |
| S4 | BugList, BugForm, BugDetail |
| S6 | Dashboard, MetricsCard, RunsTable |
| S7 | ReportsList, ReportDetail, ReportExport |
| S8 | TrendChart, (chart wrapper components) |
| S9 | Settings, CsvUpload, CsvExport, ImportResults |

If you have fewer than 8 components, consider whether you have been combining
too much logic into single components. This is a good time to refactor.

---

## Gate Command

```bash
./bootcamp complete-session 9
```

The gate validator checks:

1. CSV import endpoint exists and accepts file upload
2. CSV export endpoint exists and returns CSV content
3. Settings page component exists with form inputs
4. Settings API has GET and PUT/POST endpoints
5. At least 8 React component files exist in the project
6. Settings data persists (database table or equivalent exists)
