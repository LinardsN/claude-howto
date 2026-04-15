# Session 8: Experiment Fearlessly -- Checkpoints

Every decision in software development carries risk. Pick the wrong chart
library and you lose an afternoon ripping it out. Choose the wrong layout and
you spend hours undoing CSS tangles. In traditional development, this fear of
wasted effort makes teams conservative -- they go with the safe choice, the
familiar tool, the layout that worked last time.

Checkpoints eliminate that risk. Claude Code automatically snapshots your
project state on every response, giving you a time-travel mechanism that
makes experimentation free. Try an approach, evaluate it, and if it does not
work, rewind to the exact state before the experiment started. No `git stash`
gymnastics, no manual undo chains, no fear.

In this session you will use checkpoints to A/B test chart libraries and
dashboard layouts, picking the best of each after direct comparison.

---

## Learning Objectives

- Understand how automatic checkpoints work (every Claude response creates one)
- Use `Esc+Esc` to view the checkpoint timeline and select a restore point
- Use the `/rewind` command to roll back to a specific checkpoint
- Compare multiple implementation approaches before committing to one
- Make evidence-based technical decisions through rapid prototyping

## Prerequisites

- Session 7 gate passed (`./bootcamp complete-session 7` green)
- Working QA Command Center with dashboard, test cases, bugs, reports, and plugin
- Atlassian MCP configured
- Familiarity with your project's dashboard page (from S6) and reports page (from S7)

## Schedule

| Block | Duration | Activity |
|-------|----------|----------|
| 1 | 10 min | Checkpoints concept and workflow demonstration |
| 2 | 30 min | A/B test chart libraries for dashboard trend charts |
| 3 | 20 min | A/B test dashboard layouts (card arrangement, navigation) |
| 4 | 15 min | Finalize choices, clean up, and commit |

**Total: 75 minutes**

---

## The Feature

**Checkpoints** are automatic snapshots of your entire project state that
Claude Code creates on every response. They give you zero-cost experimentation
by making any change fully reversible.

Read the full reference module: [08-checkpoints](../../08-checkpoints/README.md)

Key concepts you will use today:

- **Automatic creation**: every time Claude responds, a checkpoint is created
  with the full state of all files
- **Esc+Esc**: press Escape twice to open the checkpoint timeline, showing
  every snapshot with its timestamp and summary
- **/rewind command**: jump back to any previous checkpoint, restoring all
  files to that exact state
- **Five restore options**: when rewinding, you can choose how to handle the
  current state (discard, keep as branch, stash, etc.)
- **Safe experimentation**: checkpoints make it safe to try radical changes
  because you can always go back

---

## What You Will Build

### Experiment 1: Chart Library A/B Test

Your dashboard (from Session 6) shows metrics cards and a table, but lacks
trend visualizations. In this experiment you will add trend charts by trying
two different chart libraries and comparing the results.

**Approach A**: Install one chart library (e.g., Recharts) and build trend
charts for test pass rate over time, bugs opened vs closed, and test
execution duration.

**Checkpoint. Evaluate. Rewind.**

**Approach B**: Install a different chart library (e.g., Chart.js with
react-chartjs-2, Nivo, Victory, or another of your choice) and build the
same three charts.

**Compare both approaches** on: rendering quality, bundle size, API
ergonomics, and how well the charts integrate with your existing design.
Pick the winner.

### Experiment 2: Dashboard Layout A/B Test

With your chosen chart library, experiment with two different dashboard
layouts:

**Layout A**: One arrangement of metrics cards, charts, and tables. Consider
a grid-based layout, a single-column flow, or a sidebar approach.

**Checkpoint. Evaluate. Rewind.**

**Layout B**: A fundamentally different arrangement. If Layout A was a grid,
try a dashboard-with-sidebar. If it was single-column, try a multi-panel
view.

**Compare and choose** based on: information density, scan-ability, and
how well it presents QA data to different audiences (engineers vs managers).

---

## Requirements

### Must-Have (Gate Checks)

- [ ] **Working trend charts**: Dashboard displays at least two chart visualizations with data
- [ ] **Chart library installed**: `package.json` includes a chart library as a dependency
- [ ] **Experimentation evidence**: Git history shows at least two different approaches were tried (different commits, branches, or messages indicating A/B testing)
- [ ] **Dashboard functional**: Dashboard page loads without errors and displays charts alongside existing metrics

### Should-Have (Bonus Points)

- [ ] **Multiple chart types**: Dashboard uses at least two different chart types (e.g., line chart + bar chart, or area chart + pie chart)
- [ ] **Layout polish**: Dashboard has a cohesive layout with intentional information hierarchy
- [ ] **Dark theme or variant**: An alternative visual theme was explored (even if not kept)
- [ ] **Charts use real data**: Trend charts pull from your API, not hardcoded arrays

---

## Rules

1. **You MUST try at least two different approaches and use /rewind to go
   back.** This is not a suggestion -- it is the core learning objective.
   Do not just install the first chart library and call it done. The value
   of this session is in the comparison.

2. **Document your decision.** After comparing approaches, your commit
   message or a comment in the code should explain WHY you chose the
   winning approach. "Chose Recharts because..." is more valuable than
   "Added charts."

3. **Do not fear breakage.** Checkpoints exist so you can try things that
   might fail. Install a library, try to integrate it, and if it produces
   ugly charts or conflicts with your setup, rewind and try something else.
   That is the workflow.

4. **Time-box each experiment.** Spend roughly equal time on each approach
   (about 15 minutes per chart library, 10 minutes per layout). Do not
   over-invest in the first approach.

5. **All code is vibe-coded.** You describe the charts you want, the data
   they should display, and the layout you envision. Claude Code generates
   the implementation.

---

## Hints (Not Solutions)

- Before starting Experiment 1, make sure your dashboard API returns
  time-series data (dates with corresponding values). If it does not, add
  that endpoint first -- then checkpoint before the library experiments.

- When you press `Esc+Esc`, you see a list of checkpoints with timestamps.
  The one labeled just before you asked Claude to install the first chart
  library is your "clean slate" -- that is where you rewind to before
  trying the second library.

- For the layout A/B test, think about who uses your dashboard. A QA
  engineer wants quick access to failing tests. A manager wants a
  high-level pass rate trend. Can your layout serve both?

- Chart libraries differ in how they handle responsive sizing. Test your
  charts at different browser widths before deciding.

- If you are not sure which libraries to compare, here are some pairs that
  offer meaningfully different approaches: Recharts vs Chart.js,
  Recharts vs Nivo, Victory vs Nivo. Pick two that you have not used
  before if possible -- this is a learning opportunity.

---

## Jira Integration

Using the Atlassian MCP:

1. **Update existing dashboard stories** with the chart requirements
2. **Create a decision record**: Write a Jira comment or task documenting
   your A/B test results -- which libraries you tried, what you observed,
   and why you chose the winner
3. **Update story status** as you finalize the implementation

This is a lighter Jira session since the work is experimental. The
decision record is the key artifact.

---

## Verification

Before running `./bootcamp complete-session 8`, self-check:

1. **Charts render**: Navigate to your dashboard. Do you see at least two
   chart visualizations with data points?

2. **Library installed**: Check `package.json` -- is your chosen chart
   library listed as a dependency?

3. **Experimentation evidence**: Run `git log --oneline -20` and look for
   evidence of multiple approaches. Do you see commits or messages that
   indicate you tried different options?

4. **No console errors**: Open browser dev tools on the dashboard page.
   Are there any React errors, missing dependency warnings, or failed
   API calls?

5. **Data integrity**: Do the charts show data that matches your test runs
   and bug records? Add a new test run and refresh -- does the chart
   update?

```bash
# Validate your session deliverables
./bootcamp complete-session 8
```
