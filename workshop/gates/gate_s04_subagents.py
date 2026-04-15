"""Session 4 gate: Subagents — agent files, bug tracker module."""

from pathlib import Path

from .common import (
    CheckResult, bonus, dir_exists, min_file_count,
    yaml_frontmatter_exists,
)


def check(project_dir: Path) -> list[CheckResult]:
    results = [
        # Agents directory exists
        dir_exists(project_dir, ".claude/agents",
                   "Agents directory exists (.claude/agents/)", 15),

        # At least 2 agent files
        min_file_count(project_dir, ".claude/agents", "*.md", 2,
                       "At least 2 agent definition files", 15),
    ]

    # Check frontmatter on agent files
    agents_dir = project_dir / ".claude/agents"
    if agents_dir.exists():
        agent_files = list(agents_dir.glob("*.md"))
        for af in agent_files[:3]:
            rel = af.relative_to(project_dir)
            results.append(
                yaml_frontmatter_exists(
                    project_dir, str(rel),
                    required_fields=["description"],
                    message=f"Agent has frontmatter: {rel}",
                    points=10,
                )
            )

    results.extend([
        # Bug tracker functionality exists
        min_file_count(project_dir, ".", "*.jsx", 4,
                       "At least 4 React components (bug tracker added)", 15),

        # Agents reference skills from S3 (progressive dependency)
        _check_agent_references_skills(project_dir),

        # Bonus: agent with tool restrictions
        bonus(_check_agent_has_tool_restrictions(project_dir)),
    ])

    return results


def _check_agent_references_skills(project_dir: Path) -> CheckResult:
    """Verify that at least one agent references skills from S3."""
    agents_dir = project_dir / ".claude/agents"
    if not agents_dir.exists():
        return CheckResult(False, "Agents reference skills from S3", 10)

    for agent_file in agents_dir.glob("*.md"):
        content = agent_file.read_text(errors="replace").lower()
        if "skill" in content or ".claude/skills" in content:
            return CheckResult(True, "Agent references skills (S3 dependency)", 10)

    return CheckResult(
        False, "No agent references skills from S3 (progressive dependency)", 10,
        critical=False,
    )


def _check_agent_has_tool_restrictions(project_dir: Path) -> CheckResult:
    """Check if any agent has tool restrictions in frontmatter."""
    agents_dir = project_dir / ".claude/agents"
    if not agents_dir.exists():
        return CheckResult(False, "Bonus: Agent with tool restrictions", 10)

    for agent_file in agents_dir.glob("*.md"):
        content = agent_file.read_text(errors="replace")
        if "tools:" in content or "allowedTools:" in content:
            return CheckResult(True, "Bonus: Agent with tool restrictions", 10)

    return CheckResult(False, "Bonus: Agent with tool restrictions", 10)
