"""Session 7 gate: Plugins — qa-toolkit plugin, reports page.
Progressive dependencies: must bundle skills (S3), agents (S4), hooks (S6)."""

from pathlib import Path

from .common import (
    CheckResult, bonus, dir_exists, file_contains, file_exists,
    json_valid, min_file_count,
)


def check(project_dir: Path) -> list[CheckResult]:
    return [
        # Plugin manifest exists
        file_exists(project_dir, ".claude-plugin/plugin.json",
                    "Plugin manifest exists (.claude-plugin/plugin.json)", 15),
        json_valid(project_dir, ".claude-plugin/plugin.json",
                   "Plugin manifest is valid JSON", 10),

        # Plugin bundles skills from S3
        _check_plugin_has_skills(project_dir),

        # Plugin bundles agents from S4
        _check_plugin_has_agents(project_dir),

        # Plugin bundles hooks from S6
        _check_plugin_has_hooks(project_dir),

        # Reports page exists
        min_file_count(project_dir, ".", "*.jsx", 7,
                       "At least 7 React components (reports page added)", 10),

        # Bonus: plugin README
        bonus(file_exists(project_dir, ".claude-plugin/README.md",
                          "Bonus: Plugin has README documentation", 10)),
    ]


def _check_plugin_has_skills(project_dir: Path) -> CheckResult:
    """Verify plugin bundles skills from Session 3."""
    plugin_dir = project_dir / ".claude-plugin"
    if not plugin_dir.exists():
        return CheckResult(
            False, "Plugin bundles skills from S3", 15
        )

    # Check plugin.json references skills
    manifest = plugin_dir / "plugin.json"
    if manifest.exists():
        content = manifest.read_text(errors="replace").lower()
        if "skill" in content or "command" in content:
            return CheckResult(True, "Plugin bundles skills from S3", 15)

    # Check for skills directory in plugin
    if (plugin_dir / "commands").exists() or (plugin_dir / "skills").exists():
        return CheckResult(True, "Plugin bundles skills from S3", 15)

    return CheckResult(False, "Plugin must bundle skills from S3", 15)


def _check_plugin_has_agents(project_dir: Path) -> CheckResult:
    """Verify plugin bundles agents from Session 4."""
    plugin_dir = project_dir / ".claude-plugin"
    if not plugin_dir.exists():
        return CheckResult(False, "Plugin bundles agents from S4", 10)

    if (plugin_dir / "agents").exists():
        return CheckResult(True, "Plugin bundles agents from S4", 10)

    manifest = plugin_dir / "plugin.json"
    if manifest.exists():
        content = manifest.read_text(errors="replace").lower()
        if "agent" in content:
            return CheckResult(True, "Plugin bundles agents from S4", 10)

    return CheckResult(False, "Plugin must bundle agents from S4", 10)


def _check_plugin_has_hooks(project_dir: Path) -> CheckResult:
    """Verify plugin bundles hooks from Session 6."""
    plugin_dir = project_dir / ".claude-plugin"
    if not plugin_dir.exists():
        return CheckResult(False, "Plugin bundles hooks from S6", 10)

    if (plugin_dir / "hooks").exists():
        return CheckResult(True, "Plugin bundles hooks from S6", 10)

    manifest = plugin_dir / "plugin.json"
    if manifest.exists():
        content = manifest.read_text(errors="replace").lower()
        if "hook" in content:
            return CheckResult(True, "Plugin bundles hooks from S6", 10)

    return CheckResult(False, "Plugin must bundle hooks from S6", 10)
