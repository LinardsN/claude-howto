"""Export bootcamp data to various formats."""

import csv
import io
import json
import sqlite3
from pathlib import Path

from ..platform import database as db
from ..platform.config import LOGS_DIR, SESSION_NAMES


def export_scores(conn: sqlite3.Connection,
                  output_format: str = "csv") -> str:
    """Export all student scores."""
    all_scores = db.get_all_scores(conn)
    data = [dict(row) for row in all_scores]

    if output_format == "json":
        return json.dumps(data, indent=2)
    elif output_format == "csv":
        if not data:
            return ""
        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        return buf.getvalue()
    else:
        return json.dumps(data, indent=2)


def export_prompt_logs(conn: sqlite3.Connection,
                       student_id: str,
                       session_number: int | None = None) -> str:
    """Export prompt logs for a student as JSON."""
    logs = db.get_prompt_logs(conn, student_id, session_number)
    return json.dumps([dict(row) for row in logs], indent=2)


def export_progress(conn: sqlite3.Connection) -> str:
    """Export all students' progress as CSV."""
    students = db.list_students(conn)
    buf = io.StringIO()
    writer = csv.writer(buf)

    # Header
    header = ["Student ID", "Name", "Email"]
    for i in range(1, 11):
        header.append(f"S{i}: {SESSION_NAMES[i]}")
    writer.writerow(header)

    # Data
    for student in students:
        row = [student["id"], student["name"], student["email"]]
        progress = db.get_session_progress(conn, student["id"])
        progress_map = {p["session_number"]: p for p in progress}
        for i in range(1, 11):
            p = progress_map.get(i)
            if p and p["gate_passed"]:
                row.append("PASSED")
            elif p and p["started_at"]:
                row.append("In Progress")
            else:
                row.append("-")
        writer.writerow(row)

    return buf.getvalue()
