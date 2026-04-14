"""Tests for the prompt quality analyzer."""

import json
import tempfile
from pathlib import Path

from workshop.scoring.prompt_analyzer import analyze_prompts


def _create_log(tmp_path: Path, session: int, prompts: list[str]) -> Path:
    """Create a JSONL log file with test prompts."""
    log_dir = tmp_path / f"session-{session}"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "prompts.jsonl"

    lines = []
    for prompt in prompts:
        lines.append(json.dumps({
            "type": "prompt",
            "content": prompt,
            "timestamp": "2026-04-14T10:00:00Z",
        }))
    log_file.write_text("\n".join(lines))
    return tmp_path


def test_no_prompts():
    with tempfile.TemporaryDirectory() as tmp:
        result = analyze_prompts(Path(tmp), 1)
    assert result["score"] == 0


def test_high_quality_prompts(tmp_path):
    prompts = [
        "Create a test case form with fields for title, description, preconditions, "
        "steps to reproduce, expected result, and ISTQB severity levels S1-S4",
        "Build an API endpoint for test cases using REST conventions because our "
        "CLAUDE.md requires consistent JSON responses with success and error fields",
        "Add boundary value analysis for the password field: minimum 8 characters, "
        "maximum 128 characters, with validation error messages",
    ]
    log_dir = _create_log(tmp_path, 1, prompts)
    result = analyze_prompts(log_dir, 1)
    assert result["score"] > 50  # High quality prompts should score well


def test_low_quality_prompts(tmp_path):
    prompts = [
        "fix it",
        "make it work",
        "help me",
        "do the thing",
    ]
    log_dir = _create_log(tmp_path, 1, prompts)
    result = analyze_prompts(log_dir, 1)
    assert result["score"] < 40  # Vague prompts should score low


def test_mixed_quality_prompts(tmp_path):
    prompts = [
        "Create a bug tracker with severity filtering using ISTQB levels",
        "fix it",
        "Add a dashboard page showing total test cases by status and open bugs by severity",
    ]
    log_dir = _create_log(tmp_path, 1, prompts)
    result = analyze_prompts(log_dir, 1)
    assert 20 < result["score"] < 80  # Mixed quality


def test_details_included(tmp_path):
    prompts = ["Build a test case CRUD API with REST conventions"]
    log_dir = _create_log(tmp_path, 1, prompts)
    result = analyze_prompts(log_dir, 1)
    assert "details" in result
    assert "total_prompts" in result["details"]
    assert result["details"]["total_prompts"] == 1
