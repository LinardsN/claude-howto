# Session 10: Ship It -- CLI and CI/CD

Nine sessions of building. Your QA Command Center has test case management,
bug tracking, a metrics dashboard with trend charts, test reports with HTML
export, CSV import/export, user settings, and a plugin that bundles everything
together. It is a real application. But it lives on your laptop.

This final session bridges the gap between "it works on my machine" and "it
runs in production." You will use Claude Code's CLI automation capabilities
to create a CI/CD pipeline, write batch processing scripts, and polish the
app into something you would demo with confidence. Then comes the final task:
an independent feature build that proves you can orchestrate all ten Claude
Code features on your own.

---

## Learning Objectives

- Use print mode (`claude -p`) for non-interactive automation and scripting
- Pipe content into Claude for automated review and analysis
- Create a GitHub Actions CI/CD pipeline with automated checks
- Build batch processing scripts that leverage `claude -p`
- Add navigation, routing, and responsive design for production readiness
- Apply professional polish (branding, layout consistency, error handling)

## Prerequisites

- Session 9 gate passed (`./bootcamp complete-session 9` green)
- Working QA Command Center with all features from S1-S9
- GitHub repository for your project (for CI/CD pipeline)
- Atlassian MCP configured

## Schedule

| Block | Duration | Activity |
|-------|----------|----------|
| 1 | 15 min | CLI automation: `claude -p`, piping, output formats |
| 2 | 20 min | Create GitHub Actions CI/CD pipeline |
| 3 | 20 min | Build batch processing scripts with `claude -p` |
| 4 | 20 min | Final polish: navigation, responsive design, branding |

**Total: 75 minutes**

---

## The Feature

**CLI and print mode** turn Claude Code from an interactive tool into an
automation engine. Instead of conversational back-and-forth, you can invoke
Claude as a command-line utility that reads input, processes it, and produces
structured output -- perfect for CI/CD pipelines, batch scripts, and
automated workflows.

Read the full reference module: [10-cli](../../10-cli/README.md)

Key concepts you will use today:

- **Print mode** (`claude -p "prompt"`): runs Claude non-interactively,
  prints the response, and exits. No conversation, no UI.
- **Output format** (`--output-format json`): returns structured JSON
  instead of plain text, useful for pipeline integration
- **Piping** (`cat file | claude -p "review this"`): feeds content into
  Claude for processing
- **Session management**: `--session-id` to resume, `--continue` to
  continue the last session
- **GitHub Actions**: Claude Code can be invoked in CI workflows for
  automated code review, documentation generation, and quality checks

---

## What You Will Build

### GitHub Actions CI/CD Pipeline

A `.github/workflows/` configuration that runs on push or pull request and
includes:

- **Linting**: ESLint or your project's linter checks all source files
- **Tests**: runs your test suite (if you have one) or at least validates
  the build
- **Build verification**: confirms `npm run build` succeeds without errors
- **Security audit**: `npm audit` or equivalent dependency check

The pipeline should be realistic -- something you would actually use on a
team project. Bonus if it includes a step that uses Claude Code or references
your MCP configuration from Session 5.

### Batch Processing Script

A shell script that uses `claude -p` to perform automated analysis. Ideas:

- Review all API route files and generate a summary of endpoints
- Analyze test coverage gaps across your codebase
- Generate release notes from recent git commits
- Validate all React components against your CLAUDE.md standards

The script should demonstrate that `claude -p` is useful for repeatable
automation tasks, not just interactive coding.

### Navigation and Routing

Your app has accumulated many pages across sessions 2-9. Now they need to
be connected with proper navigation:

- **Sidebar or top navigation bar** with links to every page
- **Client-side routing** so navigation does not trigger full page reloads
- **Active state**: current page is highlighted in the navigation
- **Responsive design**: layout works on desktop and tablet widths

### Professional Polish

Final touches to make the app presentation-ready:

- **Consistent branding**: color scheme, typography, and spacing that look
  intentional across all pages
- **Error handling**: pages show user-friendly messages when API calls fail
- **Loading states**: skeleton screens or spinners while data loads
- **Empty states**: helpful messages when lists have no data ("No test cases
  yet. Import some via CSV or create one manually.")

---

## Requirements

### Must-Have (Gate Checks)

- [ ] **CI pipeline**: `.github/workflows/` directory contains at least one valid YAML workflow file
- [ ] **Navigation**: App has a sidebar or navbar with links to all major pages
- [ ] **Client-side routing**: Navigation between pages does not cause full page reloads
- [ ] **Responsive design**: Layout is usable at both 1280px and 768px widths
- [ ] **Runnable**: `npm run dev` (or equivalent) starts the complete application
- [ ] **Component count**: At least 8 distinct React components (carried from S9)

### Should-Have (Bonus Points)

- [ ] **Batch script**: A shell script using `claude -p` for automated analysis or generation
- [ ] **CI uses Claude/MCP**: Pipeline includes a step that references Claude Code or MCP (S5 dependency)
- [ ] **Professional styling**: Consistent color scheme, typography, spacing, and branding across all pages
- [ ] **Error and loading states**: UI handles API failures and loading gracefully
- [ ] **Start script**: `package.json` has a configured `start` or `dev` script

---

## Rules

1. **The CI pipeline must be created through Claude Code.** Do not write
   the YAML manually. Describe what your pipeline should do and let Claude
   generate it. This is the last vibe-coding exercise.

2. **Use `claude -p` for at least one automation task.** This can be the
   batch script, a CI step, or any non-interactive use of Claude. The
   point is to experience print mode as an automation tool.

3. **The final app must be runnable with `npm run dev`.** This is the
   baseline deliverable. If someone clones your repo and runs `npm run dev`,
   they should see a working application with navigation between all your
   pages.

4. **Navigation must connect ALL pages.** Every page you built across
   sessions 2-9 should be reachable from the navigation. No orphan pages.

5. **All code is vibe-coded to the end.** Even for polish work -- describe
   the branding you want, the responsive behavior, the error states. Claude
   Code generates everything.

---

## Hints (Not Solutions)

- For the CI pipeline, think about what checks matter most for a team
  project: linting catches style issues, build verification catches
  compilation errors, and security audit catches vulnerable dependencies.
  Start with those three.

- `claude -p` with `--output-format json` is powerful for scripting.
  The JSON output can be parsed by `jq` and fed into other tools. Think
  about a pipeline: extract data -> process with Claude -> format output.

- For navigation, consider whether a sidebar or top bar works better for
  your page count. With 5+ pages, a sidebar is often easier to scan. With
  3-4, a top bar may suffice.

- Responsive design does not mean pixel-perfect mobile support. Focus on
  making sure nothing overflows or becomes unusable at tablet width
  (768px). CSS Grid or Flexbox with media queries handles most cases.

- For professional polish, pick a small color palette (2-3 colors) and
  apply it consistently. A single accent color for buttons, links, and
  active navigation states goes a long way.

---

## Jira Integration

Using the Atlassian MCP:

1. **Close all open epics** from previous sessions. Review each one, verify
   the stories are complete, and mark the epic as Done.
2. **Generate release notes** from your completed Jira stories. This is a
   good candidate for your `claude -p` batch script: pipe the Jira story
   summaries into Claude and ask for formatted release notes.
3. **Create a final "Ship It" epic** with stories for CI pipeline,
   navigation, responsive design, and polish.
4. **Document your bootcamp journey**: write a Jira comment summarizing
   what you built across all 10 sessions.

---

## Verification

Before running `./bootcamp complete-session 10`, self-check:

1. **App starts**: Run `npm run dev` and verify the app opens in a browser
   without errors.

2. **Navigation works**: Click through every link in your nav. Does each
   page load? Is the current page highlighted?

3. **Responsive test**: Resize your browser to 768px width. Is the layout
   still usable? Can you access all navigation items?

4. **CI pipeline valid**: Open `.github/workflows/*.yml` and verify the
   YAML is valid. Check that job steps reference real commands that would
   work in a GitHub Actions runner.

5. **Batch script runs**: If you created a batch script, execute it and
   verify it produces output. Does `claude -p` return a useful result?

6. **Full feature tour**: Walk through the complete app as a demo:
   Dashboard -> Test Cases -> Bugs -> Reports -> Import/Export -> Settings.
   Does everything work? Does it look professional?

```bash
# Validate your session deliverables
./bootcamp complete-session 10
```

---

## What Comes Next

After completing Session 10, you have one more challenge: the **Final Task**.

The final task is an independent, graded exercise worth 25% of your total
bootcamp score. You will build a new feature from scratch using all ten
Claude Code capabilities you learned. No hand-holding -- just you, Claude
Code, and a feature specification.

See [final-task.md](final-task.md) for the complete brief.
