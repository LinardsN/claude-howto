"""Session 3 gate: Skills — SKILL.md files, test suite page."""

from pathlib import Path

from .common import (
    CheckResult, bonus, min_file_count, yaml_frontmatter_exists,
)


def check(project_dir: Path) -> list[CheckResult]:
    results = [
        # At least 2 skills created
        min_file_count(project_dir, ".claude/skills", "SKILL.md", 2,
                       "At least 2 SKILL.md files in .claude/skills/", 20),
    ]

    # Check frontmatter on each SKILL.md found
    skills_dir = project_dir / ".claude/skills"
    if skills_dir.exists():
        skill_files = list(skills_dir.rglob("SKILL.md"))
        for sf in skill_files[:3]:  # Check up to 3
            rel = sf.relative_to(project_dir)
            results.append(
                yaml_frontmatter_exists(
                    project_dir, str(rel),
                    required_fields=["description"],
                    message=f"SKILL.md has frontmatter with description: {rel}",
                    points=10,
                )
            )
    else:
        results.append(CheckResult(
            False, "Skills directory .claude/skills/ not found", 10
        ))

    results.extend([
        # Test suite page exists (React component)
        min_file_count(project_dir, ".", "*.jsx", 3,
                       "At least 3 React components (test suite page added)", 15),

        # Bonus: skill with supporting files (templates/scripts)
        bonus(min_file_count(project_dir, ".claude/skills", "*", 4,
                             "Bonus: Skills have supporting files", 10)),
    ])

    return results
