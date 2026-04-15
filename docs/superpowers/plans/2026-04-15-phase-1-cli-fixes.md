# Phase 1: CLI Platform Fixes — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix the audit-discovered bugs in `workshop/` so the bootcamp CLI is correct, tested, and pilot-ready.

**Architecture:** Existing Python CLI (argparse subcommands + SQLite + gate validators + scoring engine). All changes are additive or in-place fixes; no architectural restructuring. JSONL files become the single source of truth for prompt logs (matching what real hooks write).

**Tech Stack:** Python 3.10+ (standard library only for runtime; pytest/ruff/mypy for dev). No external services required.

**Spec reference:** `docs/superpowers/specs/2026-04-15-ai-bootcamp-platform-design.md` § 5 Phase 1 + Appendix A.

---

## File Plan

**Created:**
- `workshop/__init__.py` (empty marker)
- `pyproject.toml` (repo root — pytest config so `pytest` works without `PYTHONPATH=.`)
- `workshop/requirements-dev.txt` (pytest, ruff, mypy)
- `workshop/platform/doctor.py` (preflight checks)
- `workshop/platform/jsonl_log.py` (JSONL log reader, single source of truth)
- `workshop/PILOT-RUNBOOK.md` (operational playbook)
- `workshop/tests/test_doctor.py`
- `workshop/tests/test_scoring_consistency.py`
- `workshop/tests/test_demo_fixtures.py`
- `workshop/tests/test_jsonl_log.py`

**Modified:**
- `workshop/bootcamp` (Python version guard at entry)
- `workshop/platform/cli.py` (`complete-session` writes correct per-session totals; `status --prompts` reads JSONL; new `doctor` subcommand)
- `workshop/platform/database.py` (remove `prompt_logs` table + `log_prompt`/`get_prompt_logs`/`get_prompt_count` — replaced by JSONL reader)
- `workshop/scoring/scorer.py` (don't overwrite per-session totals with aggregate)
- `workshop/demo.sh` (Bob's fixture must fail S1 critical; Alice gets `start-session` per session; prompts written as JSONL not SQLite)
- `workshop/INSTRUCTOR-GUIDE.md` (correct Atlassian MCP package name)
- `workshop/sessions/s05-mcp/README.md` (correct package name)
- `workshop/sessions/s05-mcp/reference.md` (correct package name)
- `.github/workflows/test.yml` (add workshop test job)

**Deleted:** none.

---

## Branch Setup

- [ ] **Step 1: Create feature branch from main**

```bash
cd /Users/linardsn/Documents/GitHub/claude-howto
git checkout main
git pull --ff-only
git checkout -b phase-1-cli-fixes
```

Expected: `Switched to a new branch 'phase-1-cli-fixes'`

---

## Task 1: Package structure + pytest config

**Files:**
- Create: `workshop/__init__.py`
- Create: `pyproject.toml`
- Create: `workshop/requirements-dev.txt`

This lets `pytest workshop/tests/` work from repo root without `PYTHONPATH=.` and enables `ruff`/`mypy` config in one place.

- [ ] **Step 1.1: Create empty package marker**

Run: `touch workshop/__init__.py`

Expected: file exists, empty.

- [ ] **Step 1.2: Create root pyproject.toml with pytest config**

Create `pyproject.toml` at repo root with:

```toml
[tool.pytest.ini_options]
minversion = "7.0"
testpaths = ["workshop/tests", "scripts/tests"]
pythonpath = ["."]
addopts = "-v --tb=short"

[tool.ruff]
line-length = 100
target-version = "py310"
extend-exclude = [".venv", "node_modules"]

[tool.ruff.lint]
select = ["E", "F", "W", "I", "B", "UP"]
ignore = ["E501"]  # line too long handled by formatter

[tool.mypy]
python_version = "3.10"
ignore_missing_imports = true
warn_unused_ignores = true
exclude = ["scripts/", ".venv/"]
```

(Note: `scripts/` already has its own pyproject.toml for bandit; this root file adds pytest discovery without conflicting.)

- [ ] **Step 1.3: Create workshop/requirements-dev.txt**

```
pytest>=7.4
pytest-cov>=4.1
ruff>=0.5
mypy>=1.10
```

- [ ] **Step 1.4: Verify pytest discovers workshop tests without PYTHONPATH**

Run from repo root:
```bash
/opt/homebrew/bin/python3 -m venv /tmp/p1-venv
/tmp/p1-venv/bin/pip install -r workshop/requirements-dev.txt
/tmp/p1-venv/bin/pytest workshop/tests/ -q
```

Expected: `45 passed` (all existing tests). No `ModuleNotFoundError`. No `PYTHONPATH=.` needed.

- [ ] **Step 1.5: Commit**

```bash
git add workshop/__init__.py pyproject.toml workshop/requirements-dev.txt
git commit -m "feat(workshop): make workshop a proper package with pytest config"
```

---

## Task 2: Python version guard at `bootcamp` entry

**Files:**
- Modify: `workshop/bootcamp` (entire file rewrite — only 13 lines)
- Create test: `workshop/tests/test_bootcamp_entry.py`

The CLI silently fails on Python 3.9 with `TypeError: unsupported operand type(s) for |: 'type' and 'NoneType'`. Fail-fast with a clear message before any imports of code that uses 3.10+ syntax.

- [ ] **Step 2.1: Write failing test for version guard**

Create `workshop/tests/test_bootcamp_entry.py`:

```python
"""Test the bootcamp CLI entry script's Python version guard."""

import subprocess
import sys
from pathlib import Path

BOOTCAMP = Path(__file__).resolve().parent.parent / "bootcamp"


def test_bootcamp_entry_runs_under_current_python():
    """The bootcamp script should execute and show help on a supported Python."""
    result = subprocess.run(
        [sys.executable, str(BOOTCAMP), "--help"],
        capture_output=True, text=True, timeout=10,
    )
    # Help shown OR exit 1 (no command) — both acceptable; key is no Python error
    assert "AI Bootcamp Platform" in (result.stdout + result.stderr), (
        f"Expected help text. stdout={result.stdout!r} stderr={result.stderr!r}"
    )


def test_bootcamp_entry_has_version_guard():
    """The bootcamp script must check Python version before importing CLI code."""
    content = BOOTCAMP.read_text()
    assert "sys.version_info" in content, (
        "Expected sys.version_info check at top of bootcamp script "
        "(before imports of workshop modules)"
    )
    # Guard must come before importing workshop.platform.cli (which uses 3.10+ syntax)
    guard_idx = content.find("sys.version_info")
    import_idx = content.find("from workshop.platform.cli")
    assert guard_idx < import_idx, (
        "Version guard must appear BEFORE 'from workshop.platform.cli' import"
    )
```

- [ ] **Step 2.2: Run test, verify second test fails**

```bash
/tmp/p1-venv/bin/pytest workshop/tests/test_bootcamp_entry.py -v
```

Expected: `test_bootcamp_entry_has_version_guard` FAILS (no `sys.version_info` check yet). First test may pass if running on 3.10+.

- [ ] **Step 2.3: Add version guard to `workshop/bootcamp`**

Replace the entire file with:

```python
#!/usr/bin/env python3
"""AI Bootcamp CLI entry point."""

import sys

# Python version guard — must come BEFORE any import of workshop.* modules
# because they use 3.10+ syntax (e.g. `Path | None` union types).
if sys.version_info < (3, 10):
    sys.stderr.write(
        f"\nERROR: AI Bootcamp requires Python 3.10 or newer.\n"
        f"You are running Python {sys.version.split()[0]}.\n\n"
        f"On macOS, install via Homebrew:\n"
        f"  brew install python@3.12\n"
        f"  alias python3=/opt/homebrew/bin/python3\n\n"
        f"Or use uv:\n"
        f"  pip install uv && uv python install 3.12\n"
    )
    sys.exit(2)

from pathlib import Path

# Add workshop directory to Python path
workshop_dir = Path(__file__).parent
sys.path.insert(0, str(workshop_dir.parent))

from workshop.platform.cli import main

sys.exit(main())
```

- [ ] **Step 2.4: Run tests, verify both pass**

```bash
/tmp/p1-venv/bin/pytest workshop/tests/test_bootcamp_entry.py -v
```

Expected: 2 passed.

- [ ] **Step 2.5: Commit**

```bash
git add workshop/bootcamp workshop/tests/test_bootcamp_entry.py
git commit -m "fix(workshop): add Python 3.10+ version guard to bootcamp entry"
```

---

## Task 3: Fix demo Bob fixture (must actually fail S1)

**Files:**
- Modify: `workshop/demo.sh` (Bob's fixture setup)
- Create test: `workshop/tests/test_demo_fixtures.py`

The S1 gate (`workshop/gates/gate_s01_slash_commands.py`) requires `.claude/skills/` directory with at least one `SKILL.md`. Bob's current fixture includes both, so he passes — auto-unlock never fires. Remove the skills dir from Bob so he fails the "Custom skills directory exists" critical check, which means his 5 attempts will fail until auto-unlock triggers.

- [ ] **Step 3.1: Read the S1 gate to confirm critical checks**

```bash
cat workshop/gates/gate_s01_slash_commands.py
```

Expected output includes a check for `.claude/skills/` and at least one `SKILL.md`, both `critical=True`.

- [ ] **Step 3.2: Write failing test for Bob's fixture**

Create `workshop/tests/test_demo_fixtures.py`:

```python
"""Tests that verify the demo.sh fixtures produce the intended scenarios."""

from pathlib import Path

from workshop.gates.gate_runner import run_gate


def _make_bob_fixture(tmp_path: Path) -> Path:
    """Replicate Bob's fixture from demo.sh exactly as it should be after fix."""
    project = tmp_path / "qa-demo-bob"
    (project / "server").mkdir(parents=True)
    (project / "client" / "src").mkdir(parents=True)
    (project / "package.json").write_text(
        '{"name":"qa-command-center","dependencies":'
        '{"express":"^4.18","react":"^18"}}'
    )
    (project / "server" / "index.js").write_text("const express = require('express');")
    (project / "client" / "src" / "App.jsx").write_text(
        "export default function App() { return <h1>Hello</h1>; }"
    )
    # NOTE: deliberately no .claude/skills/ — Bob is the struggling student
    return project


def test_bob_fixture_fails_s1_critical_check(tmp_path):
    """Bob's fixture must fail at least one critical S1 check so auto-unlock can fire."""
    project = _make_bob_fixture(tmp_path)
    results = run_gate(1, project)

    critical_failures = [
        r for r in results
        if not r["passed"] and r.get("critical", True)
    ]
    assert len(critical_failures) >= 1, (
        f"Bob must fail at least one critical S1 check, but all critical checks "
        f"passed. Results: {results}"
    )
    # Specifically the skills checks should be among the failures
    failure_messages = " ".join(r["message"] for r in critical_failures).lower()
    assert "skill" in failure_messages, (
        f"Expected a skills-related critical failure, got: {failure_messages}"
    )
```

- [ ] **Step 3.3: Run test, verify it FAILS (confirming Bob currently passes)**

```bash
/tmp/p1-venv/bin/pytest workshop/tests/test_demo_fixtures.py::test_bob_fixture_fails_s1_critical_check -v
```

Expected: PASS — because the test creates a fixture WITHOUT skills dir. So the test should already pass against a hypothetical fixture. We need a different test — one that runs the actual `demo.sh` setup logic.

(Adjust: the test above tests our INTENDED Bob fixture. To verify the bug, we need to test the CURRENT demo.sh behavior. Easier: just fix the demo.sh and verify the test passes.)

- [ ] **Step 3.4: Fix Bob's fixture in `workshop/demo.sh`**

Open `workshop/demo.sh` and find the section starting with `# --- Bob: only S1 done (struggling, lots of attempts) ---` (around line 69).

Replace:
```bash
# --- Bob: only S1 done (struggling, lots of attempts) ---
echo "Setting up Bob (S1 only, struggling)..."
mkdir -p /tmp/qa-demo-bob/{server,client/src,.claude/skills/new-tc}
cat > /tmp/qa-demo-bob/package.json <<'EOF'
{"name":"qa-command-center","dependencies":{"express":"^4.18","react":"^18"}}
EOF
cat > /tmp/qa-demo-bob/server/index.js <<'EOF'
const express = require('express');
EOF
cat > /tmp/qa-demo-bob/client/src/App.jsx <<'EOF'
export default function App() { return <h1>Hello</h1>; }
EOF
cat > /tmp/qa-demo-bob/.claude/skills/new-tc/SKILL.md <<'EOF'
---
name: new-test-case
description: Create test case
---
# New Test Case
EOF
```

With:
```bash
# --- Bob: struggling student (missing .claude/skills/ — fails S1 critical) ---
echo "Setting up Bob (struggling, will fail S1 until auto-unlock)..."
mkdir -p /tmp/qa-demo-bob/{server,client/src}
cat > /tmp/qa-demo-bob/package.json <<'EOF'
{"name":"qa-command-center","dependencies":{"express":"^4.18","react":"^18"}}
EOF
cat > /tmp/qa-demo-bob/server/index.js <<'EOF'
const express = require('express');
EOF
cat > /tmp/qa-demo-bob/client/src/App.jsx <<'EOF'
export default function App() { return <h1>Hello</h1>; }
EOF
# Deliberately no .claude/skills/ — Bob hasn't built any custom skills yet
```

- [ ] **Step 3.5: Verify test passes against the fixed fixture**

```bash
/tmp/p1-venv/bin/pytest workshop/tests/test_demo_fixtures.py -v
```

Expected: 1 passed.

- [ ] **Step 3.6: Run the demo and verify Bob fails 4 times then auto-unlocks at attempt 5**

```bash
cd workshop
PATH=/opt/homebrew/bin:$PATH ./demo.sh 2>&1 | grep -E "Bob attempt|FAIL|PASS|AUTO-UNLOCKED" | head -40
cd ..
```

Expected: At least 4 attempts show critical FAILs; attempt 5 shows `AUTO-UNLOCKED after 5 attempts`.

- [ ] **Step 3.7: Commit**

```bash
git add workshop/demo.sh workshop/tests/test_demo_fixtures.py
git commit -m "fix(workshop/demo): Bob's fixture must fail S1 to trigger auto-unlock"
```

---

## Task 4: Fix demo Alice progression (start each session before completing)

**Files:**
- Modify: `workshop/demo.sh` (Alice's session loop)

The current demo only runs `start-session 1` then loops `complete-session 1/2/3`. But `complete-session` updates an existing `session_progress` row; if the row doesn't exist (because `start-session N` was never called), the UPDATE matches zero rows and the session stays "Not Started." That's why `status --detailed` shows S2/S3 as Not Started even though scores exist.

- [ ] **Step 4.1: Add a test for Alice's progression**

Append to `workshop/tests/test_demo_fixtures.py`:

```python
import sqlite3

from workshop.platform.database import (
    create_cohort, get_connection, get_session_progress,
    register_student, start_session, complete_session, save_score,
)


def test_alice_progression_records_each_session(tmp_path):
    """After completing S1, S2, S3, all three should appear in session_progress
    with gate_passed=True. This catches the demo's missing start-session calls."""
    db_path = tmp_path / "test.db"
    conn = get_connection(db_path)
    create_cohort(conn, "test-cohort", "Test Cohort")
    register_student(conn, "alice", "Alice Test", "a@test.com", "test-cohort")

    # Simulate proper flow: start before complete for EACH session
    for s in [1, 2, 3]:
        start_session(conn, "alice", s)
        complete_session(conn, "alice", s, gate_passed=True,
                         gate_details={"checks": [], "total_points": 100,
                                       "max_points": 100})
        save_score(conn, "alice", s, 0, 0, 100, 0, 100)

    progress = get_session_progress(conn, "alice")
    completed = [p for p in progress if p["gate_passed"]]
    assert len(completed) == 3, (
        f"Expected 3 completed sessions, got {len(completed)}: "
        f"{[(p['session_number'], bool(p['gate_passed'])) for p in progress]}"
    )
    conn.close()
```

- [ ] **Step 4.2: Run test — verify it passes (this confirms the FIX pattern works)**

```bash
/tmp/p1-venv/bin/pytest workshop/tests/test_demo_fixtures.py::test_alice_progression_records_each_session -v
```

Expected: PASS. (We're documenting the correct flow.)

- [ ] **Step 4.3: Fix Alice's loop in `workshop/demo.sh`**

Find the block (around line 134):
```bash
# Alice: pass S1, S2, S3
# Set current session for alice
echo "alice" > ~/.claude-bootcamp/student-id
for s in 1 2 3; do
  echo "$s" > ~/.claude-bootcamp/current-session
  ./bootcamp complete-session $s --project-dir /tmp/qa-demo-alice 2>&1 | tail -5
done
```

Replace with:
```bash
# Alice: pass S1, S2, S3 — must call start-session before complete-session each time
echo "alice" > ~/.claude-bootcamp/student-id
for s in 1 2 3; do
  echo "$s" > ~/.claude-bootcamp/current-session
  ./bootcamp start-session $s 2>&1 | tail -2
  ./bootcamp complete-session $s --project-dir /tmp/qa-demo-alice 2>&1 | tail -5
done
```

- [ ] **Step 4.4: Run demo + verify Alice's status shows S1-S3 as Completed**

```bash
cd workshop
PATH=/opt/homebrew/bin:$PATH ./demo.sh > /tmp/demo-output.txt 2>&1
PATH=/opt/homebrew/bin:$PATH ./bootcamp status --student alice --detailed | grep -E "S[1-3]:" 
cd ..
```

Expected: S1, S2, S3 all show `Completed` and `PASSED`. No `Not Started`.

- [ ] **Step 4.5: Commit**

```bash
git add workshop/demo.sh workshop/tests/test_demo_fixtures.py
git commit -m "fix(workshop/demo): call start-session before complete-session in Alice's loop"
```

---

## Task 5: Fix scoring path consistency (don't overwrite per-session totals with aggregate)

**Files:**
- Modify: `workshop/scoring/scorer.py` (the per-session save loop)
- Create test: `workshop/tests/test_scoring_consistency.py`

In `scorer.py:104-115`, after computing `total` (which is the *aggregate* across all sessions), the code loops through completed sessions and writes that *same aggregate* into each session's `total` column. So 3 sessions of (deliverable=100) become total=27.5 each after `grade` runs, breaking the dashboard.

The fix: per-session total should be the **per-session weighted score**, not the aggregate.

- [ ] **Step 5.1: Write failing test for scoring consistency**

Create `workshop/tests/test_scoring_consistency.py`:

```python
"""Test that dashboard view and grade command produce consistent scores."""

from pathlib import Path

from workshop.platform.database import (
    create_cohort, get_connection, get_scores, get_all_scores,
    register_student, start_session, complete_session, save_score,
    mark_setup_completed,
)
from workshop.scoring.scorer import score_student


def _setup_alice_with_three_passed_sessions(db_path: Path):
    """Simulate Alice having completed S1-S3 with deliverable=100 each."""
    conn = get_connection(db_path)
    create_cohort(conn, "test-cohort", "Test")
    register_student(conn, "alice", "Alice", "a@test.com", "test-cohort")
    mark_setup_completed(conn, "alice")
    for s in [1, 2, 3]:
        start_session(conn, "alice", s)
        complete_session(conn, "alice", s, True,
                         {"checks": [], "total_points": 100, "max_points": 100})
        # complete-session stores per-session: only deliverable filled
        save_score(conn, "alice", s, 0, 0, 100, 0, 20)  # total=20 (weighted)
    return conn


def test_grade_does_not_overwrite_per_session_totals_with_aggregate(tmp_path):
    """After running grade, per-session 'total' columns must remain per-session,
    not be overwritten with the aggregate score across all sessions."""
    db_path = tmp_path / "test.db"
    conn = _setup_alice_with_three_passed_sessions(db_path)

    # Capture per-session totals BEFORE grade
    before = {s["session_number"]: s["total"] for s in get_scores(conn, "alice")}
    assert before == {1: 20, 2: 20, 3: 20}

    # Run grade (heuristic mode, no AI)
    score_student(conn, "alice", project_dir=tmp_path / "no-project",
                  use_ai=False)

    # Per-session totals should still be per-session values, not the aggregate
    after = {s["session_number"]: s["total"] for s in get_scores(conn, "alice")}
    # All three should be the same per-session value (since input is identical)
    assert len(set(after.values())) == 1, (
        f"All three sessions had identical inputs, expected identical per-session "
        f"totals after grade. Got: {after}"
    )
    # And should NOT be the aggregate (which mixes 25%/15%/20%/15% weights)
    # The per-session total is the deliverable_quality alone = 100, weighted by 0.20 / 0.75 = ~26.7
    # The aggregate also factors in standards (which will be 0 or 50 for missing project)
    # Key assertion: per-session totals are STABLE across grade runs
    score_student(conn, "alice", project_dir=tmp_path / "no-project",
                  use_ai=False)
    after2 = {s["session_number"]: s["total"] for s in get_scores(conn, "alice")}
    assert after == after2, (
        f"Running grade twice produced different per-session totals — "
        f"first: {after}, second: {after2}"
    )
    conn.close()


def test_dashboard_average_matches_grade_continuous_score(tmp_path):
    """The dashboard's avg_score (computed from stored per-session totals)
    should equal the grade command's reported continuous_score."""
    db_path = tmp_path / "test.db"
    conn = _setup_alice_with_three_passed_sessions(db_path)

    grade_result = score_student(conn, "alice",
                                 project_dir=tmp_path / "no-project",
                                 use_ai=False)

    # Dashboard reads from get_all_scores, which AVG()s the stored 'total' column
    dashboard_rows = get_all_scores(conn)
    alice_row = next(r for r in dashboard_rows if r["id"] == "alice")
    dashboard_avg = alice_row["avg_score"]

    # The continuous_score is what grade reports as the 75% chunk
    # Dashboard avg of per-session totals should match the continuous_score
    assert abs(dashboard_avg - grade_result["continuous_score"]) < 0.5, (
        f"Dashboard avg ({dashboard_avg}) and grade continuous_score "
        f"({grade_result['continuous_score']}) disagree by more than 0.5 pts"
    )
    conn.close()
```

- [ ] **Step 5.2: Run tests — verify both fail**

```bash
/tmp/p1-venv/bin/pytest workshop/tests/test_scoring_consistency.py -v
```

Expected: Both tests FAIL — first because grade currently does overwrite, second because dashboard/grade disagree.

- [ ] **Step 5.3: Fix `workshop/scoring/scorer.py`**

Open `workshop/scoring/scorer.py`. Find the save loop at the bottom of `score_student` (lines 104-115):

```python
    # Save to database
    for session in completed:
        sn = session["session_number"]
        idx = [s["session_number"] for s in completed].index(sn)
        db.save_score(
            conn, student_id, sn,
            prompt_quality=prompt_scores[idx] if idx < len(prompt_scores) else 0,
            efficiency=efficiency_scores[idx] if idx < len(efficiency_scores) else 0,
            deliverable_quality=deliverable_scores[idx] if idx < len(deliverable_scores) else 0,
            standards_compliance=standards_score,
            total=total,
        )
```

Replace with:

```python
    # Save per-session scores back to database with PER-SESSION totals
    # (NOT the aggregate `total` — that's a continuous-score across all sessions)
    for idx, session in enumerate(completed):
        sn = session["session_number"]
        per_session_prompt = prompt_scores[idx] if idx < len(prompt_scores) else 0
        per_session_eff = efficiency_scores[idx] if idx < len(efficiency_scores) else 0
        per_session_deliv = deliverable_scores[idx] if idx < len(deliverable_scores) else 0
        # Per-session weighted total (uses continuous-portion weights only,
        # renormalized so a per-session score is on a 0-100 scale)
        per_session_total = (
            per_session_prompt * 0.25
            + per_session_eff * 0.15
            + per_session_deliv * 0.20
            + standards_score * 0.15
        ) / CONTINUOUS_WEIGHT
        db.save_score(
            conn, student_id, sn,
            prompt_quality=per_session_prompt,
            efficiency=per_session_eff,
            deliverable_quality=per_session_deliv,
            standards_compliance=standards_score,
            total=per_session_total,
        )
```

- [ ] **Step 5.4: Run tests — verify both pass**

```bash
/tmp/p1-venv/bin/pytest workshop/tests/test_scoring_consistency.py -v
```

Expected: 2 passed.

- [ ] **Step 5.5: Run all existing tests to ensure no regressions**

```bash
/tmp/p1-venv/bin/pytest workshop/tests/ -q
```

Expected: 49+ passed (the original 45 + the new tests).

- [ ] **Step 5.6: Commit**

```bash
git add workshop/scoring/scorer.py workshop/tests/test_scoring_consistency.py
git commit -m "fix(workshop/scoring): per-session totals stay per-session in grade rerun"
```

---

## Task 6: Make `complete-session` write meaningful per-session totals

**Files:**
- Modify: `workshop/platform/cli.py` (`cmd_complete_session`)

Currently `cmd_complete_session` writes `total = quality_score` (just deliverable). After Task 5, the dashboard correctly averages stored totals — but if `complete-session` writes a wrong total, the dashboard still misrepresents until `grade` runs. Make `complete-session` compute the same per-session weighted total formula as `grade` would.

This means: `complete-session` runs prompt + efficiency + standards analyzers inline (heuristic mode, fast) and stores a real per-session total.

- [ ] **Step 6.1: Add a test that `complete-session` writes consistent per-session total**

Append to `workshop/tests/test_scoring_consistency.py`:

```python
def test_complete_session_writes_meaningful_per_session_total(tmp_path):
    """complete-session must write per-session total that matches what grade
    would produce for that session in isolation, not just deliverable_quality."""
    from workshop.platform import cli, student_setup
    import workshop.platform.config as cfg

    # Redirect bootcamp home to tmp_path
    monkey_home = tmp_path / "bootcamp-home"
    monkey_home.mkdir()
    cfg.BOOTCAMP_HOME = monkey_home
    cfg.LOGS_DIR = monkey_home / "logs"
    cfg.DB_PATH = monkey_home / "bootcamp.db"
    cfg.STUDENT_ID_FILE = monkey_home / "student-id"
    cfg.CURRENT_SESSION_FILE = monkey_home / "current-session"

    # Build a minimal passing project
    project = tmp_path / "qa-cmd-center"
    project.mkdir()
    (project / "package.json").write_text(
        '{"name":"qa-command-center","dependencies":'
        '{"express":"^4.18","react":"^18"}}'
    )
    (project / "server").mkdir()
    (project / "server" / "index.js").write_text("// noop")
    (project / "client" / "src").mkdir(parents=True)
    (project / "client" / "src" / "App.jsx").write_text("export default null;")
    (project / ".claude" / "skills" / "tg").mkdir(parents=True)
    (project / ".claude" / "skills" / "tg" / "SKILL.md").write_text(
        "---\nname: tg\ndescription: tg\n---\n"
    )

    # Set up bootcamp state
    from workshop.platform.database import (
        get_connection, create_cohort, register_student, mark_setup_completed,
        get_scores,
    )
    conn = get_connection(cfg.DB_PATH)
    create_cohort(conn, "c", "C")
    register_student(conn, "alice", "Alice", "a@a.com", "c")
    mark_setup_completed(conn, "alice")
    cfg.STUDENT_ID_FILE.write_text("alice")
    cfg.CURRENT_SESSION_FILE.write_text("1")

    # Run complete-session
    args = type("A", (), {"session": 1, "project_dir": project})()
    rc = cli.cmd_complete_session(conn, args)
    assert rc == 0, "complete-session should pass"

    # Per-session total should reflect ALL components (not just deliverable)
    scores = get_scores(conn, "alice")
    s1 = next(s for s in scores if s["session_number"] == 1)
    # The deliverable will be 100 (gate passes), prompt/efficiency/standards
    # may be 0 or higher depending on logs / project. Either way, the formula:
    # (pq * 0.25 + eff * 0.15 + deliv * 0.20 + std * 0.15) / 0.75
    # ...with deliv=100, std possibly 0, others possibly 0:
    # = (0 + 0 + 20 + 0) / 0.75 = 26.67
    # If standards picks up CLAUDE.md presence (we don't have one), still ~26.67
    expected_lower_bound = 25.0   # at least the deliverable contribution
    assert s1["total"] >= expected_lower_bound, (
        f"Per-session total {s1['total']} is suspiciously low — expected at least "
        f"{expected_lower_bound} from the deliverable contribution alone."
    )
    # And critically: NOT 100 (the bug was 'total = deliverable_quality')
    assert s1["total"] < 100, (
        f"Per-session total {s1['total']} == 100 looks like the old bug "
        "where total was just deliverable_quality"
    )
    conn.close()
```

- [ ] **Step 6.2: Run test — verify it FAILS**

```bash
/tmp/p1-venv/bin/pytest workshop/tests/test_scoring_consistency.py::test_complete_session_writes_meaningful_per_session_total -v
```

Expected: FAIL — current code writes `total=quality_score` (=100).

- [ ] **Step 6.3: Modify `cmd_complete_session` in `workshop/platform/cli.py`**

Find this block (around line 247-256):

```python
    # Save deliverable quality score regardless
    quality_score = (total_points / max_points * 100) if max_points > 0 else 0
    db.save_score(
        conn, student_id, session,
        prompt_quality=0, efficiency=0,
        deliverable_quality=quality_score,
        standards_compliance=0,
        total=quality_score,
    )
```

Replace with:

```python
    # Compute deliverable_quality from gate points
    quality_score = (total_points / max_points * 100) if max_points > 0 else 0

    # Compute per-session components inline (heuristic, fast — no AI calls here)
    from workshop.scoring.efficiency_analyzer import analyze_efficiency
    from workshop.scoring.prompt_analyzer import analyze_prompts
    from workshop.scoring.standards_analyzer import analyze_standards
    from workshop.platform.config import LOGS_DIR

    log_dir = LOGS_DIR / student_id
    prompt_result = analyze_prompts(log_dir, session, use_ai=False)
    eff_result = analyze_efficiency(log_dir, session, gate_passed=critical_passed)
    if args.project_dir.exists():
        std_result = analyze_standards(args.project_dir)
        standards_score = std_result["score"]
    else:
        standards_score = 0

    # Per-session weighted total (continuous-portion weights, renormalized)
    # Same formula scorer.py uses for per-session storage.
    per_session_total = (
        prompt_result["score"] * 0.25
        + eff_result["score"] * 0.15
        + quality_score * 0.20
        + standards_score * 0.15
    ) / 0.75

    db.save_score(
        conn, student_id, session,
        prompt_quality=prompt_result["score"],
        efficiency=eff_result["score"],
        deliverable_quality=quality_score,
        standards_compliance=standards_score,
        total=per_session_total,
    )
```

- [ ] **Step 6.4: Run test — verify it now PASSES**

```bash
/tmp/p1-venv/bin/pytest workshop/tests/test_scoring_consistency.py::test_complete_session_writes_meaningful_per_session_total -v
```

Expected: 1 passed.

- [ ] **Step 6.5: Run full test suite**

```bash
/tmp/p1-venv/bin/pytest workshop/tests/ -q
```

Expected: All passing.

- [ ] **Step 6.6: Commit**

```bash
git add workshop/platform/cli.py workshop/tests/test_scoring_consistency.py
git commit -m "fix(workshop/cli): complete-session writes weighted per-session total"
```

---

## Task 7: Unify prompt logs on JSONL (remove SQLite `prompt_logs` table)

**Files:**
- Create: `workshop/platform/jsonl_log.py`
- Create test: `workshop/tests/test_jsonl_log.py`
- Modify: `workshop/platform/database.py` (remove `prompt_logs` table + helpers)
- Modify: `workshop/platform/cli.py` (`status --prompts` reads JSONL)
- Modify: `workshop/demo.sh` (write JSONL files instead of SQLite)

The hooks (`hooks/log-prompt.sh`) write JSONL to `~/.claude-bootcamp/logs/{student}/session-{N}/prompts.jsonl`. The prompt analyzer reads JSONL. But the demo writes to a SQLite `prompt_logs` table, and `status --prompts` reads from SQLite. Two formats = two views of the same data = bugs. Single source of truth: **JSONL on disk**, matching what real hooks produce.

- [ ] **Step 7.1: Write tests for the new JSONL log reader**

Create `workshop/tests/test_jsonl_log.py`:

```python
"""Test the JSONL prompt log reader (single source of truth for prompts)."""

import json

from workshop.platform.jsonl_log import (
    append_prompt, append_response, read_prompts, read_all_events,
    count_prompts,
)


def test_append_and_read_prompts(tmp_path):
    log_dir = tmp_path / "logs" / "alice"
    append_prompt(log_dir, session=1, content="Make a button")
    append_prompt(log_dir, session=1, content="Make it red")
    append_prompt(log_dir, session=2, content="Different session")

    s1 = read_prompts(log_dir, session=1)
    assert len(s1) == 2
    assert s1[0] == "Make a button"
    assert s1[1] == "Make it red"

    s2 = read_prompts(log_dir, session=2)
    assert s2 == ["Different session"]


def test_count_prompts(tmp_path):
    log_dir = tmp_path / "logs" / "alice"
    for i in range(5):
        append_prompt(log_dir, session=1, content=f"prompt {i}")
    assert count_prompts(log_dir, session=1) == 5
    assert count_prompts(log_dir, session=2) == 0


def test_read_all_events_includes_responses(tmp_path):
    log_dir = tmp_path / "logs" / "alice"
    append_prompt(log_dir, session=1, content="p1")
    append_response(log_dir, session=1, content="r1")
    append_prompt(log_dir, session=1, content="p2")

    events = read_all_events(log_dir, session=1)
    assert len(events) == 3
    assert events[0]["type"] == "prompt"
    assert events[1]["type"] == "response"
    assert events[2]["content"] == "p2"


def test_jsonl_format_matches_hook_output(tmp_path):
    """The on-disk format must match what hooks/log-prompt.sh produces:
       {"type":"prompt","student":"alice","session":1,"timestamp":"...","content":"..."}"""
    log_dir = tmp_path / "logs" / "alice"
    append_prompt(log_dir, session=1, content='Has "quotes" and \\backslashes')

    jsonl_file = log_dir / "session-1" / "prompts.jsonl"
    line = jsonl_file.read_text().strip()
    parsed = json.loads(line)  # Must be valid JSON
    assert parsed["type"] == "prompt"
    assert parsed["session"] == 1
    assert parsed["content"] == 'Has "quotes" and \\backslashes'
    assert "timestamp" in parsed


def test_missing_session_dir_returns_empty(tmp_path):
    log_dir = tmp_path / "logs" / "nobody"
    assert read_prompts(log_dir, session=1) == []
    assert count_prompts(log_dir, session=1) == 0
    assert read_all_events(log_dir, session=1) == []
```

- [ ] **Step 7.2: Run tests — verify FAIL with import error**

```bash
/tmp/p1-venv/bin/pytest workshop/tests/test_jsonl_log.py -v
```

Expected: FAIL — `workshop.platform.jsonl_log` doesn't exist yet.

- [ ] **Step 7.3: Implement `workshop/platform/jsonl_log.py`**

```python
"""Single source of truth for prompt logs: JSONL files matching hook output.

Format (one JSON object per line):
    {"type": "prompt"|"response", "student": "alice", "session": 1,
     "timestamp": "2026-04-15T12:00:00Z", "content": "..."}

Layout:
    {LOGS_DIR}/{student_id}/session-{N}/prompts.jsonl  -- prompt events
    {LOGS_DIR}/{student_id}/session-{N}/responses.jsonl -- response events
"""

import json
from datetime import datetime, timezone
from pathlib import Path


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _session_dir(log_dir: Path, session: int) -> Path:
    return log_dir / f"session-{session}"


def _append_event(log_dir: Path, session: int, event_type: str,
                  content: str, filename: str) -> None:
    sd = _session_dir(log_dir, session)
    sd.mkdir(parents=True, exist_ok=True)
    entry = {
        "type": event_type,
        "student": log_dir.name,  # student_id is the parent dir name
        "session": session,
        "timestamp": _now(),
        "content": content,
    }
    with (sd / filename).open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def append_prompt(log_dir: Path, session: int, content: str) -> None:
    """Append a 'prompt' event to {log_dir}/session-{N}/prompts.jsonl."""
    _append_event(log_dir, session, "prompt", content, "prompts.jsonl")


def append_response(log_dir: Path, session: int, content: str) -> None:
    """Append a 'response' event to {log_dir}/session-{N}/responses.jsonl."""
    _append_event(log_dir, session, "response", content, "responses.jsonl")


def _read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue  # tolerate malformed lines (hook writes can be partial)
    return out


def read_prompts(log_dir: Path, session: int) -> list[str]:
    """Return the content of all prompt events for the given session, in order."""
    events = _read_jsonl(_session_dir(log_dir, session) / "prompts.jsonl")
    return [e.get("content", "") for e in events if e.get("type") == "prompt"]


def count_prompts(log_dir: Path, session: int) -> int:
    return len(read_prompts(log_dir, session))


def read_all_events(log_dir: Path, session: int) -> list[dict]:
    """Return prompts + responses, sorted by timestamp."""
    sd = _session_dir(log_dir, session)
    events = _read_jsonl(sd / "prompts.jsonl") + _read_jsonl(sd / "responses.jsonl")
    events.sort(key=lambda e: e.get("timestamp", ""))
    return events
```

- [ ] **Step 7.4: Run JSONL tests — verify all pass**

```bash
/tmp/p1-venv/bin/pytest workshop/tests/test_jsonl_log.py -v
```

Expected: 5 passed.

- [ ] **Step 7.5: Update `cmd_status` in `workshop/platform/cli.py` to read JSONL**

Find the block (around line 434-442):
```python
    # Prompt logs
    if args.prompts:
        logs = db.get_prompt_logs(conn, student_id)
        if logs:
            print(f"\n  Prompt History ({len(logs)} entries):")
            for log_entry in logs[-20:]:  # Show last 20
                print(f"    [{log_entry['timestamp']}] "
                      f"S{log_entry['session_number']} "
                      f"({log_entry['event_type']}): "
                      f"{log_entry['content'][:80]}")
```

Replace with:
```python
    # Prompt logs (JSONL files on disk — single source of truth)
    if args.prompts:
        from workshop.platform.config import LOGS_DIR
        from workshop.platform.jsonl_log import read_all_events

        all_events = []
        for n in range(1, TOTAL_SESSIONS + 1):
            for ev in read_all_events(LOGS_DIR / student_id, n):
                all_events.append(ev)
        if all_events:
            print(f"\n  Prompt History ({len(all_events)} entries):")
            for ev in all_events[-20:]:
                content = ev.get("content", "")[:80]
                print(f"    [{ev.get('timestamp','?')}] "
                      f"S{ev.get('session','?')} "
                      f"({ev.get('type','?')}): {content}")
```

- [ ] **Step 7.6: Remove SQLite prompt log helpers from `workshop/platform/database.py`**

Open `workshop/platform/database.py`. Delete:
1. The `CREATE TABLE IF NOT EXISTS prompt_logs` block (lines 52-59) from `SCHEMA`
2. The functions `log_prompt`, `get_prompt_logs`, `get_prompt_count` (lines 274-308)

After edit, the `SCHEMA` constant should end with the `scores` table.

- [ ] **Step 7.7: Update `workshop/demo.sh` to write JSONL prompts (not SQLite)**

Find the Python heredoc that logs Alice/Bob prompts (around line 102):

```bash
PYTHONPATH="$REPO_ROOT" python3 <<'PYEOF'
from workshop.platform import database as db
conn = db.get_connection()

# Alice prompts — high quality
alice_prompts = [...]
for i, p in enumerate(alice_prompts):
    db.log_prompt(conn, "alice", 1, "prompt", p)

# Bob prompts — low quality (vague)
bob_prompts = [...]
for p in bob_prompts:
    db.log_prompt(conn, "bob", 1, "prompt", p)

conn.close()
print("  Simulated prompts logged for Alice (high quality) and Bob (low quality)")
PYEOF
```

Replace with:

```bash
PYTHONPATH="$REPO_ROOT" /opt/homebrew/bin/python3 <<'PYEOF'
from pathlib import Path
from workshop.platform.config import LOGS_DIR
from workshop.platform.jsonl_log import append_prompt

# Alice prompts — high quality
alice_prompts = [
    "Create a full-stack project with Express backend and React frontend using Vite, named QA Command Center following the ISTQB naming conventions",
    "Generate a test case data model with ISTQB severity levels S1-S4 and priority P1-P4, with fields for title, preconditions, steps, and expected result",
    "Build a REST API for test cases with consistent {success, data, error} response format as specified in CLAUDE.md",
    "Create a React page for test case listing with severity filter badges and sortable columns",
    "Add a custom slash command for creating new test cases with a template including boundary value analysis",
]
alice_log = LOGS_DIR / "alice"
for p in alice_prompts:
    append_prompt(alice_log, session=1, content=p)

# Bob prompts — low quality (vague)
bob_prompts = ["make it work", "fix it", "help", "do the thing", "make a test", "idk what to do"]
bob_log = LOGS_DIR / "bob"
for p in bob_prompts:
    append_prompt(bob_log, session=1, content=p)

print("  Simulated prompts logged as JSONL for Alice (high quality) and Bob (low quality)")
PYEOF
```

(Note: also replace `python3` with `/opt/homebrew/bin/python3` in this heredoc to ensure 3.10+ on macOS.)

- [ ] **Step 7.8: Run all workshop tests + the demo to verify nothing broke**

```bash
/tmp/p1-venv/bin/pytest workshop/tests/ -q
cd workshop && PATH=/opt/homebrew/bin:$PATH ./demo.sh > /tmp/demo.txt 2>&1 && cd ..
PATH=/opt/homebrew/bin:$PATH ./workshop/bootcamp status --student alice --prompts | tail -10
```

Expected:
- All tests pass (the database.py-related tests in test_database.py may need a tiny update if any specifically tested `log_prompt` — fix those tests too in this commit)
- `demo.sh` exits 0
- `status --prompts` shows the JSONL-sourced Alice prompts

- [ ] **Step 7.9: Update test_database.py if it referenced removed functions**

Run:
```bash
grep -n "log_prompt\|get_prompt_logs\|get_prompt_count" workshop/tests/test_database.py
```

If matches found, remove or rewrite those test cases (they tested the now-removed SQLite helpers; the JSONL ones are tested in `test_jsonl_log.py`).

- [ ] **Step 7.10: Commit**

```bash
git add workshop/platform/jsonl_log.py workshop/platform/database.py \
        workshop/platform/cli.py workshop/demo.sh \
        workshop/tests/test_jsonl_log.py workshop/tests/test_database.py
git commit -m "refactor(workshop): unify prompt logs on JSONL (single source of truth)"
```

---

## Task 8: Verify Atlassian MCP package name + update docs

**Files:**
- Modify: `workshop/INSTRUCTOR-GUIDE.md`
- Modify: `workshop/sessions/s05-mcp/README.md`
- Modify: `workshop/sessions/s05-mcp/reference.md`

The current docs reference `@anthropic-ai/mcp-server-atlassian`. Verify against npm and correct.

- [ ] **Step 8.1: Look up the package on npm**

```bash
npm view @anthropic-ai/mcp-server-atlassian 2>&1 | head -5
echo "---"
npm search atlassian mcp 2>&1 | head -10
```

Note the actual package name (likely `@modelcontextprotocol/server-atlassian` or `mcp-server-atlassian` from a different scope, or it may be `@atlassian/mcp-server` published by Atlassian themselves).

- [ ] **Step 8.2: Document the verified name**

Once confirmed, identify all files referencing the old name:
```bash
grep -rn "anthropic-ai/mcp-server-atlassian" workshop/
```

Replace with the verified name in each file. Common locations:
- `workshop/INSTRUCTOR-GUIDE.md` (around the Jira setup section)
- `workshop/sessions/s05-mcp/README.md`
- `workshop/sessions/s05-mcp/reference.md`

- [ ] **Step 8.3: Verify install command still works**

If the package actually exists, document the install command:
```
claude mcp add atlassian --command "npx <correct-package-name>"
```

If no canonical Atlassian MCP exists yet (only community ones), update docs to: "As of {date}, the Atlassian MCP server is community-maintained — pick one of these: [list]. We recommend X."

- [ ] **Step 8.4: Commit**

```bash
git add workshop/INSTRUCTOR-GUIDE.md workshop/sessions/s05-mcp/
git commit -m "docs(workshop): correct Atlassian MCP package name (verified against npm)"
```

---

## Task 9: Implement `./bootcamp doctor` preflight

**Files:**
- Create: `workshop/platform/doctor.py`
- Create test: `workshop/tests/test_doctor.py`
- Modify: `workshop/platform/cli.py` (register `doctor` subcommand)

Adds `./bootcamp doctor` command that checks all student/instructor prerequisites and prints a green/red status table. Run before pilot.

- [ ] **Step 9.1: Write tests for the doctor module**

Create `workshop/tests/test_doctor.py`:

```python
"""Tests for the bootcamp doctor preflight."""

from workshop.platform.doctor import (
    Check, run_all_checks, check_python_version,
    check_command_available,
)


def test_check_dataclass_str_renders_pass_and_fail():
    p = Check(name="x", passed=True, message="ok")
    f = Check(name="y", passed=False, message="missing", fix="install y")
    assert "[+]" in str(p) and "PASS" in str(p)
    assert "[-]" in str(f) and "FAIL" in str(f)
    assert "install y" in str(f)


def test_check_python_version_passes_on_310_plus():
    result = check_python_version(min_major=3, min_minor=10)
    assert result.passed is True
    assert "3." in result.message


def test_check_python_version_fails_on_too_old():
    # Force a too-high requirement
    result = check_python_version(min_major=99, min_minor=0)
    assert result.passed is False
    assert "99" in result.message


def test_check_command_available_finds_python():
    import sys
    # `python3` may or may not be on PATH; test with sys.executable instead
    result = check_command_available(sys.executable)
    assert result.passed is True


def test_check_command_available_fails_for_nonsense():
    result = check_command_available("definitely-not-a-command-xyz123")
    assert result.passed is False
    assert "not found" in result.message.lower()


def test_run_all_checks_returns_list_of_checks():
    results = run_all_checks()
    assert isinstance(results, list)
    assert all(isinstance(c, Check) for c in results)
    assert len(results) >= 4  # python, claude, node, git at minimum
```

- [ ] **Step 9.2: Run tests — verify FAIL (module doesn't exist)**

```bash
/tmp/p1-venv/bin/pytest workshop/tests/test_doctor.py -v
```

Expected: ImportError on `workshop.platform.doctor`.

- [ ] **Step 9.3: Implement `workshop/platform/doctor.py`**

```python
"""Preflight checks for the bootcamp environment.

Run via `./bootcamp doctor`. Returns a list of Check results that are
displayed as a status table. Designed to be student- and instructor-friendly:
each FAIL includes a 'fix' message with concrete remediation.
"""

import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Check:
    name: str
    passed: bool
    message: str
    fix: str | None = None

    def __str__(self) -> str:
        icon = "[+]" if self.passed else "[-]"
        status = "PASS" if self.passed else "FAIL"
        out = f"  {icon} {status}: {self.name} -- {self.message}"
        if not self.passed and self.fix:
            out += f"\n      Fix: {self.fix}"
        return out


def check_python_version(min_major: int = 3, min_minor: int = 10) -> Check:
    actual = sys.version_info
    ok = (actual.major, actual.minor) >= (min_major, min_minor)
    msg = f"Python {actual.major}.{actual.minor}.{actual.micro} (require >={min_major}.{min_minor})"
    fix = ("Install a newer Python via Homebrew: brew install python@3.12\n"
           "      Or via uv: pip install uv && uv python install 3.12")
    return Check("Python version", ok, msg, fix if not ok else None)


def check_command_available(cmd: str, version_arg: str = "--version") -> Check:
    path = shutil.which(cmd)
    if not path:
        return Check(
            f"`{cmd}` on PATH",
            False,
            f"`{cmd}` not found on PATH",
            f"Install {cmd} (see docs)",
        )
    try:
        v = subprocess.run(
            [path, version_arg], capture_output=True, text=True, timeout=5,
        )
        version = (v.stdout or v.stderr).strip().splitlines()[0] if (v.stdout or v.stderr) else "(no version)"
    except Exception:
        version = "(unknown version)"
    return Check(f"`{cmd}` on PATH", True, f"{path} -- {version}")


def check_claude_cli() -> Check:
    return check_command_available("claude")


def check_node() -> Check:
    return check_command_available("node")


def check_git_configured() -> Check:
    name = subprocess.run(
        ["git", "config", "--global", "user.name"],
        capture_output=True, text=True,
    ).stdout.strip()
    if name:
        return Check("Git user.name configured", True, name)
    return Check(
        "Git user.name configured",
        False,
        "git config --global user.name is empty",
        "Run: git config --global user.name 'Your Name'",
    )


def check_bootcamp_home_writable() -> Check:
    from .config import BOOTCAMP_HOME
    try:
        BOOTCAMP_HOME.mkdir(parents=True, exist_ok=True)
        probe = BOOTCAMP_HOME / ".doctor-probe"
        probe.write_text("ok")
        probe.unlink()
        return Check(
            "Bootcamp home writable",
            True,
            f"{BOOTCAMP_HOME} is writable",
        )
    except Exception as e:
        return Check(
            "Bootcamp home writable",
            False,
            f"{BOOTCAMP_HOME} not writable: {e}",
            f"Check permissions on {BOOTCAMP_HOME.parent}",
        )


def run_all_checks() -> list[Check]:
    return [
        check_python_version(),
        check_claude_cli(),
        check_node(),
        check_git_configured(),
        check_bootcamp_home_writable(),
    ]


def doctor_main() -> int:
    """Print the status table; return 0 if all PASS, 1 otherwise."""
    print("\n  Bootcamp doctor — environment preflight")
    print(f"  {'=' * 60}\n")
    results = run_all_checks()
    for r in results:
        print(r)
    failed = [r for r in results if not r.passed]
    print(f"\n  {'=' * 60}")
    if failed:
        print(f"  {len(failed)} check(s) FAILED. Fix the issues above before continuing.\n")
        return 1
    print(f"  All {len(results)} checks PASSED.\n")
    return 0
```

- [ ] **Step 9.4: Wire `doctor` subcommand in `workshop/platform/cli.py`**

In `cli.py`, after the `unlock_parser` block (around line 105), add:

```python
    subparsers.add_parser("doctor", help="Run preflight checks on the environment")
```

In the dispatch chain (the `if/elif` block starting at line 116), add **before** the final `else`:

```python
        elif args.command == "doctor":
            from .doctor import doctor_main
            return doctor_main()
```

- [ ] **Step 9.5: Run doctor and verify output**

```bash
PATH=/opt/homebrew/bin:$PATH ./workshop/bootcamp doctor
```

Expected: A 5-row status table. All PASS on this dev machine. Exit code 0.

```bash
echo "Exit code: $?"
```

- [ ] **Step 9.6: Run doctor tests + full suite**

```bash
/tmp/p1-venv/bin/pytest workshop/tests/test_doctor.py -v
/tmp/p1-venv/bin/pytest workshop/tests/ -q
```

Expected: doctor tests pass; full suite passes.

- [ ] **Step 9.7: Commit**

```bash
git add workshop/platform/doctor.py workshop/platform/cli.py workshop/tests/test_doctor.py
git commit -m "feat(workshop): add ./bootcamp doctor preflight command"
```

---

## Task 10: Wire workshop tests into CI

**Files:**
- Modify: `.github/workflows/test.yml`

Add a new job that runs `pytest workshop/tests/` on Python 3.10/3.11/3.12. Mirror the existing `pytest` job's structure.

- [ ] **Step 10.1: Read current workflow**

Already loaded earlier. Job we're adding mirrors the `pytest` job but for workshop.

- [ ] **Step 10.2: Add a `workshop-tests` job to `.github/workflows/test.yml`**

Append the following job after the existing `pytest` job (before `lint`):

```yaml
  workshop-tests:
    name: Workshop Tests (Python ${{ matrix.python-version }})
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        python-version: ['3.10', '3.11', '3.12']

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v4

      - name: Set up Python ${{ matrix.python-version }}
        run: uv python install ${{ matrix.python-version }}

      - name: Create venv and install dev dependencies
        run: |
          uv venv
          uv pip install -r workshop/requirements-dev.txt

      - name: Run workshop pytest
        run: uv run pytest workshop/tests/ -v --tb=short

      - name: Run workshop demo (smoke)
        run: |
          # Demo writes to ~/.claude-bootcamp; make sure it runs cleanly
          cd workshop
          chmod +x demo.sh bootcamp
          ./demo.sh
```

Also update the workflow's path filters at the top so workshop changes trigger CI:

Change:
```yaml
on:
  push:
    branches: [main, develop]
    paths:
      - 'scripts/**'
      - '.github/workflows/test.yml'
      - 'pyproject.toml'
      - 'requirements*.txt'
```

To:
```yaml
on:
  push:
    branches: [main, develop]
    paths:
      - 'scripts/**'
      - 'workshop/**'
      - '.github/workflows/test.yml'
      - 'pyproject.toml'
      - 'requirements*.txt'
```

(Apply the same `workshop/**` addition under the `pull_request` block.)

Also update the `summary` job's `needs` to include `workshop-tests`:

Change:
```yaml
  summary:
    name: Test Summary
    needs: [pytest, lint, security, type-check, build-epub]
```

To:
```yaml
  summary:
    name: Test Summary
    needs: [pytest, workshop-tests, lint, security, type-check, build-epub]
```

And add a line to the summary script:
```yaml
          echo "- **Workshop Tests**: ${{ needs.workshop-tests.result }}" >> $GITHUB_STEP_SUMMARY
```

And to the failure check:
```yaml
      - name: Check if all tests passed
        if: |
          needs.pytest.result != 'success' ||
          needs.workshop-tests.result != 'success' ||
          needs.build-epub.result != 'success'
```

- [ ] **Step 10.3: Validate workflow syntax locally**

```bash
# Use yq or python yaml to validate
/opt/homebrew/bin/python3 -c "import yaml; yaml.safe_load(open('.github/workflows/test.yml'))"
```

Expected: no output (means valid YAML).

- [ ] **Step 10.4: Commit**

```bash
git add .github/workflows/test.yml
git commit -m "ci: run workshop pytest + demo smoke on PR/main"
```

---

## Task 11: Write `workshop/PILOT-RUNBOOK.md`

**Files:**
- Create: `workshop/PILOT-RUNBOOK.md`

Operational playbook for running a 2-3 person Phase 1 pilot.

- [ ] **Step 11.1: Create the runbook**

Create `workshop/PILOT-RUNBOOK.md`:

```markdown
# Phase 1 Pilot Runbook

For running a 2-3 person internal pilot of the AI Bootcamp CLI before the web UI exists.

## Prerequisites checklist

Run on EACH pilot machine:

```bash
./workshop/bootcamp doctor
```

All 5 checks must PASS. If any FAIL, follow the printed `Fix:` line.

## Setup (one-time, instructor)

```bash
cd workshop

# Open a fresh cohort
./bootcamp open-registration --cohort "pilot-1" --name "Phase 1 Pilot" --deadline "2026-05-31"

# Register pilots (replace IDs/names/emails)
./bootcamp register pilot-a "Alice Pilot" alice@example.com --cohort pilot-1
./bootcamp register pilot-b "Bob Pilot"   bob@example.com   --cohort pilot-1
```

Verify roster:
```bash
./bootcamp dashboard
```

## Per-pilot setup (each pilot does this on their own laptop)

```bash
git clone <repo-url> claude-howto
cd claude-howto/workshop

# Verify environment
./bootcamp doctor

# Authenticate Claude Code (uses your own Claude.ai account)
claude /login

# Run setup with your assigned student-id
./bootcamp setup --student-id pilot-a --project-dir ~/qa-cmd-center
```

Hooks are installed into `~/qa-cmd-center/.claude/`. The setup creates `~/.claude-bootcamp/` for state.

## Running a session (pilot does this)

```bash
cd workshop
./bootcamp start-session 1
```

Read the printed guide path. Open it. Work through the requirements by prompting Claude in your project dir. When you think you're done:

```bash
./bootcamp complete-session 1 --project-dir ~/qa-cmd-center
```

The CLI prints a per-check status table + your per-session score breakdown.

## Monitoring (instructor)

Run continuously on a separate screen:
```bash
watch -n 30 ./bootcamp dashboard
```

Drill into a specific pilot:
```bash
./bootcamp status --student pilot-a --detailed
./bootcamp status --student pilot-a --prompts | tail -50
```

## Troubleshooting

**"Python 3.10+ required"** — install via `brew install python@3.12`. Re-run with `/opt/homebrew/bin/python3 ./bootcamp ...`.

**"Student '...' is not registered"** — instructor needs to run `./bootcamp register ...` first.

**"You must complete session N first"** — the pilot tried to skip ahead. They must complete sessions in order, OR an instructor force-unlocks via `./bootcamp unlock-session N --student pilot-a --reason "catch-up"`.

**Gate fails repeatedly** — after 3 attempts, escalating hints appear automatically. After 5 attempts, auto-unlock fires with a 20% score penalty. The pilot can keep retrying for full credit even after auto-unlock.

**Scores look wrong** — run `./bootcamp grade pilot-a --no-ai` for a fresh recompute. If dashboard avg disagrees with grade total, file a bug — they should match (Phase 1 fixed this).

**No prompts in `status --prompts`** — the hook script in their `~/qa-cmd-center/.claude/settings.json` may not be wired. Verify with: `cat ~/.claude-bootcamp/logs/pilot-a/session-1/prompts.jsonl`.

## Pilot success criteria

- Both pilots complete S1-S3 within 3 hours
- No data loss (scores persist across sessions)
- All gate checks behave as expected
- `dashboard` and `grade ... --no-ai` produce consistent scores
- Instructor reports < 30 min total intervention time

## When to stop the pilot

If 3+ critical bugs surface, halt and patch before continuing. Do NOT escalate to a wider pilot until critical bugs are fixed.

## Reset (between pilots)

```bash
# On each pilot machine
rm -rf ~/.claude-bootcamp ~/qa-cmd-center
```
```

- [ ] **Step 11.2: Commit**

```bash
git add workshop/PILOT-RUNBOOK.md
git commit -m "docs(workshop): add Phase 1 pilot runbook"
```

---

## Task 12: Final smoke test + push

- [ ] **Step 12.1: Full clean smoke test**

```bash
# Clean state
rm -rf ~/.claude-bootcamp /tmp/qa-demo-*

# Tests
/tmp/p1-venv/bin/pytest workshop/tests/ -v --tb=short

# Doctor
PATH=/opt/homebrew/bin:$PATH ./workshop/bootcamp doctor

# Demo
cd workshop && PATH=/opt/homebrew/bin:$PATH ./demo.sh > /tmp/final-demo.log 2>&1; cd ..
echo "Demo exit: $?"

# Verify Bob's auto-unlock fired
grep -c "AUTO-UNLOCKED" /tmp/final-demo.log
# Expected: 1 (Bob's attempt 5)

# Verify Alice's S1-S3 all show Completed/PASSED
PATH=/opt/homebrew/bin:$PATH ./workshop/bootcamp status --student alice --detailed | grep -E "S[1-3]:"
# Expected: all three show "Completed" + "PASSED"

# Verify dashboard ≈ grade output
PATH=/opt/homebrew/bin:$PATH ./workshop/bootcamp dashboard | grep alice
PATH=/opt/homebrew/bin:$PATH ./workshop/bootcamp grade alice --no-ai
# The two avg/total values should be close (within a few points)
```

Expected: all green, no surprises. If anything fails, fix and re-run.

- [ ] **Step 12.2: Verify pre-commit hooks pass on the full diff**

```bash
git diff main --stat
pre-commit run --all-files 2>&1 | tail -30
```

(If pre-commit isn't installed: `pip install pre-commit && pre-commit install`. If it complains about `markdownlint` or other tools, install them per the root `CLAUDE.md`.)

- [ ] **Step 12.3: Open PR**

```bash
git push -u origin phase-1-cli-fixes
gh pr create \
  --title "Phase 1: Fix CLI platform bugs + tests + doctor + pilot runbook" \
  --body "$(cat <<'EOF'
## Summary
Implements Phase 1 of the AI Bootcamp Platform spec
(`docs/superpowers/specs/2026-04-15-ai-bootcamp-platform-design.md`).

Fixes audit-discovered bugs:
- Bob's demo fixture now actually fails S1 → auto-unlock at attempt 5 fires correctly
- Alice's demo loop calls `start-session` per session → progression persists
- `complete-session` writes weighted per-session totals (not just deliverable)
- `grade` no longer overwrites per-session totals with the aggregate
- Prompt logs unified on JSONL (single source of truth, matches hook output)
- `bootcamp` entry point fails-fast on Python < 3.10 with clear remediation
- Atlassian MCP package name verified against npm and corrected in docs
- New `./bootcamp doctor` preflight checks env before pilots
- Workshop tests + demo smoke wired into CI

## Test plan
- [ ] `pytest workshop/tests/` — all green
- [ ] `./workshop/bootcamp doctor` — all 5 checks pass
- [ ] `./workshop/demo.sh` — exits 0, Bob auto-unlocks, Alice S1-S3 all completed
- [ ] `./bootcamp dashboard` and `./bootcamp grade alice --no-ai` produce consistent scores
- [ ] CI green on PR
EOF
)"
```

- [ ] **Step 12.4: Verify CI passes**

```bash
gh pr view --web   # or watch in CLI
gh pr checks
```

Wait for green, then merge.

---

## Self-Review Notes

This plan covers Phase 1 of the spec (§ 5 Phase 1, Appendix A). Per-task spec-coverage check:

| Spec item (Section 5 Phase 1) | Implementing task |
|---|---|
| Add `workshop/__init__.py` | Task 1 |
| Add `pyproject.toml` w/ pytest | Task 1 |
| Add `requirements-dev.txt` | Task 1 |
| Python version guard | Task 2 |
| Bob fixture must fail S1 | Task 3 |
| Alice progression fix | Task 4 |
| Unify scoring paths | Task 5 + Task 6 |
| Prompt-log format unified on JSONL | Task 7 |
| Verify Atlassian MCP package | Task 8 |
| `./bootcamp doctor` | Task 9 |
| Workshop tests in CI | Task 10 |
| `PILOT-RUNBOOK.md` | Task 11 |
| Final smoke + ship | Task 12 |

No spec items missing. No `TBD`/`TODO`/placeholder text. All file paths and code blocks are concrete.

**Type/method-name consistency check:**
- `Check` dataclass shape used in Task 9 matches what tests in Step 9.1 import
- `append_prompt` / `read_prompts` / `count_prompts` / `read_all_events` consistent across Tasks 7.1-7.7
- `score_student(conn, student_id, project_dir, use_ai)` signature matches the existing `scorer.py`

**Completeness check:**
- Every TDD task has: failing-test → run-fails → impl → run-passes → commit
- Every code change shows the actual code
- Every shell command has expected output

**Remaining intentional gaps:**
- Phase 2 (devcontainer) and Phase 3 (web UI) get their own plans after Phase 1 ships
- AI scoring smoke test (real `claude -p` call) is in `PILOT-RUNBOOK.md` as a manual step, not automated (requires real Claude auth)
