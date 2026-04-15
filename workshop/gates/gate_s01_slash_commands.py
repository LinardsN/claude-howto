"""Session 1 gate: Slash Commands — project init, landing page, custom commands."""

from pathlib import Path

from .common import (
    CheckResult, bonus, dir_exists, file_contains, file_exists,
    min_file_count, package_json_has_dep,
)


def check(project_dir: Path) -> list[CheckResult]:
    return [
        # Project structure exists
        file_exists(project_dir, "package.json",
                    "Project initialized with package.json", 15),
        package_json_has_dep(project_dir, "express",
                             "Express backend dependency installed", 10),
        package_json_has_dep(project_dir, "react",
                             "React frontend dependency installed", 10),

        # Server entry point
        file_exists(project_dir, "server/index.js",
                    "Express server entry point exists", 10)
        if (project_dir / "server").exists()
        else file_contains(project_dir, "package.json", r"express",
                           "Express server configured", 10),

        # Landing page exists (React component or HTML)
        min_file_count(project_dir, ".", "*.jsx", 1,
                       "At least one React component (.jsx) exists", 10)
        if not (project_dir / "client/src").exists()
        else dir_exists(project_dir, "client/src",
                        "React client source directory exists", 10),

        # Custom slash commands
        dir_exists(project_dir, ".claude/skills",
                   "Custom skills directory exists (.claude/skills/)", 15),
        min_file_count(project_dir, ".claude/skills", "SKILL.md", 1,
                       "At least 1 custom skill (SKILL.md) created", 15),

        # Bonus: second custom skill
        bonus(min_file_count(project_dir, ".claude/skills", "SKILL.md", 2,
                             "Bonus: 2+ custom skills created", 15)),
    ]
