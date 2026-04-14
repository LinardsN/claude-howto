"""Session 6 gate: Hooks — validation hooks, prompt logging, dashboard page."""

from pathlib import Path

from .common import (
    CheckResult, bonus, dir_exists, file_contains, file_exists,
    json_valid, min_file_count,
)


def check(project_dir: Path) -> list[CheckResult]:
    results = [
        # Hooks directory with hook scripts
        dir_exists(project_dir, ".claude/hooks",
                   "Hooks directory exists (.claude/hooks/)", 10),
        min_file_count(project_dir, ".claude/hooks", "*", 1,
                       "At least 1 hook script in .claude/hooks/", 10),

        # Settings.json with hook configuration
        file_exists(project_dir, ".claude/settings.json",
                    "Claude settings.json exists with hook config", 10),
        json_valid(project_dir, ".claude/settings.json",
                   "settings.json is valid JSON", 5),
        file_contains(project_dir, ".claude/settings.json",
                      r"(PreToolUse|PostToolUse|Stop|UserPromptSubmit)",
                      "settings.json configures at least one hook event", 15),

        # Dashboard page exists
        min_file_count(project_dir, ".", "*.jsx", 6,
                       "At least 6 React components (dashboard added)", 10),
    ]

    # Progressive dependency: hooks reference or enforce S2 CLAUDE.md rules
    results.append(_check_hooks_enforce_standards(project_dir))

    # Progressive dependency: hooks reference skills from S3
    results.append(_check_hooks_reference_skills(project_dir))

    # Bonus: multiple hook types (PreToolUse + PostToolUse + Stop)
    results.append(bonus(_check_multiple_hook_types(project_dir)))

    return results


def _check_hooks_enforce_standards(project_dir: Path) -> CheckResult:
    """Verify hooks reference or enforce project standards from S2."""
    hooks_dir = project_dir / ".claude/hooks"
    if not hooks_dir.exists():
        return CheckResult(
            False, "Hooks enforce CLAUDE.md standards (S2 dependency)", 10,
            critical=False,
        )

    for hook_file in hooks_dir.iterdir():
        if hook_file.is_file():
            content = hook_file.read_text(errors="replace").lower()
            if any(kw in content for kw in
                   ["claude.md", "standard", "convention", "naming", "lint"]):
                return CheckResult(
                    True, "Hooks enforce project standards (S2 dependency)", 10
                )

    return CheckResult(
        False, "Hooks should enforce CLAUDE.md standards (S2 dependency)", 10,
        critical=False,
    )


def _check_hooks_reference_skills(project_dir: Path) -> CheckResult:
    """Verify hooks validate or reference skills from S3."""
    settings_path = project_dir / ".claude/settings.json"
    if settings_path.exists():
        content = settings_path.read_text(errors="replace").lower()
        if "skill" in content:
            return CheckResult(
                True, "Hooks reference skills (S3 dependency)", 5
            )
    return CheckResult(
        False, "Hooks should reference skills (S3 dependency)", 5,
        critical=False,
    )


def _check_multiple_hook_types(project_dir: Path) -> CheckResult:
    """Check for multiple hook event types configured."""
    settings_path = project_dir / ".claude/settings.json"
    if not settings_path.exists():
        return CheckResult(False, "Bonus: Multiple hook types configured", 10)

    content = settings_path.read_text(errors="replace")
    hook_types = ["PreToolUse", "PostToolUse", "Stop", "UserPromptSubmit"]
    found = sum(1 for ht in hook_types if ht in content)
    return CheckResult(
        found >= 2,
        f"Bonus: {found} hook types configured (need 2+)",
        10,
    )
