"""Tests for the scoring engine."""

from workshop.scoring.rubric import get_grade


def test_grade_excellent():
    label, desc = get_grade(95)
    assert label == "Excellent"


def test_grade_good():
    label, desc = get_grade(75)
    assert label == "Good"


def test_grade_incomplete():
    label, desc = get_grade(30)
    assert label == "Incomplete"


def test_grade_boundary_90():
    label, _ = get_grade(90)
    assert label == "Excellent"


def test_grade_boundary_89():
    label, _ = get_grade(89)
    assert label == "Very Good"


def test_grade_boundary_0():
    label, _ = get_grade(0)
    assert label == "Incomplete"
