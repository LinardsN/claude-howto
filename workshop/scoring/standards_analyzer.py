"""Analyze standards compliance: CLAUDE.md adherence, naming, structure."""

import json
import re
from pathlib import Path


def analyze_standards(project_dir: Path) -> dict:
    """Analyze how well the project follows its own CLAUDE.md standards.

    Returns dict with:
        score (0-100), details (dict of compliance metrics)
    """
    claude_md = project_dir / "CLAUDE.md"
    if not claude_md.exists():
        return {"score": 20, "details": {"error": "No CLAUDE.md found"}}

    claude_content = claude_md.read_text(errors="replace").lower()

    checks = []

    # 1. Check if project follows naming conventions mentioned in CLAUDE.md
    checks.append(_check_naming_conventions(project_dir, claude_content))

    # 2. Check if API response format is consistent
    checks.append(_check_api_consistency(project_dir))

    # 3. Check if file organization matches CLAUDE.md description
    checks.append(_check_file_organization(project_dir, claude_content))

    # 4. Check for code comments/documentation standards
    checks.append(_check_documentation(project_dir))

    # 5. Check CLAUDE.md itself is well-structured
    checks.append(_check_claude_md_quality(claude_content))

    total = sum(c["score"] for c in checks)
    max_total = sum(c["max"] for c in checks)
    score = (total / max_total * 100) if max_total > 0 else 0

    return {
        "score": round(min(100, score), 1),
        "details": {c["name"]: c for c in checks},
    }


def _check_naming_conventions(project_dir: Path,
                              claude_content: str) -> dict:
    """Check if files follow naming conventions."""
    score = 0
    max_score = 20

    # Check for consistent file naming in server and client dirs
    js_files = [f for f in project_dir.rglob("*.js")
                if "node_modules" not in str(f) and ".git/" not in str(f)]
    jsx_files = [f for f in project_dir.rglob("*.jsx")
                 if "node_modules" not in str(f) and ".git/" not in str(f)]

    all_files = js_files + jsx_files
    if not all_files:
        return {"name": "naming_conventions", "score": 0, "max": max_score}

    # Check for consistent casing (camelCase or kebab-case)
    camel_count = sum(1 for f in all_files
                      if re.match(r"^[a-z][a-zA-Z]*\.", f.name))
    pascal_count = sum(1 for f in all_files
                       if re.match(r"^[A-Z][a-zA-Z]*\.", f.name))
    kebab_count = sum(1 for f in all_files
                      if re.match(r"^[a-z]+-[a-z]", f.name))

    # Consistency bonus
    total = len(all_files)
    dominant = max(camel_count, pascal_count, kebab_count)
    consistency = dominant / total if total > 0 else 0

    if consistency > 0.7:
        score = max_score
    elif consistency > 0.5:
        score = max_score * 0.7
    else:
        score = max_score * 0.4

    return {"name": "naming_conventions", "score": round(score), "max": max_score}


def _check_api_consistency(project_dir: Path) -> dict:
    """Check for consistent API response patterns."""
    score = 0
    max_score = 20

    route_files = list(project_dir.rglob("*route*"))
    route_files += list(project_dir.rglob("*api*"))
    route_files = [f for f in route_files
                   if "node_modules" not in str(f)
                   and f.suffix in (".js", ".ts")
                   and ".git/" not in str(f)]

    if not route_files:
        return {"name": "api_consistency", "score": 10, "max": max_score}

    # Check for consistent response format (res.json patterns)
    response_patterns = 0
    for route_file in route_files:
        content = route_file.read_text(errors="replace")
        if "res.json" in content or "res.status" in content:
            response_patterns += 1

    if response_patterns > 0:
        score = max_score

    return {"name": "api_consistency", "score": round(score), "max": max_score}


def _check_file_organization(project_dir: Path,
                             claude_content: str) -> dict:
    """Check if project has organized file structure."""
    score = 0
    max_score = 20

    # Check for separated concerns
    has_server = (project_dir / "server").exists()
    has_client = (project_dir / "client").exists() or (project_dir / "src").exists()
    has_models = any(project_dir.rglob("*model*"))
    has_routes = any(project_dir.rglob("*route*"))

    if has_server:
        score += 5
    if has_client:
        score += 5
    if has_models:
        score += 5
    if has_routes:
        score += 5

    return {"name": "file_organization", "score": min(score, max_score),
            "max": max_score}


def _check_documentation(project_dir: Path) -> dict:
    """Check for code documentation."""
    score = 0
    max_score = 20

    # Check for README
    if (project_dir / "README.md").exists():
        score += 10

    # Check for comments in JS files
    js_files = [f for f in project_dir.rglob("*.js")
                if "node_modules" not in str(f) and ".git/" not in str(f)]
    commented = 0
    for f in js_files[:10]:  # Sample up to 10 files
        content = f.read_text(errors="replace")
        if "//" in content or "/*" in content:
            commented += 1
    if js_files and commented / min(len(js_files), 10) > 0.5:
        score += 10

    return {"name": "documentation", "score": min(score, max_score),
            "max": max_score}


def _check_claude_md_quality(claude_content: str) -> dict:
    """Check CLAUDE.md itself for quality and completeness."""
    score = 0
    max_score = 20

    # Check for key sections
    key_sections = ["##", "convention", "standard", "rule", "api", "style"]
    for section in key_sections:
        if section in claude_content:
            score += 3

    score = min(score, max_score)
    return {"name": "claude_md_quality", "score": round(score), "max": max_score}
