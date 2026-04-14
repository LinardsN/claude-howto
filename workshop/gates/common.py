"""Shared validation utilities for gate checks."""

import json
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class CheckResult:
    """Result of a single gate check."""
    passed: bool
    message: str
    points: int
    critical: bool = True  # Must pass to proceed

    def to_dict(self) -> dict:
        return {
            "passed": self.passed,
            "message": self.message,
            "points": self.points,
            "critical": self.critical,
        }


def file_exists(project_dir: Path, relative_path: str,
                message: str | None = None, points: int = 10) -> CheckResult:
    """Check that a file exists in the project directory."""
    path = project_dir / relative_path
    exists = path.exists() and path.is_file()
    msg = message or f"File exists: {relative_path}"
    return CheckResult(passed=exists, message=msg, points=points)


def dir_exists(project_dir: Path, relative_path: str,
               message: str | None = None, points: int = 10) -> CheckResult:
    """Check that a directory exists in the project directory."""
    path = project_dir / relative_path
    exists = path.exists() and path.is_dir()
    msg = message or f"Directory exists: {relative_path}"
    return CheckResult(passed=exists, message=msg, points=points)


def file_contains(project_dir: Path, relative_path: str, pattern: str,
                  message: str | None = None, points: int = 10) -> CheckResult:
    """Check that a file contains a regex pattern."""
    path = project_dir / relative_path
    if not path.exists():
        return CheckResult(
            passed=False,
            message=f"File not found: {relative_path}",
            points=points,
        )
    content = path.read_text(errors="replace")
    matches = bool(re.search(pattern, content, re.IGNORECASE))
    msg = message or f"File {relative_path} contains pattern: {pattern}"
    return CheckResult(passed=matches, message=msg, points=points)


def file_not_empty(project_dir: Path, relative_path: str,
                   message: str | None = None, points: int = 5) -> CheckResult:
    """Check that a file exists and is not empty."""
    path = project_dir / relative_path
    if not path.exists():
        return CheckResult(
            passed=False, message=f"File not found: {relative_path}",
            points=points,
        )
    is_nonempty = path.stat().st_size > 0
    msg = message or f"File is not empty: {relative_path}"
    return CheckResult(passed=is_nonempty, message=msg, points=points)


def min_file_count(project_dir: Path, relative_dir: str, pattern: str,
                   minimum: int, message: str | None = None,
                   points: int = 10) -> CheckResult:
    """Check that a directory contains at least N files matching a pattern."""
    dir_path = project_dir / relative_dir
    if not dir_path.exists():
        return CheckResult(
            passed=False, message=f"Directory not found: {relative_dir}",
            points=points,
        )
    matches = list(dir_path.rglob(pattern))
    count = len(matches)
    msg = message or f"At least {minimum} {pattern} files in {relative_dir} (found {count})"
    return CheckResult(passed=count >= minimum, message=msg, points=points)


def json_valid(project_dir: Path, relative_path: str,
               message: str | None = None, points: int = 10) -> CheckResult:
    """Check that a file contains valid JSON."""
    path = project_dir / relative_path
    if not path.exists():
        return CheckResult(
            passed=False, message=f"File not found: {relative_path}",
            points=points,
        )
    try:
        json.loads(path.read_text())
        msg = message or f"Valid JSON: {relative_path}"
        return CheckResult(passed=True, message=msg, points=points)
    except json.JSONDecodeError as e:
        msg = message or f"Invalid JSON in {relative_path}: {e}"
        return CheckResult(passed=False, message=msg, points=points)


def yaml_frontmatter_exists(project_dir: Path, relative_path: str,
                            required_fields: list[str] | None = None,
                            message: str | None = None,
                            points: int = 10) -> CheckResult:
    """Check that a markdown file has YAML frontmatter with required fields."""
    path = project_dir / relative_path
    if not path.exists():
        return CheckResult(
            passed=False, message=f"File not found: {relative_path}",
            points=points,
        )
    content = path.read_text(errors="replace")
    if not content.startswith("---"):
        msg = message or f"No YAML frontmatter in {relative_path}"
        return CheckResult(passed=False, message=msg, points=points)

    # Extract frontmatter
    parts = content.split("---", 2)
    if len(parts) < 3:
        msg = message or f"Incomplete frontmatter in {relative_path}"
        return CheckResult(passed=False, message=msg, points=points)

    frontmatter = parts[1]
    if required_fields:
        for field in required_fields:
            if field + ":" not in frontmatter:
                msg = message or f"Missing field '{field}' in frontmatter of {relative_path}"
                return CheckResult(passed=False, message=msg, points=points)

    msg = message or f"Valid frontmatter in {relative_path}"
    return CheckResult(passed=True, message=msg, points=points)


def package_json_has_dep(project_dir: Path, dep_name: str,
                         message: str | None = None,
                         points: int = 5) -> CheckResult:
    """Check that package.json includes a specific dependency."""
    pkg_path = project_dir / "package.json"
    if not pkg_path.exists():
        return CheckResult(
            passed=False, message="package.json not found",
            points=points,
        )
    try:
        pkg = json.loads(pkg_path.read_text())
        deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
        found = dep_name in deps
        msg = message or f"Dependency '{dep_name}' in package.json"
        return CheckResult(passed=found, message=msg, points=points)
    except json.JSONDecodeError:
        return CheckResult(
            passed=False, message="Invalid package.json",
            points=points,
        )


def bonus(check: CheckResult) -> CheckResult:
    """Mark a check as non-critical (bonus points)."""
    check.critical = False
    return check
