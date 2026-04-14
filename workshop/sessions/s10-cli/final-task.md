# Final Task: Test Coverage Matrix

**Weight: 25% of total bootcamp score**

This is your independent, graded final task. You will build a complete new
feature for the QA Command Center using all ten Claude Code capabilities you
learned across the bootcamp. There are no step-by-step instructions. You
have goals, requirements, and grading criteria. How you get there is up to
you and Claude Code.

---

## The Brief

Your QA Command Center tracks test cases, bugs, and test runs. But there is
a critical gap: nobody can answer the question "which features have test
coverage and which do not?" The Test Coverage Matrix solves this by mapping
features to test cases and visualizing where coverage exists and where it is
missing.

Build it. All of it. From data model to UI to automation.

---

## What You Must Build

### 1. Coverage Matrix Page

A new React page that displays a matrix (heatmap, grid, or table) showing:

- **Rows**: application features or functional areas
- **Columns**: test types (unit, integration, E2E, regression, smoke) or
  test case categories
- **Cells**: coverage status -- covered (has test cases), partial (some
  coverage), uncovered (no test cases), or a numeric coverage score

The matrix must be scannable at a glance. A QA manager looking at this page
should immediately see which features lack test coverage and what type of
testing is missing.

### 2. Data Model

A many-to-many relationship between features and test cases:

- **Features table**: feature name, description, priority, owner, status
- **Coverage mapping**: which test cases cover which features, with
  coverage type (full, partial, regression-only, etc.)
- **Aggregation**: computed coverage scores per feature and per test type

This is a data modeling exercise. Think about how the relationships work:
one test case can cover multiple features, and one feature can be covered
by multiple test cases.

### 3. API Routes

CRUD endpoints for the coverage matrix:

- Create, read, update, delete features
- Map and unmap test cases to features
- Query coverage by feature, by test type, or as a full matrix
- Aggregate coverage statistics (total features, covered percentage,
  highest-risk uncovered areas)

### 4. Visual Coverage Heatmap or Matrix Grid

The page must include a visual representation, not just a data table:

- Color-coded cells (green for covered, yellow for partial, red for
  uncovered)
- Interactive: clicking a cell shows which test cases provide that coverage
- Summary row and column showing aggregate coverage percentages
- Sortable or filterable by coverage status (show uncovered first)

### 5. CSV Coverage Import

Extend your CSV import capability (from Session 9) to handle coverage data:

- Import a CSV that maps features to test cases
- Validate that referenced test cases exist in the database
- Handle duplicates (skip or update)
- Report import results (rows imported, skipped, errors)

---

## Required Claude Code Feature Usage

You must use **all ten** Claude Code features during this task. The grading
rubric evaluates whether you leveraged each feature appropriately:

| # | Feature | How to Use It |
|---|---------|---------------|
| 1 | **Slash Commands** | Use your custom commands from S1 (e.g., `/new-test-case`) during development |
| 2 | **Memory** | Your CLAUDE.md standards should guide the data model and code style |
| 3 | **Skills** | Create a custom skill to generate coverage analysis (e.g., identify gaps, suggest priority) |
| 4 | **Subagents** | Use an agent to review coverage gaps and suggest which features need testing first |
| 5 | **MCP** | Create a Jira epic and stories for the coverage matrix feature via Atlassian MCP |
| 6 | **Hooks** | Add a hook that validates coverage data format (e.g., PreToolUse:Write hook for coverage CSV files) |
| 7 | **Plugins** | Add the new skill and hook to your qa-toolkit plugin manifest |
| 8 | **Checkpoints** | Use checkpoints to experiment with heatmap visualization approaches |
| 9 | **Advanced** | Use `/plan` to design the data model and API before coding. Use appropriate permission modes. |
| 10 | **CLI** | Add a CI step to generate a coverage summary report, or use `claude -p` for batch analysis |

---

## Jira Integration

Before writing any code, set up your project management:

1. **Create a "Test Coverage Matrix" epic** in Jira via Atlassian MCP
2. **Write user stories** with acceptance criteria for each major component:
   - Coverage data model and database schema
   - Feature CRUD API
   - Coverage mapping API
   - Coverage matrix page with heatmap
   - CSV coverage import
   - Coverage analysis skill
   - Coverage gap review agent
   - Coverage data validation hook
   - CI coverage report step
3. **Estimate and prioritize** the stories
4. **Update status** as you work through each story
5. **Close the epic** when all stories are complete

---

## Grading Criteria

The final task is scored across five dimensions:

### Prompt Quality (25%)

- Are your prompts specific, well-structured, and domain-appropriate?
- Do they reference your CLAUDE.md standards and existing data models?
- Do they provide enough context for Claude to generate correct code?
- Do they use QA terminology naturally (ISTQB severity, test techniques,
  coverage types)?

### Efficiency (15%)

- How many prompts did it take to complete the feature?
- Did you use planning mode to reduce iteration?
- Did you avoid unnecessary back-and-forth (clear requirements upfront)?
- Did you use appropriate permission modes to speed up execution?

### Deliverable Quality (20%)

- Does the coverage matrix page work correctly?
- Is the data model sound (proper relationships, no data anomalies)?
- Does the CSV import handle edge cases?
- Is the heatmap visually effective and interactive?
- Does the UI integrate seamlessly with the rest of the app?

### Standards Compliance (15%)

- Does the code follow your CLAUDE.md conventions?
- Are naming conventions consistent with the rest of the project?
- Do hooks and validators enforce your standards on the new feature?
- Are Jira stories well-written with proper acceptance criteria?

### Feature Usage (25%)

- Were all ten Claude Code features used?
- Was each feature used appropriately (not just checked off)?
- Does the skill produce useful coverage analysis?
- Does the agent provide actionable gap review?
- Does the hook actually validate coverage data?
- Was `/plan` used before coding the complex parts?

---

## Rules

1. **This is independent work.** No instructor help for the final task.
   You and Claude Code, working together.

2. **All code is vibe-coded.** You must not write any code manually. Every
   line must be generated by Claude Code from your prompts.

3. **Your standards apply.** The CLAUDE.md rules you wrote in Session 2
   govern this feature just like everything else. If your standards say
   components use PascalCase and API routes use kebab-case, the coverage
   matrix must follow suit.

4. **The feature must integrate with the existing app.** It should appear
   in the navigation, use the same database, follow the same design
   patterns, and feel like a natural part of the QA Command Center.

5. **Quality over speed.** A well-designed feature that uses 8 Claude Code
   capabilities thoughtfully scores higher than a rushed feature that
   checks all 10 boxes superficially.

---

## Hints (Not Solutions)

- Start with `/plan`. The coverage matrix has enough complexity (data model,
  many-to-many relationships, aggregation queries, visualization) that
  planning first will save you significant time.

- Think about the data model carefully. A many-to-many relationship between
  features and test cases typically uses a junction table. What additional
  fields does the junction table need? Coverage type? Confidence level?
  Date mapped?

- For the heatmap, consider what makes coverage data scannable. Features
  with zero coverage should stand out immediately. Features with full
  coverage can recede into the background. Color is your primary tool.

- The coverage analysis skill should do something useful, not just
  reformat data. Think about what a QA lead wants to know: which features
  are highest-risk (high priority + no coverage)? Which test types are
  underrepresented?

- The gap review agent should act like a senior QA engineer reviewing
  the coverage matrix. What would they flag? What would they recommend?
  "Feature X is critical priority but has only smoke tests -- recommend
  adding integration and E2E coverage."

- For the CSV import, reuse patterns from Session 9. The same validation
  approach works, but the data shape is different (feature-to-test-case
  mappings instead of test case records).

---

## Verification

Before submitting the final task:

1. **Matrix renders**: Navigate to the coverage matrix page. Is the
   heatmap/grid visible with color-coded cells?

2. **Data model works**: Create a feature, map test cases to it, and verify
   the coverage status updates in the matrix.

3. **CSV import**: Import a coverage CSV file. Do the mappings appear in
   the matrix?

4. **Interactive**: Click a cell in the matrix. Do you see which test cases
   provide coverage for that feature/test-type combination?

5. **Skill works**: Run your coverage analysis skill. Does it produce a
   useful report identifying gaps?

6. **Agent works**: Run your coverage gap review agent. Does it provide
   actionable recommendations?

7. **Hook fires**: Try to import a malformed coverage CSV. Does the hook
   catch the invalid format?

8. **CI step**: Check your GitHub Actions workflow. Is there a step that
   generates or validates coverage data?

9. **Navigation**: Is the Coverage Matrix accessible from the app's main
   navigation, alongside all other pages?

10. **Jira complete**: Are all coverage matrix stories in your Jira project
    marked as Done?

```bash
# Submit the final task
./bootcamp submit-final-task
```

---

## Time Guidance

The final task is designed to take approximately **90 minutes** for a student
who has completed all 10 sessions and is comfortable with Claude Code. If you
find yourself spending significantly more time, step back and use `/plan` to
reassess your approach.

Good luck. Ship it.
