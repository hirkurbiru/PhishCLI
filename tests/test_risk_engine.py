"""
Tests for RiskEngine.
"""

from analysis.scoring import RiskEngine


class DummyDetector:
    """
    Mock detector result.
    """

    def __init__(self, triggered, score):
        self.triggered = triggered
        self.score_impact = score


def test_safe_email():

    detectors = [
        DummyDetector(False, 20),
        DummyDetector(False, 15),
    ]

    score, classification = RiskEngine.calculate_risk(
        detectors,
        {},
    )

    assert score == 0
    assert classification == "Safe"


def test_suspicious_email():

    detectors = [
        DummyDetector(True, 35),
    ]

    score, classification = RiskEngine.calculate_risk(
        detectors,
        {},
    )

    assert score == 35
    assert classification == "Suspicious"


def test_high_risk_email():

    detectors = [
        DummyDetector(True, 75),
    ]

    score, classification = RiskEngine.calculate_risk(
        detectors,
        {},
    )

    assert score == 75
    assert classification == "High Risk"


def test_phishing_email():

    detectors = [
        DummyDetector(True, 95),
    ]

    score, classification = RiskEngine.calculate_risk(
        detectors,
        {},
    )

    assert score == 95
    assert classification == "Phishing"


def test_score_limit():

    detectors = [
        DummyDetector(True, 500),
    ]

    score, _ = RiskEngine.calculate_risk(
        detectors,
        {},
    )

    assert score == 100