"""Analyze efficiency: prompts-to-success ratio per session."""

import json
from pathlib import Path

from .rubric import EFFICIENCY_THRESHOLDS


def analyze_efficiency(log_dir: Path, session_number: int,
                       gate_passed: bool) -> dict:
    """Analyze how efficiently a student completed a session.

    Returns dict with:
        score (0-100), details (dict of metrics)
    """
    prompt_count = _count_prompts(log_dir, session_number)

    if prompt_count == 0:
        return {"score": 0, "details": {"error": "No prompts logged"}}

    if not gate_passed:
        # Session not completed — partial credit based on attempt
        return {
            "score": max(0, 30 - prompt_count * 0.5),
            "details": {
                "prompt_count": prompt_count,
                "gate_passed": False,
                "note": "Session not completed",
            },
        }

    # Score based on prompt count thresholds
    if prompt_count <= EFFICIENCY_THRESHOLDS["excellent"]:
        score = 90 + (EFFICIENCY_THRESHOLDS["excellent"] - prompt_count) * 0.67
    elif prompt_count <= EFFICIENCY_THRESHOLDS["good"]:
        score = 70 + (EFFICIENCY_THRESHOLDS["good"] - prompt_count) * 2
    elif prompt_count <= EFFICIENCY_THRESHOLDS["satisfactory"]:
        score = 50 + (EFFICIENCY_THRESHOLDS["satisfactory"] - prompt_count) * 1.33
    elif prompt_count <= EFFICIENCY_THRESHOLDS["poor"]:
        score = 30 + (EFFICIENCY_THRESHOLDS["poor"] - prompt_count) * 1
    else:
        score = max(0, 30 - (prompt_count - EFFICIENCY_THRESHOLDS["poor"]) * 0.5)

    score = max(0, min(100, score))

    # Analyze retry patterns
    retry_count = _count_retries(log_dir, session_number)
    retry_ratio = retry_count / prompt_count if prompt_count > 0 else 0

    # Penalty for high retry ratio
    if retry_ratio > 0.4:
        score *= 0.85  # 15% penalty for >40% retries

    return {
        "score": round(score, 1),
        "details": {
            "prompt_count": prompt_count,
            "retry_count": retry_count,
            "retry_ratio": round(retry_ratio, 2),
            "gate_passed": gate_passed,
        },
    }


def _count_prompts(log_dir: Path, session_number: int) -> int:
    """Count total prompts for a session."""
    count = 0
    session_dir = log_dir / f"session-{session_number}"
    if not session_dir.exists():
        return 0

    for jsonl_file in session_dir.glob("*.jsonl"):
        for line in jsonl_file.read_text().splitlines():
            try:
                entry = json.loads(line)
                if entry.get("type") == "prompt":
                    count += 1
            except json.JSONDecodeError:
                continue
    return count


def _count_retries(log_dir: Path, session_number: int) -> int:
    """Estimate retry count by detecting similar consecutive prompts."""
    prompts = []
    session_dir = log_dir / f"session-{session_number}"
    if not session_dir.exists():
        return 0

    for jsonl_file in session_dir.glob("*.jsonl"):
        for line in jsonl_file.read_text().splitlines():
            try:
                entry = json.loads(line)
                if entry.get("type") == "prompt":
                    prompts.append(entry.get("content", "").lower().strip())
            except json.JSONDecodeError:
                continue

    retries = 0
    for i in range(1, len(prompts)):
        # Simple similarity: if >60% of words overlap with previous prompt
        prev_words = set(prompts[i - 1].split())
        curr_words = set(prompts[i].split())
        if not prev_words or not curr_words:
            continue
        overlap = len(prev_words & curr_words) / max(len(prev_words), len(curr_words))
        if overlap > 0.6:
            retries += 1

    return retries
