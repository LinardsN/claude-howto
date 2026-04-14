"""Generate scoring reports in HTML, CSV, and JSON formats."""

import csv
import io
import json
import sqlite3
from datetime import datetime, timezone

from ..platform import database as db
from .rubric import get_grade


def generate_student_report(conn: sqlite3.Connection,
                            student_id: str) -> dict:
    """Generate a detailed report for a single student."""
    student = db.get_student(conn, student_id)
    if not student:
        return {"error": f"Student {student_id} not found"}

    scores = db.get_scores(conn, student_id)
    progress = db.get_session_progress(conn, student_id)
    prompt_count = sum(
        db.get_prompt_count(conn, student_id, i) for i in range(1, 11)
    )

    total_score = db.get_total_score(conn, student_id)
    grade_label, grade_desc = get_grade(total_score)

    return {
        "student": {
            "id": student_id,
            "name": student["name"],
            "email": student["email"],
            "cohort": student["cohort_id"],
        },
        "summary": {
            "total_score": round(total_score, 1),
            "grade": grade_label,
            "grade_description": grade_desc,
            "sessions_completed": len([p for p in progress if p["gate_passed"]]),
            "total_prompts": prompt_count,
        },
        "sessions": [
            {
                "number": s["session_number"],
                "prompt_quality": s["prompt_quality"],
                "efficiency": s["efficiency"],
                "deliverable_quality": s["deliverable_quality"],
                "standards_compliance": s["standards_compliance"],
                "total": s["total"],
            }
            for s in scores
        ],
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


def generate_cohort_report(conn: sqlite3.Connection,
                           cohort_id: str | None = None) -> dict:
    """Generate a report for an entire cohort."""
    students = db.list_students(conn, cohort_id)
    reports = []

    for student in students:
        report = generate_student_report(conn, student["id"])
        reports.append(report)

    # Calculate cohort statistics
    scores = [r["summary"]["total_score"] for r in reports
              if r["summary"]["total_score"] > 0]

    return {
        "cohort": cohort_id or "all",
        "statistics": {
            "total_students": len(students),
            "scored_students": len(scores),
            "average_score": round(sum(scores) / len(scores), 1) if scores else 0,
            "highest_score": round(max(scores), 1) if scores else 0,
            "lowest_score": round(min(scores), 1) if scores else 0,
        },
        "students": reports,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


def to_json(report: dict) -> str:
    """Export report as JSON."""
    return json.dumps(report, indent=2)


def to_csv(report: dict) -> str:
    """Export cohort report as CSV."""
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow([
        "Student ID", "Name", "Email", "Score", "Grade",
        "Sessions Completed", "Total Prompts",
    ])

    for student_report in report.get("students", []):
        s = student_report.get("student", {})
        summary = student_report.get("summary", {})
        writer.writerow([
            s.get("id", ""),
            s.get("name", ""),
            s.get("email", ""),
            summary.get("total_score", 0),
            summary.get("grade", ""),
            summary.get("sessions_completed", 0),
            summary.get("total_prompts", 0),
        ])

    return buf.getvalue()


def to_html(report: dict) -> str:
    """Export cohort report as HTML."""
    stats = report.get("statistics", {})
    rows = ""
    for student_report in report.get("students", []):
        s = student_report.get("student", {})
        summary = student_report.get("summary", {})
        score = summary.get("total_score", 0)
        grade = summary.get("grade", "Ungraded")

        # Color code by grade
        if score >= 80:
            color = "#2ecc71"
        elif score >= 60:
            color = "#f39c12"
        else:
            color = "#e74c3c"

        rows += f"""<tr>
<td>{s.get('id', '')}</td>
<td>{s.get('name', '')}</td>
<td style="color:{color};font-weight:bold">{score:.1f}</td>
<td>{grade}</td>
<td>{summary.get('sessions_completed', 0)}/10</td>
<td>{summary.get('total_prompts', 0)}</td>
</tr>\n"""

    return f"""<!DOCTYPE html>
<html><head>
<title>AI Bootcamp - Cohort Report</title>
<style>
body {{ font-family: system-ui, -apple-system, sans-serif; margin: 2rem; background: #f5f5f5; }}
.container {{ max-width: 1000px; margin: 0 auto; background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
h1 {{ color: #1a1a2e; border-bottom: 2px solid #e94560; padding-bottom: 0.5rem; }}
.stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin: 1.5rem 0; }}
.stat {{ background: #f8f9fa; padding: 1rem; border-radius: 4px; text-align: center; }}
.stat-value {{ font-size: 2rem; font-weight: bold; color: #1a1a2e; }}
.stat-label {{ color: #666; font-size: 0.85rem; }}
table {{ border-collapse: collapse; width: 100%; margin-top: 1.5rem; }}
th {{ background: #1a1a2e; color: white; padding: 10px; text-align: left; }}
td {{ border-bottom: 1px solid #eee; padding: 10px; }}
tr:hover {{ background: #f8f9fa; }}
.footer {{ color: #999; font-size: 0.8rem; margin-top: 2rem; text-align: center; }}
</style>
</head><body>
<div class="container">
<h1>AI Bootcamp - Cohort Report</h1>
<div class="stats">
<div class="stat"><div class="stat-value">{stats.get('total_students', 0)}</div><div class="stat-label">Total Students</div></div>
<div class="stat"><div class="stat-value">{stats.get('average_score', 0):.1f}</div><div class="stat-label">Average Score</div></div>
<div class="stat"><div class="stat-value">{stats.get('highest_score', 0):.1f}</div><div class="stat-label">Highest Score</div></div>
<div class="stat"><div class="stat-value">{stats.get('lowest_score', 0):.1f}</div><div class="stat-label">Lowest Score</div></div>
</div>
<table>
<tr><th>Student ID</th><th>Name</th><th>Score</th><th>Grade</th><th>Sessions</th><th>Prompts</th></tr>
{rows}
</table>
<div class="footer">Generated: {report.get('generated_at', '')}</div>
</div>
</body></html>"""
