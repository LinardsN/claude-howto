# Session 7 Deliverables: Packaging It All Together

## Acceptance Criteria Checklist

### Must-Have (Required to Pass Gate)

- [ ] **Plugin manifest exists**: `.claude-plugin/plugin.json` is present and valid JSON
- [ ] **Skills bundled (S3)**: Manifest references at least one skill file from Session 3, and the file exists
- [ ] **Agents bundled (S4)**: Manifest references at least one agent definition from Session 4, and the file exists
- [ ] **Hooks bundled (S6)**: Manifest references at least one hook from Session 6, and the script/prompt exists
- [ ] **All paths valid**: Every file path in the manifest resolves to an existing file
- [ ] **Reports page**: A React component renders at a dedicated route (e.g., `/reports`)

### Should-Have (Bonus Points)

- [ ] **Commands bundled (S1)**: Manifest also references slash commands from Session 1 (four sessions bundled)
- [ ] **Plugin README**: `.claude-plugin/README.md` explains installation and usage
- [ ] **HTML report export**: Reports page has a download button that produces a self-contained HTML file
- [ ] **Self-contained HTML**: Downloaded report renders correctly when opened directly in a browser (no external dependencies)
- [ ] **Manifest metadata**: `plugin.json` includes `version`, `author`, and `description` fields

### Progressive Dependency Verification

This session is the major integration checkpoint. The gate validator specifically checks:

| Dependency | What the Gate Checks |
|------------|---------------------|
| S3 Skills | At least one `.md` skill file referenced in `plugin.json` exists and contains skill instructions |
| S4 Agents | At least one agent definition referenced in `plugin.json` exists and contains agent configuration |
| S6 Hooks | At least one hook script or prompt referenced in `plugin.json` exists and is functional |
| S1 Commands (bonus) | Slash command files referenced in `plugin.json` exist |

### Jira Artifacts

- [ ] **Epic created**: "Plugin Packaging" (or similar) epic in Jira
- [ ] **Stories written**: At least three stories covering manifest, bundling, and reports
- [ ] **Status updated**: Completed stories moved to Done

---

## File Inventory

After completing this session, your project should include:

| File | Description |
|------|-------------|
| `.claude-plugin/plugin.json` | Plugin manifest with all component references |
| `.claude-plugin/README.md` | Plugin documentation (recommended) |
| `.claude-plugin/commands/` | Copied or symlinked slash command files from S1 |
| `.claude-plugin/skills/` | Copied or symlinked skill files from S3 |
| `.claude-plugin/agents/` | Copied or symlinked agent definitions from S4 |
| `.claude-plugin/hooks/` | Copied or symlinked hook scripts from S6 |
| `src/pages/Reports.jsx` (or `.tsx`) | React test reports page |
| `src/api/routes/reports.js` (or `.ts`) | API endpoint for report data and HTML export |

File names and paths will vary based on your project structure.

---

## Gate Command

```bash
./bootcamp complete-session 7
```

The gate validator checks:

1. `.claude-plugin/plugin.json` is valid JSON with required fields
2. Skills section references at least one file that exists (S3 dependency)
3. Agents section references at least one file that exists (S4 dependency)
4. Hooks section references at least one script/prompt that exists (S6 dependency)
5. Reports page component exists in React source
6. No broken file references in the manifest
