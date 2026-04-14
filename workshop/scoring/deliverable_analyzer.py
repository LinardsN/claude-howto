"""Analyze deliverable quality based on gate check results."""

import json
import sqlite3


def analyze_deliverables(conn: sqlite3.Connection, student_id: str,
                         session_number: int) -> dict:
    """Score deliverable quality from gate check results.

    Returns dict with:
        score (0-100), details (dict of check results)
    """
    row = conn.execute(
        """SELECT gate_passed, gate_details FROM session_progress
           WHERE student_id = ? AND session_number = ?""",
        (student_id, session_number),
    ).fetchone()

    if not row:
        return {"score": 0, "details": {"error": "Session not attempted"}}

    gate_passed = bool(row["gate_passed"])
    try:
        details = json.loads(row["gate_details"]) if row["gate_details"] else {}
    except json.JSONDecodeError:
        details = {}

    total_points = details.get("total_points", 0)
    max_points = details.get("max_points", 1)  # Avoid division by zero

    # Calculate percentage score
    score = (total_points / max_points * 100) if max_points > 0 else 0

    # Bonus for completing all checks (not just critical ones)
    checks = details.get("checks", [])
    if checks:
        all_passed = all(c.get("passed", False) for c in checks)
        if all_passed:
            score = min(100, score * 1.1)  # 10% bonus for perfect

    return {
        "score": round(min(100, score), 1),
        "details": {
            "gate_passed": gate_passed,
            "total_points": total_points,
            "max_points": max_points,
            "checks_passed": sum(1 for c in checks if c.get("passed")),
            "checks_total": len(checks),
        },
    }
