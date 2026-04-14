"""Session 2 gate: Memory — CLAUDE.md, rules, test case CRUD."""

from pathlib import Path

from .common import (
    CheckResult, bonus, dir_exists, file_contains, file_exists,
    file_not_empty,
)


def check(project_dir: Path) -> list[CheckResult]:
    return [
        # CLAUDE.md exists and has content
        file_exists(project_dir, "CLAUDE.md",
                    "Project CLAUDE.md exists", 15),
        file_contains(project_dir, "CLAUDE.md", r"(test|qa|quality|istqb)",
                      "CLAUDE.md references QA/testing domain", 10),

        # Rules directory
        dir_exists(project_dir, ".claude/rules",
                   "Rules directory exists (.claude/rules/)", 10),
        file_not_empty(project_dir, ".claude/rules",
                       "At least one rule file exists")
        if (project_dir / ".claude/rules").exists()
        and any((project_dir / ".claude/rules").iterdir())
        else CheckResult(False, "Rules directory has rule files", 5),

        # Test case model/routes
        file_contains(project_dir, ".", r"test.?case",
                      "Test case model or route exists", 10)
        if not any(project_dir.rglob("*test*case*"))
        else CheckResult(True, "Test case files found", 10),

        # API routes exist
        file_contains(project_dir, "package.json", r"express",
                      "Express server with API routes", 10),

        # React pages for test cases
        min_file_count(project_dir, ".", "*.jsx", 2,
                       "At least 2 React components exist", 15),

        # Bonus: path-specific rules
        bonus(file_contains(project_dir, "CLAUDE.md",
                            r"(api|server|client|convention|standard)",
                            "Bonus: CLAUDE.md defines conventions", 10)),
    ]
