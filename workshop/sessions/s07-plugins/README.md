# Session 7: Packaging It All Together -- Plugins

Six sessions of work sit across your project: slash commands, memory rules,
skills, agents, hooks, and MCP integrations. Each piece works, but they are
scattered artifacts that only make sense if you know the history. Plugins
change that. A plugin is a single, distributable package that bundles related
Claude Code capabilities so that anyone -- a new team member, a different
project, your future self -- can install everything at once.

In this session you will assemble the "TestDevLab QA Toolkit" plugin by
bundling the most valuable artifacts from previous sessions into a coherent
package with a manifest, documentation, and clear entry points. You will also
build a test reports page that lets users view run results and export them as
downloadable HTML reports.

---

## Learning Objectives

- Create a valid plugin manifest (`plugin.json`) that describes bundled capabilities
- Bundle slash commands, skills, agents, hooks, and MCP configurations into a single plugin directory
- Understand plugin loading via the `--plugin-dir` flag
- Build a distributable package that another team could install and use immediately
- Generate downloadable HTML test reports from your QA Command Center

## Prerequisites

- Session 6 gate passed (`./bootcamp complete-session 6` green)
- Working QA Command Center with: test cases, bug tracker, dashboard, hooks
- Artifacts from S1 (commands), S3 (skills), S4 (agents), S6 (hooks) available in your project
- Atlassian MCP configured

## Schedule

| Block | Duration | Activity |
|-------|----------|----------|
| 1 | 10 min | Plugin concept and manifest walkthrough |
| 2 | 30 min | Bundle QA toolkit plugin from previous session artifacts |
| 3 | 35 min | Build test reports page with HTML export |

**Total: 75 minutes**

---

## The Feature

**Plugins** are self-contained packages that extend Claude Code with bundled
commands, skills, agents, hooks, and MCP configurations. They are the
distribution mechanism for everything you have built so far.

Read the full reference module: [07-plugins](../../07-plugins/README.md)

Key concepts you will use today:

- **Plugin manifest** (`plugin.json`): declares the plugin's name, version,
  description, and all bundled components with their paths
- **Directory convention**: `.claude-plugin/` contains the manifest and
  all referenced files in a structured layout
- **Loading**: `claude --plugin-dir .claude-plugin/` loads the plugin on
  startup, making all its commands, skills, and hooks available
- **Bundling**: plugins can include any combination of slash commands,
  skills, agent definitions, hooks, and MCP server configurations
- **Distribution**: the plugin directory is self-contained and can be
  copied to another project or shared as a zip/tarball

---

## What You Will Build

### The QA Toolkit Plugin

A `.claude-plugin/` directory containing a `plugin.json` manifest that
bundles artifacts from your previous sessions:

- **From Session 1**: Slash commands (e.g., `/new-test-case`, `/bug-report`)
- **From Session 3**: Skills (e.g., `generate-test-suite`, `qa-review`)
- **From Session 4**: Agent definitions (e.g., test writer, bug triager)
- **From Session 6**: Hooks (e.g., file naming validator, auto-lint)

The manifest must reference real files that exist in your project. This is
the progressive dependency test: your plugin proves that you built working
artifacts across multiple sessions and can integrate them into a coherent
package.

### Test Reports Page

A new React page in your QA Command Center that:

- Displays a list of test reports with run date, suite name, total/passed/
  failed counts, and status
- Allows selecting a report to view details (individual test results)
- Provides a "Download HTML Report" button that generates a self-contained
  HTML file with charts, summary statistics, and detailed results
- The HTML export should be presentable to stakeholders without requiring
  access to your app

---

## Requirements

### Must-Have (Gate Checks)

- [ ] `.claude-plugin/plugin.json` exists and is valid JSON
- [ ] Plugin manifest references skills from Session 3
- [ ] Plugin manifest references agents from Session 4
- [ ] Plugin manifest references hooks from Session 6
- [ ] All referenced files actually exist at the specified paths
- [ ] Test reports page renders at a dedicated route (e.g., `/reports`)

### Should-Have (Bonus Points)

- [ ] Plugin includes a README.md explaining what it provides and how to install it
- [ ] Plugin also bundles slash commands from Session 1 (four sessions total)
- [ ] Downloadable HTML test report with embedded charts or summary statistics
- [ ] HTML report is self-contained (inline CSS/JS, no external dependencies)
- [ ] Plugin manifest includes version number and description

---

## Rules

1. **The plugin MUST bundle artifacts from at least three previous sessions**
   (S3 skills, S4 agents, S6 hooks). This is not optional -- it is the core
   progressive dependency check for this session. If you skipped or lost
   artifacts from earlier sessions, you need to recreate them before the
   plugin will pass the gate.

2. **Referenced files must be real.** The manifest cannot point to files that
   do not exist. The gate validator will follow every path in `plugin.json`
   and verify the target exists.

3. **The plugin must be loadable.** Running `claude --plugin-dir .claude-plugin/`
   should not produce errors. The manifest schema must be correct.

4. **Think distribution.** Write the plugin as if you are handing it to a
   colleague who has never seen your project. Would they understand what it
   does? Would it work in their environment?

5. **All code is vibe-coded.** Claude Code generates the manifest, the
   directory structure, the reports page, and the HTML export. You describe
   what you want.

---

## Hints (Not Solutions)

- Start by inventorying what you have. Look at your project for the skill
  files from S3, agent definitions from S4, and hook scripts from S6. You
  need to know their exact paths to reference them in the manifest.

- The `plugin.json` manifest is a JSON file with a specific schema. Think
  about what fields a package manifest typically has: name, version,
  description, and then the capabilities it provides.

- For the HTML report export, think about what a standalone HTML file needs:
  inline `<style>` and `<script>` blocks, a data section with the test
  results, and enough structure to be readable without your app running.

- If you find that artifacts from earlier sessions are missing or broken,
  this is the right time to fix them. The plugin is a quality check on
  all your previous work.

- Consider grouping related capabilities in the manifest. Commands go in
  one section, skills in another, hooks in another. This makes the manifest
  readable and the plugin easy to extend.

---

## Jira Integration

Using the Atlassian MCP:

1. **Create a "Plugin Packaging" epic** in your project board
2. **Write stories** for:
   - Plugin manifest creation and validation
   - Bundling S3 skills into the plugin
   - Bundling S4 agents into the plugin
   - Bundling S6 hooks into the plugin
   - Test reports page with report listing
   - HTML report export functionality
3. **Link dependent stories**: the bundling stories depend on the manifest
   story; the export story depends on the reports page story
4. **Update status** as you complete each piece

---

## Verification

Before running `./bootcamp complete-session 7`, self-check:

1. **Manifest validation**: Open `.claude-plugin/plugin.json` and verify it
   is valid JSON. Check that every file path referenced in the manifest
   points to a file that actually exists.

2. **Progressive dependencies**: Confirm the manifest references at least
   one skill (S3), one agent (S4), and one hook (S6). Ideally also a slash
   command (S1).

3. **Plugin loading**: Run `claude --plugin-dir .claude-plugin/` and verify
   no errors are reported during startup.

4. **Reports page**: Navigate to your reports route. Can you see a list of
   test reports? Can you click one to see details?

5. **HTML export**: Click the download button. Open the downloaded HTML file
   directly in a browser (not through your dev server). Does it render
   correctly with data, styling, and any charts?

```bash
# Validate your session deliverables
./bootcamp complete-session 7
```
