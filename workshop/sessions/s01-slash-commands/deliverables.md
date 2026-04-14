# Session 1 Deliverables: First Contact

Checklist of exact deliverables with acceptance criteria. All "Must-Have" items are validated by the gate checker.

## Must-Have Deliverables

### D1: Project Structure

- [ ] `package.json` exists in the project root
- [ ] `express` is listed as a dependency in `package.json`
- [ ] `react` is listed as a dependency in `package.json`
- [ ] `server/` directory exists with at least one `.js` or `.ts` source file
- [ ] `client/` directory exists with React source files (`.jsx` or `.tsx`)

### D2: Running Application

- [ ] `npm run dev` starts both backend and frontend without errors
- [ ] Express server responds on its configured port (e.g., `http://localhost:3001`)
- [ ] Vite dev server serves the React app (e.g., `http://localhost:5173`)
- [ ] Landing page is accessible in a browser

### D3: Custom Slash Command

- [ ] At least 1 `SKILL.md` file exists in `.claude/skills/`
- [ ] The SKILL.md file has valid YAML frontmatter with `---` delimiters
- [ ] Frontmatter includes a `name` field
- [ ] Frontmatter includes a `description` field

## Should-Have Deliverables (Bonus)

### D4: Two Custom Commands

- [ ] `/new-test-case` SKILL.md exists with QA-specific test case structure
- [ ] `/bug-report` SKILL.md exists with defect reporting structure
- [ ] Both commands produce structured, domain-appropriate output when invoked

### D5: Landing Page Quality

- [ ] Landing page displays "QA Command Center" (or similar project title)
- [ ] Landing page includes TestDevLab branding (name, logo reference, or color scheme)
- [ ] Page is styled (not raw unstyled HTML)

### D6: Dev Script Quality

- [ ] `npm run dev` uses `concurrently` (or similar) to run server and client together
- [ ] Both server and client start from a single command

## Acceptance Criteria Summary

| ID | Deliverable | Validation Method |
|----|-------------|-------------------|
| D1 | Project structure | File existence checks |
| D2 | Running application | Process start + HTTP response |
| D3 | Custom slash command | File existence + YAML parse |
| D4 | Two commands | File existence + content inspection |
| D5 | Landing page | Content pattern matching |
| D6 | Dev script | package.json script inspection |

## Gate Command

```bash
./bootcamp complete-session 1
```

You must pass all Must-Have deliverables (D1-D3) to unlock Session 2.
