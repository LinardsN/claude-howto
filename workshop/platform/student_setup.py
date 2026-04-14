"""Student onboarding: create directories, install hooks, link to cohort."""

import json
import shutil
import sqlite3
from pathlib import Path

from . import database as db
from .config import (
    BOOTCAMP_HOME,
    CURRENT_SESSION_FILE,
    HOOKS_DIR,
    HOOKS_SETTINGS_TEMPLATE,
    LOGS_DIR,
    STUDENT_ID_FILE,
)


def setup_student(conn: sqlite3.Connection, student_id: str,
                  project_dir: Path | None = None) -> list[str]:
    """Run the full student setup process. Returns a list of steps completed."""
    steps = []

    # Verify student exists in database
    student = db.get_student(conn, student_id)
    if not student:
        raise ValueError(
            f"Student '{student_id}' is not registered. "
            "Ask your instructor to register you first."
        )

    # Create bootcamp home directory
    BOOTCAMP_HOME.mkdir(parents=True, exist_ok=True)
    steps.append(f"Created bootcamp directory: {BOOTCAMP_HOME}")

    # Write student ID file
    STUDENT_ID_FILE.write_text(student_id)
    steps.append(f"Saved student ID: {student_id}")

    # Initialize current session
    CURRENT_SESSION_FILE.write_text("0")
    steps.append("Initialized session tracker")

    # Create logs directory
    student_logs = LOGS_DIR / student_id
    student_logs.mkdir(parents=True, exist_ok=True)
    for i in range(1, 11):
        (student_logs / f"session-{i}").mkdir(exist_ok=True)
    steps.append(f"Created log directories: {student_logs}")

    # Install hooks into project
    if project_dir:
        hooks_installed = _install_hooks(project_dir)
        steps.extend(hooks_installed)

    # Mark setup as completed
    db.mark_setup_completed(conn, student_id)
    steps.append("Setup marked as completed in database")

    return steps


def _install_hooks(project_dir: Path) -> list[str]:
    """Install prompt logging hooks into the student's project."""
    steps = []
    claude_dir = project_dir / ".claude"
    claude_dir.mkdir(exist_ok=True)

    # Copy hook scripts
    hooks_dest = claude_dir / "hooks"
    hooks_dest.mkdir(exist_ok=True)

    for hook_file in ["log-prompt.sh", "log-response.sh"]:
        src = HOOKS_DIR / hook_file
        dst = hooks_dest / hook_file
        if src.exists():
            shutil.copy2(src, dst)
            dst.chmod(0o755)
            steps.append(f"Installed hook: {dst}")

    # Install or merge settings.json
    settings_path = claude_dir / "settings.json"
    if HOOKS_SETTINGS_TEMPLATE.exists():
        template = json.loads(HOOKS_SETTINGS_TEMPLATE.read_text())

        # Update hook paths to point to actual location
        _update_hook_paths(template, hooks_dest)

        if settings_path.exists():
            existing = json.loads(settings_path.read_text())
            existing.setdefault("hooks", {})
            for event, hooks in template.get("hooks", {}).items():
                existing["hooks"].setdefault(event, []).extend(hooks)
            settings_path.write_text(json.dumps(existing, indent=2))
            steps.append("Merged hooks into existing settings.json")
        else:
            settings_path.write_text(json.dumps(template, indent=2))
            steps.append("Created settings.json with logging hooks")

    return steps


def _update_hook_paths(template: dict, hooks_dir: Path) -> None:
    """Replace placeholder paths in template with actual hook locations."""
    for _event, hook_list in template.get("hooks", {}).items():
        for hook_group in hook_list:
            for hook in hook_group.get("hooks", []):
                if "command" in hook:
                    # Replace $HOOKS_DIR placeholder
                    hook["command"] = hook["command"].replace(
                        "$HOOKS_DIR", str(hooks_dir)
                    )


def get_student_id() -> str | None:
    """Read the current student ID from the bootcamp home directory."""
    if STUDENT_ID_FILE.exists():
        return STUDENT_ID_FILE.read_text().strip()
    return None


def get_current_session() -> int:
    """Read the current session number."""
    if CURRENT_SESSION_FILE.exists():
        try:
            return int(CURRENT_SESSION_FILE.read_text().strip())
        except ValueError:
            return 0
    return 0


def set_current_session(session_number: int) -> None:
    """Update the current session tracker."""
    CURRENT_SESSION_FILE.write_text(str(session_number))
