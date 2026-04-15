"""Session 10 gate: CLI & CI/CD — pipeline, batch scripts, final polish."""

from pathlib import Path

from .common import (
    CheckResult, bonus, dir_exists, file_contains, file_exists,
    min_file_count,
)


def check(project_dir: Path) -> list[CheckResult]:
    return [
        # CI/CD configuration exists
        _check_ci_config(project_dir),

        # Navigation/routing in React app
        _check_navigation(project_dir),

        # Responsive design
        _check_responsive(project_dir),

        # Final app has sufficient components
        min_file_count(project_dir, ".", "*.jsx", 8,
                       "Complete app with 8+ React components", 10),

        # App is runnable (package.json has start/dev scripts)
        file_contains(project_dir, "package.json", r'"(dev|start)"',
                      "App has start/dev script in package.json", 10),

        # MCP used in CI (progressive dependency from S5)
        bonus(_check_ci_uses_mcp(project_dir)),

        # Bonus: batch processing script
        bonus(_check_batch_script(project_dir)),
    ]


def _check_ci_config(project_dir: Path) -> CheckResult:
    """Check for CI/CD configuration (GitHub Actions, etc.)."""
    ci_paths = [
        ".github/workflows",
        ".github/actions",
        ".gitlab-ci.yml",
        "Jenkinsfile",
        ".circleci",
    ]
    for ci_path in ci_paths:
        path = project_dir / ci_path
        if path.exists():
            return CheckResult(True, f"CI/CD config found: {ci_path}", 20)

    return CheckResult(False, "CI/CD configuration not found", 20)


def _check_navigation(project_dir: Path) -> CheckResult:
    """Check for app navigation (router, sidebar, navbar)."""
    nav_keywords = ["router", "route", "navigate", "sidebar", "navbar",
                    "nav", "menu", "link to="]
    for jsx_file in project_dir.rglob("*.jsx"):
        if "node_modules" in str(jsx_file):
            continue
        content = jsx_file.read_text(errors="replace").lower()
        if any(kw in content for kw in nav_keywords):
            return CheckResult(True, "App has navigation/routing", 15)

    return CheckResult(False, "App navigation not found", 15)


def _check_responsive(project_dir: Path) -> CheckResult:
    """Check for responsive design patterns."""
    responsive_keywords = ["media", "responsive", "mobile", "flex",
                           "grid", "@media", "breakpoint"]
    for css_file in project_dir.rglob("*.css"):
        if "node_modules" in str(css_file):
            continue
        content = css_file.read_text(errors="replace").lower()
        if any(kw in content for kw in responsive_keywords):
            return CheckResult(True, "Responsive design CSS found", 10)

    # Check JSX for responsive patterns
    for jsx_file in project_dir.rglob("*.jsx"):
        if "node_modules" in str(jsx_file):
            continue
        content = jsx_file.read_text(errors="replace").lower()
        if "useMediaQuery" in content or "responsive" in content:
            return CheckResult(True, "Responsive design patterns found", 10)

    return CheckResult(False, "Responsive design not found", 10)


def _check_ci_uses_mcp(project_dir: Path) -> CheckResult:
    """Check if CI config references MCP or Claude Code (S5 dependency)."""
    workflows_dir = project_dir / ".github/workflows"
    if not workflows_dir.exists():
        return CheckResult(
            False, "Bonus: CI uses MCP/Claude Code (S5 dependency)", 10
        )

    for yml_file in workflows_dir.glob("*.yml"):
        content = yml_file.read_text(errors="replace").lower()
        if "claude" in content or "mcp" in content:
            return CheckResult(
                True, "Bonus: CI references Claude Code/MCP", 10
            )

    return CheckResult(
        False, "Bonus: CI uses MCP/Claude Code (S5 dependency)", 10
    )


def _check_batch_script(project_dir: Path) -> CheckResult:
    """Check for batch processing scripts using claude -p."""
    for sh_file in project_dir.rglob("*.sh"):
        if "node_modules" in str(sh_file):
            continue
        content = sh_file.read_text(errors="replace")
        if "claude -p" in content or "claude --print" in content:
            return CheckResult(True, "Bonus: Batch script using claude -p", 10)

    return CheckResult(False, "Bonus: Batch processing script", 10)
