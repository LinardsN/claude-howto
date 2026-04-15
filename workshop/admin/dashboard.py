"""Terminal-based instructor dashboard for real-time student monitoring."""

import json
import sys
import time
from pathlib import Path

from ..platform import database as db
from ..platform.config import (
    BOOTCAMP_HOME, GRADE_BANDS, LOGS_DIR, SESSION_NAMES, TOTAL_SESSIONS,
)


def run_dashboard(conn, refresh_interval: int = 5) -> None:
    """Run the real-time instructor dashboard."""
    print("\n  AI Bootcamp - Instructor Dashboard")
    print("  " + "=" * 60)
    print(f"  Database: {BOOTCAMP_HOME / 'bootcamp.db'}")
    print(f"  Refresh: every {refresh_interval}s (Ctrl+C to exit)\n")

    try:
        while True:
            _render_dashboard(conn)
            time.sleep(refresh_interval)
    except KeyboardInterrupt:
        print("\n  Dashboard closed.")


def _render_dashboard(conn) -> None:
    """Render one frame of the dashboard."""
    # Clear screen
    print("\033[2J\033[H", end="")

    print("  AI Bootcamp - Live Dashboard")
    print("  " + "=" * 70)

    # Cohort summary
    cohort = db.get_active_cohort(conn)
    if cohort:
        status = "OPEN" if cohort["registration_open"] else "CLOSED"
        print(f"  Cohort: {cohort['name']} | Registration: {status}")
        if cohort["deadline"]:
            print(f"  Deadline: {cohort['deadline']}")
    print()

    # Student table
    students = db.list_students(conn)
    if not students:
        print("  No students registered.")
        return

    print(f"  {'ID':<15} {'Name':<20} {'Session':<10} "
          f"{'Score':<8} {'Status':<15} {'Prompts':<8}")
    print(f"  {'-' * 76}")

    for student in students:
        sid = student["id"]
        last_session = db.get_last_completed_session(conn, sid)
        total_score = db.get_total_score(conn, sid)
        grade = _get_grade_label(total_score)

        # Count total prompts
        total_prompts = sum(
            db.get_prompt_count(conn, sid, i) for i in range(1, 11)
        )

        # Determine status
        if not student["setup_completed"]:
            status = "Setup Pending"
        elif last_session >= TOTAL_SESSIONS:
            status = "COMPLETED"
        elif last_session > 0:
            current = last_session + 1
            session_name = SESSION_NAMES.get(current, f"S{current}")
            status = f"Working: S{current}"
        else:
            status = "Not Started"

        score_str = f"{total_score:.0f}" if total_score > 0 else "-"

        print(f"  {sid:<15} {student['name']:<20} "
              f"S{last_session:<9} {score_str:<8} "
              f"{status:<15} {total_prompts:<8}")

    print(f"\n  Total students: {len(students)}")

    # Session distribution
    session_counts = {}
    for student in students:
        last = db.get_last_completed_session(conn, student["id"])
        session_counts[last] = session_counts.get(last, 0) + 1

    print("\n  Session Distribution:")
    for i in range(0, TOTAL_SESSIONS + 1):
        count = session_counts.get(i, 0)
        bar = "#" * count
        label = f"S{i}" if i > 0 else "S0 (not started)"
        print(f"    {label:<20} [{bar:<20}] {count}")

    print(f"\n  Last refresh: {time.strftime('%H:%M:%S')}")
    print("  Press Ctrl+C to exit")


def _get_grade_label(score: float) -> str:
    for low, high, label in GRADE_BANDS:
        if low <= score <= high:
            return label
    return "-"


def show_student_detail(conn, student_id: str) -> None:
    """Show detailed view for a specific student."""
    student = db.get_student(conn, student_id)
    if not student:
        print(f"  Student '{student_id}' not found")
        return

    print(f"\n  Student Detail: {student['name']} ({student_id})")
    print(f"  {'=' * 50}")
    print(f"  Email: {student['email']}")
    print(f"  Cohort: {student['cohort_id']}")
    print(f"  Setup: {'Complete' if student['setup_completed'] else 'Pending'}")

    # Progress
    progress = db.get_session_progress(conn, student_id)
    print(f"\n  Session Progress:")
    for p in progress:
        sn = p["session_number"]
        name = SESSION_NAMES.get(sn, f"Session {sn}")
        status = "PASSED" if p["gate_passed"] else "In Progress"
        print(f"    S{sn} {name}: {status}")
        if p["gate_details"]:
            try:
                details = json.loads(p["gate_details"])
                pts = details.get("total_points", 0)
                max_pts = details.get("max_points", 0)
                print(f"        Gate: {pts}/{max_pts} points")
            except json.JSONDecodeError:
                pass

    # Recent prompts
    print(f"\n  Recent Prompts:")
    logs = db.get_prompt_logs(conn, student_id)
    for log_entry in logs[-10:]:
        print(f"    [{log_entry['timestamp'][:19]}] "
              f"S{log_entry['session_number']} "
              f"({log_entry['event_type']}): "
              f"{log_entry['content'][:70]}")
