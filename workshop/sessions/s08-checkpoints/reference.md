# Session 8 Reference: Checkpoints

Quick reference for checkpoint access, rewind options, and experimentation
workflows. See [08-checkpoints](../../08-checkpoints/README.md) for the full
tutorial.

---

## How Checkpoints Work

Every time Claude Code sends a response, it automatically creates a checkpoint
-- a snapshot of your entire project's file state. This happens silently in
the background with no performance cost.

```text
[You prompt] --> [Claude responds] --> [Checkpoint #1 created]
[You prompt] --> [Claude responds] --> [Checkpoint #2 created]
[You prompt] --> [Claude responds] --> [Checkpoint #3 created]
```

Each checkpoint captures the state of every file Claude has read or modified.
You can jump back to any checkpoint to restore that state.

---

## Accessing Checkpoints

### Method 1: Esc+Esc (Checkpoint Timeline)

Press `Escape` twice in quick succession to open the checkpoint list.

**What you see:**

- A chronological list of checkpoints
- Each entry shows a timestamp and a summary of what changed
- Scroll through the list to find the state you want
- Select a checkpoint to preview or restore it

**When to use**: When you want to browse your history and pick a specific
point to return to.

### Method 2: /rewind Command

Type `/rewind` to go back to a previous checkpoint.

```text
/rewind            # Interactive: shows recent checkpoints to choose from
/rewind 3          # Go back 3 checkpoints
```

**When to use**: When you know roughly how far back you want to go.

### Method 3: Undo (Ctrl+Z Equivalent)

For the most recent change only, you can undo Claude's last response and
restore the previous state.

**When to use**: When Claude's last response broke something and you
want to immediately undo it.

---

## Rewind Options

When you rewind, Claude Code offers options for handling the current state:

| Option | What Happens | When to Use |
|--------|-------------|-------------|
| **Discard current** | Current state is gone, restored state becomes active | You know the current approach is wrong |
| **Keep as branch** | Current state saved as a git branch before restoring | You might want to come back to it |
| **Stash changes** | Current changes stashed, clean restore | Quick comparison, might re-apply |
| **Diff only** | Shows what changed but does not restore | Just want to see the differences |
| **Cancel** | Nothing happens | Changed your mind |

---

## A/B Testing Workflow

The recommended workflow for comparing two approaches:

```text
Step 1: Get to a stable state (everything works)
        └── This is your "baseline checkpoint"

Step 2: Ask Claude to implement Approach A
        └── Checkpoint created automatically

Step 3: Evaluate Approach A
        ├── Does it work?
        ├── How does it look?
        ├── Any performance issues?
        └── Note your observations

Step 4: Press Esc+Esc, find the baseline checkpoint, restore it
        └── Choose "Keep as branch" to save Approach A

Step 5: Ask Claude to implement Approach B
        └── Checkpoint created automatically

Step 6: Evaluate Approach B
        ├── Same criteria as Step 3
        └── Compare against Approach A notes

Step 7: Choose the winner
        ├── If B wins: commit and move on
        └── If A wins: rewind to Step 4's branch
```

---

## Chart Library Quick Comparison

For your A/B test, here are libraries commonly compared:

| Library | Style | Bundle Size | Learning Curve |
|---------|-------|-------------|----------------|
| **Recharts** | Declarative React components | ~170 KB | Low |
| **Chart.js** (react-chartjs-2) | Canvas-based, imperative | ~60 KB | Medium |
| **Nivo** | Rich, D3-based with React | ~200 KB | Medium |
| **Victory** | Composable React primitives | ~150 KB | Medium |

Factors to evaluate:

- **Rendering quality**: Do the charts look professional?
- **Responsiveness**: Do charts resize with the browser window?
- **API ergonomics**: How natural is it to pass your data format?
- **Customization**: Can you match your app's color scheme and style?
- **Bundle size**: How much does it add to your production build?

---

## Git Evidence of Experimentation

The gate validator looks for evidence that you tried multiple approaches.
Here is what counts:

- **Commit messages** mentioning "try", "experiment", "compare", "A/B",
  "approach A", "approach B", "revert", "rewind"
- **Multiple commits** adding and then changing chart library dependencies
- **Branch names** indicating experiments (e.g., `experiment/recharts`,
  `experiment/chartjs`)
- **package.json history** showing different libraries were installed at
  different points

A clean git history with a single "add charts" commit suggests you did not
actually experiment. The gate will flag this.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Esc+Esc does not open anything | Ensure you are in the Claude Code CLI, not a regular terminal |
| /rewind shows no checkpoints | You may be in a fresh session; checkpoints are per-session |
| Rewinding lost my node_modules | Run `npm install` after rewinding; node_modules are not always checkpointed |
| Chart library conflicts after rewind | Delete `node_modules` and `package-lock.json`, then `npm install` |
| Cannot find my old approach | Use git log and git stash list to find saved experiments |
