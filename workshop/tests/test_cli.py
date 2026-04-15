"""Tests for CLI subcommands."""

from workshop.platform.cli import main


def test_help_returns_1():
    """No subcommand should print help and return 1."""
    result = main([])
    assert result == 1


def test_open_registration(db_conn, monkeypatch):
    """Open registration via CLI."""
    monkeypatch.setattr(
        "workshop.platform.cli.db.get_connection", lambda: db_conn
    )
    result = main(["open-registration", "--cohort", "cli-test"])
    assert result == 0


def test_register_student(db_conn, sample_cohort, monkeypatch):
    """Register student via CLI."""
    monkeypatch.setattr(
        "workshop.platform.cli.db.get_connection", lambda: db_conn
    )
    result = main([
        "register", "cli-student", "CLI Student", "cli@test.com",
        "--cohort", sample_cohort,
    ])
    assert result == 0


def test_start_session_without_setup(db_conn, monkeypatch, tmp_path):
    """Starting session without setup should fail."""
    monkeypatch.setattr(
        "workshop.platform.cli.db.get_connection", lambda: db_conn
    )
    monkeypatch.setattr(
        "workshop.platform.cli.setup.get_student_id", lambda: None
    )
    result = main(["start-session", "1"])
    assert result == 1


def test_status_without_student(db_conn, monkeypatch):
    """Status without student ID should fail."""
    monkeypatch.setattr(
        "workshop.platform.cli.db.get_connection", lambda: db_conn
    )
    monkeypatch.setattr(
        "workshop.platform.cli.setup.get_student_id", lambda: None
    )
    result = main(["status"])
    assert result == 1


def test_invalid_session_number(db_conn, monkeypatch):
    """Session number out of range should fail."""
    monkeypatch.setattr(
        "workshop.platform.cli.db.get_connection", lambda: db_conn
    )
    monkeypatch.setattr(
        "workshop.platform.cli.setup.get_student_id", lambda: "s1"
    )
    result = main(["start-session", "99"])
    assert result == 1
