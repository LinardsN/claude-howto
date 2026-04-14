"""Cohort registration management: open/close, deadlines, student roster."""

import sqlite3

from . import database as db


def open_registration(conn: sqlite3.Connection, cohort_id: str,
                      name: str | None = None,
                      deadline: str | None = None) -> str:
    """Open registration for a cohort. Creates the cohort if it doesn't exist."""
    existing = db.get_cohort(conn, cohort_id)
    if existing:
        db.set_registration_open(conn, cohort_id, True)
        if deadline:
            conn.execute(
                "UPDATE cohorts SET deadline = ? WHERE id = ?",
                (deadline, cohort_id),
            )
            conn.commit()
        return f"Registration reopened for cohort '{cohort_id}'"

    cohort_name = name or cohort_id
    db.create_cohort(conn, cohort_id, cohort_name, deadline)
    msg = f"Cohort '{cohort_id}' created with registration open"
    if deadline:
        msg += f" (deadline: {deadline})"
    return msg


def close_registration(conn: sqlite3.Connection, cohort_id: str) -> str:
    """Close registration for a cohort."""
    existing = db.get_cohort(conn, cohort_id)
    if not existing:
        raise ValueError(f"Cohort '{cohort_id}' does not exist")
    db.set_registration_open(conn, cohort_id, False)
    return f"Registration closed for cohort '{cohort_id}'"


def register_student(conn: sqlite3.Connection, student_id: str, name: str,
                     email: str, cohort_id: str) -> str:
    """Register a student in a cohort."""
    db.register_student(conn, student_id, name, email, cohort_id)
    return f"Student '{name}' ({student_id}) registered in cohort '{cohort_id}'"


def get_roster(conn: sqlite3.Connection,
               cohort_id: str | None = None) -> list[dict]:
    """Get the student roster, optionally filtered by cohort."""
    students = db.list_students(conn, cohort_id)
    roster = []
    for s in students:
        last_session = db.get_last_completed_session(conn, s["id"])
        total_score = db.get_total_score(conn, s["id"])
        roster.append({
            "id": s["id"],
            "name": s["name"],
            "email": s["email"],
            "cohort_id": s["cohort_id"],
            "setup_completed": bool(s["setup_completed"]),
            "last_completed_session": last_session,
            "average_score": round(total_score, 1),
        })
    return roster
