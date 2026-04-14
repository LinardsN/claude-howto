"""Analyze prompt quality: clarity, specificity, domain relevance."""

import json
import re
import subprocess
from pathlib import Path

from .rubric import QA_DOMAIN_KEYWORDS, VAGUE_INDICATORS


def analyze_prompts(log_dir: Path, session_number: int,
                    use_ai: bool = False) -> dict:
    """Analyze prompt quality for a student's session.

    Returns dict with:
        score (0-100), details (dict of sub-metrics)
    """
    prompts = _load_prompts(log_dir, session_number)

    if not prompts:
        return {"score": 0, "details": {"error": "No prompts logged"}}

    if use_ai:
        return _analyze_with_ai(prompts)

    return _analyze_heuristic(prompts)


def _load_prompts(log_dir: Path, session_number: int) -> list[str]:
    """Load prompt texts from JSONL log files."""
    prompts = []
    session_dir = log_dir / f"session-{session_number}"
    if not session_dir.exists():
        return prompts

    for jsonl_file in session_dir.glob("*.jsonl"):
        for line in jsonl_file.read_text().splitlines():
            try:
                entry = json.loads(line)
                if entry.get("type") == "prompt":
                    prompts.append(entry.get("content", ""))
            except json.JSONDecodeError:
                continue
    return prompts


def _analyze_heuristic(prompts: list[str]) -> dict:
    """Score prompts using heuristic analysis (no AI required)."""
    if not prompts:
        return {"score": 0, "details": {}}

    total_prompts = len(prompts)

    # 1. Average length (longer = more specific, up to a point)
    avg_length = sum(len(p) for p in prompts) / total_prompts
    length_score = min(100, avg_length * 1.5)  # 67+ chars = 100

    # 2. Domain specificity (QA terminology usage)
    domain_matches = 0
    for prompt in prompts:
        prompt_lower = prompt.lower()
        for keyword in QA_DOMAIN_KEYWORDS:
            if keyword in prompt_lower:
                domain_matches += 1
                break  # Count each prompt once
    specificity_score = min(100, (domain_matches / total_prompts) * 150)

    # 3. Vagueness penalty
    vague_count = 0
    for prompt in prompts:
        prompt_lower = prompt.lower()
        if any(indicator in prompt_lower for indicator in VAGUE_INDICATORS):
            vague_count += 1
    vague_ratio = vague_count / total_prompts
    vagueness_penalty = vague_ratio * 40  # Up to -40 points

    # 4. Structural quality (prompts with context, requirements, examples)
    structural_indicators = [
        r"\b(must|should|need|require)\b",  # Requirements language
        r"\b(because|since|so that)\b",     # Reasoning
        r"\b(for example|e\.g\.|such as)\b",  # Examples
        r"\b(using|with|via)\b",            # Tool/method specification
    ]
    structural_count = 0
    for prompt in prompts:
        for pattern in structural_indicators:
            if re.search(pattern, prompt, re.IGNORECASE):
                structural_count += 1
                break
    structural_score = min(100, (structural_count / total_prompts) * 130)

    # Weighted combination
    raw_score = (
        length_score * 0.20
        + specificity_score * 0.30
        + structural_score * 0.30
        + (100 - vagueness_penalty) * 0.20
    )
    final_score = max(0, min(100, raw_score))

    return {
        "score": round(final_score, 1),
        "details": {
            "total_prompts": total_prompts,
            "avg_length": round(avg_length, 1),
            "length_score": round(length_score, 1),
            "domain_specificity": round(specificity_score, 1),
            "structural_quality": round(structural_score, 1),
            "vagueness_penalty": round(vagueness_penalty, 1),
        },
    }


def _analyze_with_ai(prompts: list[str]) -> dict:
    """Score prompts using Claude Code AI analysis."""
    prompt_text = "\n---\n".join(prompts[:50])  # Cap at 50 prompts

    rubric_prompt = f"""Analyze these student prompts from an AI coding bootcamp.
Score each dimension 0-100:

1. CLARITY: Are prompts clear and unambiguous?
2. SPECIFICITY: Do prompts include specific requirements, constraints, details?
3. DOMAIN_RELEVANCE: Do prompts use QA/testing terminology naturally?
4. ITERATIVE_QUALITY: When retrying, do prompts refine rather than repeat?
5. CONTEXT_AWARENESS: Do prompts reference project standards, prior work?

Prompts:
{prompt_text}

Respond ONLY with JSON: {{"clarity": N, "specificity": N, "domain_relevance": N, "iterative_quality": N, "context_awareness": N}}"""

    try:
        result = subprocess.run(
            ["claude", "-p", "--output-format", "json", rubric_prompt],
            capture_output=True, text=True, timeout=60,
        )
        if result.returncode == 0:
            scores = json.loads(result.stdout)
            avg = sum(scores.values()) / len(scores)
            return {
                "score": round(avg, 1),
                "details": scores,
            }
    except (subprocess.SubprocessError, json.JSONDecodeError, FileNotFoundError):
        pass

    # Fallback to heuristic
    return _analyze_heuristic(prompts)
