"""Bootcamp platform configuration constants."""

from pathlib import Path

# Session configuration
TOTAL_SESSIONS = 10
SESSION_NAMES = {
    1: "Slash Commands",
    2: "Memory",
    3: "Skills",
    4: "Subagents",
    5: "MCP",
    6: "Hooks",
    7: "Plugins",
    8: "Checkpoints",
    9: "Advanced Features",
    10: "CLI and CI/CD",
}

# Paths
WORKSHOP_DIR = Path(__file__).parent.parent
SESSIONS_DIR = WORKSHOP_DIR / "sessions"
GATES_DIR = WORKSHOP_DIR / "gates"
HOOKS_DIR = WORKSHOP_DIR / "hooks"
TEMPLATES_DIR = WORKSHOP_DIR / "templates"

BOOTCAMP_HOME = Path.home() / ".claude-bootcamp"
LOGS_DIR = BOOTCAMP_HOME / "logs"
DB_PATH = BOOTCAMP_HOME / "bootcamp.db"
STUDENT_ID_FILE = BOOTCAMP_HOME / "student-id"
CURRENT_SESSION_FILE = BOOTCAMP_HOME / "current-session"

# Scoring weights (must sum to 1.0)
SCORING_WEIGHTS = {
    "prompt_quality": 0.25,
    "efficiency": 0.15,
    "deliverable_quality": 0.20,
    "standards_compliance": 0.15,
    "final_task": 0.25,
}

# Grade bands
GRADE_BANDS = [
    (90, 100, "Excellent"),
    (80, 89, "Very Good"),
    (70, 79, "Good"),
    (60, 69, "Satisfactory"),
    (50, 59, "Needs Improvement"),
    (0, 49, "Incomplete"),
]

# Hook settings template path
HOOKS_SETTINGS_TEMPLATE = HOOKS_DIR / "hooks-settings.json"
