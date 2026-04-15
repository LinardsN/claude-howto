"""Session 2 gate: Memory — CLAUDE.md, rules, test case CRUD."""

from pathlib import Path

from .common import (
    CheckResult, bonus, dir_exists, file_contains, file_exists,
    min_file_count,
)


def check(project_dir: Path) -> list[CheckResult]:
    # Check rules directory has at least one file
    rules_dir = project_dir / ".claude/rules"
    has_rule_files = (
        rules_dir.exists()
        and any(f.is_file() for f in rules_dir.iterdir())
    )

    # Check for test case files
    has_test_case_files = any(
        "test" in f.name.lower() and "case" in f.name.lower()
        for f in project_dir.rglob("*")
        if f.is_file() and "node_modules" not in str(f)
    )

    return [
        # CLAUDE.md exists and has content
        file_exists(project_dir, "CLAUDE.md",
                    "Project CLAUDE.md exists", 15),
        file_contains(project_dir, "CLAUDE.md", r"(test|qa|quality|istqb)",
                      "CLAUDE.md references QA/testing domain", 10),

        # Rules directory
        dir_exists(project_dir, ".claude/rules",
                   "Rules directory exists (.claude/rules/)", 10),
        CheckResult(
            has_rule_files,
            "At least one rule file in .claude/rules/",
            5,
        ),

        # Test case model/routes
        CheckResult(
            has_test_case_files,
            "Test case files exist (model or route)",
            10,
        ),

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
