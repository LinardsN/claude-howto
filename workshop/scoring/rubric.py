"""Scoring rubric: weights, thresholds, and grade bands."""

# Component weights (must sum to 1.0 for continuous scoring portion)
CONTINUOUS_WEIGHT = 0.75  # 75% of total from continuous scoring
FINAL_TASK_WEIGHT = 0.25  # 25% of total from final task

COMPONENT_WEIGHTS = {
    "prompt_quality": 0.25 / CONTINUOUS_WEIGHT,      # ~33% of continuous
    "efficiency": 0.15 / CONTINUOUS_WEIGHT,           # ~20% of continuous
    "deliverable_quality": 0.20 / CONTINUOUS_WEIGHT,  # ~27% of continuous
    "standards_compliance": 0.15 / CONTINUOUS_WEIGHT, # ~20% of continuous
}

# Score scale: all components scored 0-100, then weighted
MAX_SCORE = 100

# Prompt quality thresholds
PROMPT_QUALITY_THRESHOLDS = {
    "excellent": {  # 90-100
        "min_avg_length": 50,        # Characters per prompt
        "min_specificity": 0.7,      # Ratio of specific vs generic words
        "max_retry_rate": 0.15,      # Max 15% of prompts are retries
    },
    "good": {  # 70-89
        "min_avg_length": 30,
        "min_specificity": 0.5,
        "max_retry_rate": 0.30,
    },
    "satisfactory": {  # 50-69
        "min_avg_length": 15,
        "min_specificity": 0.3,
        "max_retry_rate": 0.50,
    },
}

# Efficiency thresholds (prompts per successful gate check)
EFFICIENCY_THRESHOLDS = {
    "excellent": 15,     # <=15 prompts per session
    "good": 25,          # <=25 prompts
    "satisfactory": 40,  # <=40 prompts
    "poor": 60,          # <=60 prompts
}

# QA domain keywords for specificity analysis
QA_DOMAIN_KEYWORDS = [
    "test case", "test suite", "bug", "defect", "severity", "priority",
    "regression", "smoke test", "boundary", "equivalence", "precondition",
    "expected result", "actual result", "steps to reproduce", "istqb",
    "acceptance criteria", "user story", "epic", "sprint", "coverage",
    "pass", "fail", "blocked", "in progress", "crud", "api", "endpoint",
    "component", "dashboard", "metric", "chart", "report",
]

# Generic/vague prompt indicators
VAGUE_INDICATORS = [
    "make it work", "fix it", "do the thing", "something",
    "whatever", "just do", "idk", "help me",
]

# Grade bands
GRADE_BANDS = [
    (90, 100, "Excellent", "Expert-level Claude Code usage"),
    (80, 89, "Very Good", "Strong proficiency"),
    (70, 79, "Good", "Solid understanding"),
    (60, 69, "Satisfactory", "Basic competency"),
    (50, 59, "Needs Improvement", "Review and practice needed"),
    (0, 49, "Incomplete", "Significant gaps"),
]


def get_grade(score: float) -> tuple[str, str]:
    """Return (grade_label, description) for a score."""
    for low, high, label, desc in GRADE_BANDS:
        if low <= score <= high:
            return label, desc
    return "Ungraded", "Score out of range"
