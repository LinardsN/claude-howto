"""Session 9 gate: Advanced Features — CSV import/export, settings page."""

from pathlib import Path

from .common import CheckResult, bonus, min_file_count


def check(project_dir: Path) -> list[CheckResult]:
    return [
        # CSV import/export functionality
        _check_csv_functionality(project_dir),

        # Settings page
        _check_settings_page(project_dir),

        # React components increased
        min_file_count(project_dir, ".", "*.jsx", 8,
                       "At least 8 React components (settings page added)", 15),

        # Bonus: planning mode evidence (plan output or structured approach)
        bonus(_check_planning_evidence(project_dir)),
    ]


def _check_csv_functionality(project_dir: Path) -> CheckResult:
    """Check for CSV import/export in the codebase."""
    csv_keywords = ["csv", "import", "export", "download", "upload",
                    "papaparse", "csv-parse", "fast-csv"]

    # Check package.json for CSV libraries
    pkg_path = project_dir / "package.json"
    if pkg_path.exists():
        content = pkg_path.read_text(errors="replace").lower()
        for kw in ["papaparse", "csv-parse", "fast-csv", "csv-writer"]:
            if kw in content:
                return CheckResult(True, "CSV library installed", 25)

    # Check source files for CSV handling
    for ext in ["*.js", "*.jsx", "*.ts", "*.tsx"]:
        for src_file in project_dir.rglob(ext):
            if "node_modules" in str(src_file):
                continue
            content = src_file.read_text(errors="replace").lower()
            if "csv" in content and ("import" in content or "export" in content):
                return CheckResult(
                    True, "CSV import/export functionality found", 25
                )

    return CheckResult(False, "CSV import/export not found", 25)


def _check_settings_page(project_dir: Path) -> CheckResult:
    """Check for a settings page component."""
    for jsx_file in project_dir.rglob("*.jsx"):
        if "node_modules" in str(jsx_file):
            continue
        name = jsx_file.stem.lower()
        if "setting" in name or "config" in name or "preference" in name:
            return CheckResult(True, "Settings page component exists", 20)

        content = jsx_file.read_text(errors="replace").lower()
        if "settings" in content and "save" in content:
            return CheckResult(True, "Settings page functionality found", 20)

    return CheckResult(False, "Settings page not found", 20)


def _check_planning_evidence(project_dir: Path) -> CheckResult:
    """Check for evidence of planning mode usage."""
    # Look for plan files or structured approach
    plan_patterns = ["*plan*", "*architecture*", "*design*"]
    for pattern in plan_patterns:
        matches = [m for m in project_dir.rglob(pattern)
                   if "node_modules" not in str(m) and ".git/" not in str(m)]
        if matches:
            return CheckResult(
                True, "Bonus: Planning mode evidence found", 10
            )
    return CheckResult(False, "Bonus: Planning mode evidence", 10)
