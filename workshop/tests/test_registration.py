"""Tests for registration management."""

import pytest

from workshop.platform import database as db
from workshop.platform.registration import (
    close_registration,
    get_roster,
    open_registration,
    register_student,
)


def test_open_registration_new_cohort(db_conn):
    msg = open_registration(db_conn, "new-cohort", "New Cohort")
    assert "created" in msg
    cohort = db.get_cohort(db_conn, "new-cohort")
    assert cohort is not None
    assert cohort["registration_open"] == 1


def test_open_registration_with_deadline(db_conn):
    msg = open_registration(db_conn, "dl-cohort", deadline="2026-12-31")
    assert "deadline" in msg


def test_reopen_registration(db_conn, sample_cohort):
    close_registration(db_conn, sample_cohort)
    msg = open_registration(db_conn, sample_cohort)
    assert "reopened" in msg
    cohort = db.get_cohort(db_conn, sample_cohort)
    assert cohort["registration_open"] == 1


def test_close_registration(db_conn, sample_cohort):
    msg = close_registration(db_conn, sample_cohort)
    assert "closed" in msg.lower()


def test_close_nonexistent_cohort(db_conn):
    with pytest.raises(ValueError, match="does not exist"):
        close_registration(db_conn, "fake")


def test_register_student_success(db_conn, sample_cohort):
    msg = register_student(db_conn, "s1", "Alice", "a@t.com", sample_cohort)
    assert "registered" in msg


def test_get_roster(db_conn, sample_cohort, sample_student):
    roster = get_roster(db_conn, sample_cohort)
    assert len(roster) == 1
    assert roster[0]["id"] == sample_student
    assert roster[0]["last_completed_session"] == 0
