"""Session 5 gate: MCP — GitHub MCP, Jira MCP, bug-to-issue sync, test run executor."""

from pathlib import Path

from .common import (
    CheckResult, bonus, file_contains, file_exists, json_valid,
    min_file_count,
)


def check(project_dir: Path) -> list[CheckResult]:
    return [
        # .mcp.json exists and is valid
        file_exists(project_dir, ".mcp.json",
                    "MCP configuration file exists (.mcp.json)", 15),
        json_valid(project_dir, ".mcp.json",
                   "MCP configuration is valid JSON", 10),

        # GitHub MCP configured
        file_contains(project_dir, ".mcp.json", r"github",
                      "GitHub MCP server configured", 15),

        # Test run executor functionality
        min_file_count(project_dir, ".", "*.jsx", 5,
                       "At least 5 React components (test run executor added)", 10),

        # API routes for test runs
        _check_test_run_routes(project_dir),

        # Jira/Atlassian MCP configured
        file_contains(project_dir, ".mcp.json",
                      r"(atlassian|jira|confluence)",
                      "Jira/Atlassian MCP configured", 15),

        # Bonus: bug-to-issue sync functionality
        bonus(_check_github_issue_integration(project_dir)),
    ]


def _check_test_run_routes(project_dir: Path) -> CheckResult:
    """Check for test run related files or routes."""
    for pattern in ["*test*run*", "*executor*", "*runner*"]:
        matches = list(project_dir.rglob(pattern))
        # Filter out node_modules and .git
        matches = [m for m in matches
                   if "node_modules" not in str(m) and ".git/" not in str(m)]
        if matches:
            return CheckResult(True, "Test run executor files exist", 10)
    return CheckResult(False, "Test run executor not found", 10)


def _check_github_issue_integration(project_dir: Path) -> CheckResult:
    """Check for GitHub issue creation integration in bug tracker."""
    for jsx_file in project_dir.rglob("*.jsx"):
        if "node_modules" in str(jsx_file):
            continue
        content = jsx_file.read_text(errors="replace").lower()
        if "issue" in content and "github" in content:
            return CheckResult(
                True, "Bonus: GitHub issue integration in bug tracker", 10
            )
    return CheckResult(
        False, "Bonus: GitHub issue integration in bug tracker", 10
    )
