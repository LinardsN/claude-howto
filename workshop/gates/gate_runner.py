"""Gate runner: orchestrates validation for a given session number."""

import importlib
from pathlib import Path

from .common import CheckResult


def run_gate(session_number: int, project_dir: Path) -> list[dict]:
    """Run all gate checks for a session. Returns list of check result dicts."""
    module_map = {
        1: "gate_s01_slash_commands",
        2: "gate_s02_memory",
        3: "gate_s03_skills",
        4: "gate_s04_subagents",
        5: "gate_s05_mcp",
        6: "gate_s06_hooks",
        7: "gate_s07_plugins",
        8: "gate_s08_checkpoints",
        9: "gate_s09_advanced",
        10: "gate_s10_cli",
    }

    module_name = module_map.get(session_number)
    if not module_name:
        return [{
            "passed": False,
            "message": f"No gate defined for session {session_number}",
            "points": 0,
        }]

    try:
        gate_module = importlib.import_module(f".{module_name}", package="workshop.gates")
        results: list[CheckResult] = gate_module.check(project_dir)
        return [r.to_dict() for r in results]
    except ImportError as e:
        return [{
            "passed": False,
            "message": f"Gate module not found: {module_name} ({e})",
            "points": 0,
        }]
    except Exception as e:
        return [{
            "passed": False,
            "message": f"Gate error: {e}",
            "points": 0,
        }]
