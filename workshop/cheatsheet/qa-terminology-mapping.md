# QA Terminology to Claude Code Mapping

How familiar QA concepts map to Claude Code features.

## Test Management Concepts

| QA Concept | Claude Code Feature | Session |
|------------|-------------------|---------|
| Test plan template | Custom Slash Command (`SKILL.md`) | S1 |
| QA standards document | `CLAUDE.md` (Memory) | S2 |
| Reusable test procedure | Skill with auto-invocation | S3 |
| Specialized QA role | Custom Agent (`.claude/agents/`) | S4 |
| Tool integration (Jira, GitHub) | MCP Server | S5 |
| Quality gate / pre-commit check | Hook (`PreToolUse`, `PostToolUse`) | S6 |
| QA toolkit distribution | Plugin (`.claude-plugin/`) | S7 |
| Test environment snapshot | Checkpoint (`/rewind`) | S8 |
| Test strategy document | Planning Mode (`/plan`) | S9 |
| CI/CD test automation | CLI Print Mode (`claude -p`) | S10 |

## ISTQB Test Levels

| ISTQB Level | In QA Command Center | How Claude Builds It |
|-------------|---------------------|---------------------|
| Unit testing | Individual test cases | Generated via test-writer agent |
| Integration testing | API route tests | Generated from CLAUDE.md standards |
| System testing | Full test suites | Organized by /generate-test-suite skill |
| Acceptance testing | User story verification | Linked to Jira stories via MCP |

## Defect Management

| QA Process | Claude Code Workflow |
|------------|---------------------|
| Bug discovery | Claude identifies issues during code review |
| Bug reporting | /bug-report skill generates structured report |
| Severity classification | bug-triager agent categorizes (S1-S4) |
| GitHub issue creation | MCP server syncs to GitHub Issues |
| Jira ticket creation | Atlassian MCP creates stories with acceptance criteria |
| Fix verification | Hook validates fix follows CLAUDE.md standards |
| Regression check | Stop hook reminds to verify related test cases |

## Test Case Design Techniques (ISTQB)

| Technique | How Students Use It |
|-----------|-------------------|
| Boundary value analysis | Describe boundary conditions in prompts |
| Equivalence partitioning | Ask Claude to group inputs into classes |
| Decision tables | Describe conditions, Claude generates the table |
| State transition | Describe workflows, Claude creates state diagrams |
| Error guessing | security-scanner agent finds common issues |

## Process Mapping

| QA Process Step | Bootcamp Equivalent |
|----------------|-------------------|
| Test planning | Session guide requirements (goals + rules) |
| Test design | Crafting prompts that describe what to test |
| Test execution | Claude generates and runs the code |
| Test reporting | Reports page with HTML export |
| Defect tracking | Bug tracker module with GitHub sync |
| Test closure | `./bootcamp complete-session N` with gate validation |

## Roles

| QA Role | Bootcamp Activity |
|---------|------------------|
| Manual QA | Drives prompts (describes what to build in natural language) |
| Automation QA | Reviews generated code, writes hook configs directly |
| QA Lead | Defines CLAUDE.md standards, reviews agent configurations |
| Test Manager | Uses instructor dashboard, monitors student progress |

## Prompt Engineering for QA

| Instead of... | Try... |
|--------------|--------|
| "Make a test" | "Create a test case for user login with boundary values for password length (min 8, max 128 chars)" |
| "Fix the bug" | "The bug tracker form allows empty severity. Add validation that requires S1-S4 selection before submit" |
| "Add a page" | "Build a dashboard page showing: total test cases by status (pass/fail/blocked), open bugs by severity, and a table of the 10 most recent test runs" |
| "Set up CI" | "Create a GitHub Actions workflow that runs ESLint, checks for security issues, and generates a test coverage report on every PR" |
