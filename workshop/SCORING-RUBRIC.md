# Scoring Rubric

Your bootcamp performance is scored automatically on a 0-100 scale. This document explains exactly how scoring works so there are no surprises.

## Score Breakdown

| Component | Weight | Max Points |
|-----------|--------|------------|
| Prompt Quality | 25% | 25 |
| Efficiency | 15% | 15 |
| Deliverable Quality | 20% | 20 |
| Standards Compliance | 15% | 15 |
| Final Task (Session 10) | 25% | 25 |
| **Total** | **100%** | **100** |

## Component Details

### Prompt Quality (25%)

How well you communicate with Claude Code. Measured across all sessions.

| Score Range | Description |
|-------------|-------------|
| 21-25 | Clear, specific prompts with context. Describes the "what" and "why". Uses domain vocabulary. |
| 16-20 | Good prompts with minor vagueness. Occasionally missing context or constraints. |
| 11-15 | Functional but generic prompts. Often requires follow-up clarification. |
| 6-10 | Vague prompts that lead to multiple retries. Missing key requirements. |
| 0-5 | Copy-pasted prompts from external sources, or single-word commands with no context. |

**What we look for:**

- Specificity: "Add a test case form with fields for title, description, preconditions, steps, expected result, and ISTQB severity" vs "make a form"
- Context awareness: referencing CLAUDE.md standards, previous work, project conventions
- Iterative refinement: when initial results are not right, providing targeted feedback rather than starting over
- Domain expertise: using QA terminology naturally (regression, boundary value, equivalence partitioning)

### Efficiency (15%)

How many prompts it takes you to achieve each goal.

| Score Range | Description |
|-------------|-------------|
| 13-15 | Achieves goals in minimal prompts. Rarely needs to retry or backtrack. |
| 10-12 | Mostly efficient with occasional retries. Good at course-correcting. |
| 7-9 | Some unnecessary retries. Occasionally restarts instead of refining. |
| 4-6 | Frequent retries. Often abandons approaches instead of iterating. |
| 0-3 | Excessive retries with no clear strategy. Repeats the same failed approach. |

### Deliverable Quality (20%)

Whether your QA Command Center meets the session requirements. Measured by gate checks.

| Score Range | Description |
|-------------|-------------|
| 17-20 | All must-have requirements met. Bonus items completed. App runs cleanly. |
| 13-16 | All must-have requirements met. Minor polish issues. |
| 9-12 | Most requirements met. Some functionality incomplete or buggy. |
| 5-8 | Partial completion. Several requirements missing. |
| 0-4 | Minimal completion. App does not run or is missing major features. |

**Gate checks are deterministic** — they verify file existence, content patterns, and structural requirements. No subjective judgment.

### Standards Compliance (15%)

Whether your generated code follows the CLAUDE.md rules you defined in Session 2.

| Score Range | Description |
|-------------|-------------|
| 13-15 | Consistent adherence to project standards. Naming, structure, and patterns match CLAUDE.md. |
| 10-12 | Mostly compliant with minor deviations. |
| 7-9 | Some standards followed, others ignored. Inconsistent patterns. |
| 4-6 | Minimal compliance. Standards defined but not enforced. |
| 0-3 | No meaningful standards compliance. |

### Final Task (25%)

Session 10 includes a graded final task where you independently build a new feature using all 10 Claude Code features you have learned. This is scored on the same four components above (prompt quality, efficiency, deliverables, standards).

## Grade Bands

| Score | Grade | Description |
|-------|-------|-------------|
| 90-100 | Excellent | Expert-level Claude Code usage. Ready to lead AI-assisted projects. |
| 80-89 | Very Good | Strong proficiency. Can work independently with Claude Code. |
| 70-79 | Good | Solid understanding. May need occasional guidance on advanced features. |
| 60-69 | Satisfactory | Basic competency achieved. Should continue practicing. |
| 50-59 | Needs Improvement | Gaps in understanding. Review reference modules and retry weak sessions. |
| 0-49 | Incomplete | Significant gaps. Recommend retaking the bootcamp. |

## When Scoring Happens

- **Continuous**: Every prompt you type is logged and analyzed in the background
- **Per-session**: When you run `./bootcamp complete-session N`, gate checks score deliverables
- **Final**: After Session 10, the full score is calculated from all sessions + final task

## Checking Your Score

```bash
# See current score breakdown
./bootcamp status

# After completing all sessions
./bootcamp status --detailed
```

## Scoring Modes

The scoring engine supports two modes:

- **AI mode** (default): Uses Claude Code to analyze prompt quality for deeper evaluation
- **Heuristic mode** (`--no-ai`): Pattern-based analysis for environments without API access

Your instructor will configure the appropriate mode for your cohort.
