"""Tests for database operations."""

import pytest

from workshop.platform import database as db


def test_create_cohort(db_conn):
    db.create_cohort(db_conn, "c1", "Cohort 1")
    cohort = db.get_cohort(db_conn, "c1")
    assert cohort is not None
    assert cohort["name"] == "Cohort 1"
    assert cohort["registration_open"] == 1


def test_create_cohort_with_deadline(db_conn):
    db.create_cohort(db_conn, "c2", "Cohort 2", deadline="2026-12-31")
    cohort = db.get_cohort(db_conn, "c2")
    assert cohort["deadline"] == "2026-12-31"


def test_set_registration_open(db_conn, sample_cohort):
    db.set_registration_open(db_conn, sample_cohort, False)
    cohort = db.get_cohort(db_conn, sample_cohort)
    assert cohort["registration_open"] == 0


def test_register_student(db_conn, sample_cohort):
    db.register_student(db_conn, "s1", "Bob", "bob@test.com", sample_cohort)
    student = db.get_student(db_conn, "s1")
    assert student is not None
    assert student["name"] == "Bob"


def test_register_student_closed_cohort(db_conn, sample_cohort):
    db.set_registration_open(db_conn, sample_cohort, False)
    with pytest.raises(ValueError, match="closed"):
        db.register_student(db_conn, "s2", "Eve", "eve@test.com", sample_cohort)


def test_register_student_nonexistent_cohort(db_conn):
    with pytest.raises(ValueError, match="does not exist"):
        db.register_student(db_conn, "s3", "Faye", "f@test.com", "fake")


def test_session_progress(db_conn, sample_student):
    db.start_session(db_conn, sample_student, 1)
    progress = db.get_session_progress(db_conn, sample_student)
    assert len(progress) == 1
    assert progress[0]["session_number"] == 1


def test_complete_session(db_conn, sample_student):
    db.start_session(db_conn, sample_student, 1)
    db.complete_session(db_conn, sample_student, 1, True, {"checks": []})
    last = db.get_last_completed_session(db_conn, sample_student)
    assert last == 1


def test_last_completed_session_none(db_conn, sample_student):
    last = db.get_last_completed_session(db_conn, sample_student)
    assert last == 0


def test_save_and_get_scores(db_conn, sample_student):
    db.save_score(db_conn, sample_student, 1,
                  prompt_quality=80, efficiency=70,
                  deliverable_quality=90, standards_compliance=85,
                  total=81)
    scores = db.get_scores(db_conn, sample_student)
    assert len(scores) == 1
    assert scores[0]["total"] == 81


def test_get_total_score(db_conn, sample_student):
    db.save_score(db_conn, sample_student, 1, 80, 70, 90, 85, 80)
    db.save_score(db_conn, sample_student, 2, 70, 60, 80, 75, 70)
    total = db.get_total_score(db_conn, sample_student)
    assert total == 75.0


def test_log_prompt(db_conn, sample_student):
    db.log_prompt(db_conn, sample_student, 1, "prompt", "Create a test case form")
    logs = db.get_prompt_logs(db_conn, sample_student, 1)
    assert len(logs) == 1
    assert logs[0]["content"] == "Create a test case form"


def test_prompt_count(db_conn, sample_student):
    db.log_prompt(db_conn, sample_student, 1, "prompt", "first")
    db.log_prompt(db_conn, sample_student, 1, "prompt", "second")
    db.log_prompt(db_conn, sample_student, 1, "response", "not a prompt")
    count = db.get_prompt_count(db_conn, sample_student, 1)
    assert count == 2


def test_list_students(db_conn, sample_cohort):
    db.register_student(db_conn, "a1", "Alice", "a@t.com", sample_cohort)
    db.register_student(db_conn, "b1", "Bob", "b@t.com", sample_cohort)
    students = db.list_students(db_conn, sample_cohort)
    assert len(students) == 2


def test_get_all_scores(db_conn, sample_student):
    db.save_score(db_conn, sample_student, 1, 80, 70, 90, 85, 80)
    all_scores = db.get_all_scores(db_conn)
    assert len(all_scores) == 1
    assert all_scores[0]["avg_score"] == 80.0
