"""Tests for phase gate validators."""

from workshop.gates.gate_s01_slash_commands import check as check_s01
from workshop.gates.gate_s02_memory import check as check_s02
from workshop.gates.gate_s03_skills import check as check_s03


def test_s01_gate_passes_valid_project(sample_project):
    results = check_s01(sample_project)
    passed = [r for r in results if r.passed]
    assert len(passed) >= 3  # At least package.json, express, react


def test_s01_gate_fails_empty_dir(tmp_path):
    empty = tmp_path / "empty"
    empty.mkdir()
    results = check_s01(empty)
    critical_fails = [r for r in results if not r.passed and r.critical]
    assert len(critical_fails) > 0


def test_s02_gate_passes_with_claude_md(sample_project):
    results = check_s02(sample_project)
    # CLAUDE.md exists and has QA content
    claude_checks = [r for r in results if "CLAUDE.md" in r.message]
    assert any(r.passed for r in claude_checks)


def test_s03_gate_passes_with_skills(sample_project):
    results = check_s03(sample_project)
    skill_checks = [r for r in results if "SKILL.md" in r.message]
    assert any(r.passed for r in skill_checks)


def test_s03_gate_checks_frontmatter(sample_project):
    results = check_s03(sample_project)
    frontmatter_checks = [r for r in results if "frontmatter" in r.message]
    assert any(r.passed for r in frontmatter_checks)


def test_gate_empty_project(tmp_path):
    """All gates should handle empty projects gracefully."""
    empty = tmp_path / "empty-project"
    empty.mkdir()
    (empty / "package.json").write_text("{}")

    results_s01 = check_s01(empty)
    results_s02 = check_s02(empty)
    results_s03 = check_s03(empty)

    # Should not raise exceptions
    assert isinstance(results_s01, list)
    assert isinstance(results_s02, list)
    assert isinstance(results_s03, list)
