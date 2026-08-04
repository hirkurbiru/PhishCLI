"""
Tests for KeywordDetector.
"""

from analysis.detectors.keyword_detector import KeywordDetector


detector = KeywordDetector()


def test_safe_email():

    email = {
        "subject": "Weekly Team Meeting",
        "body": "Please review the meeting notes before tomorrow."
    }

    result = detector.analyze(email)

    assert result.triggered is False
    assert result.score_impact == 0
    assert result.evidence["count"] == 0


def test_single_keyword():

    email = {
        "subject": "",
        "body": "Please verify your account immediately."
    }

    result = detector.analyze(email)

    assert result.triggered is True
    assert result.score_impact == 5
    assert result.evidence["count"] == 1


def test_keyword_in_subject():

    email = {
        "subject": "Security Alert",
        "body": ""
    }

    result = detector.analyze(email)

    assert result.triggered is True
    assert result.score_impact == 5


def test_multiple_keywords():

    email = {
        "subject": "Security Alert",
        "body": (
            "Verify your account. "
            "Password expired. "
            "Login immediately."
        )
    }

    result = detector.analyze(email)

    assert result.triggered is True
    assert result.evidence["count"] == 4
    assert result.score_impact == 20


def test_score_cap():

    email = {
        "subject": (
            "Security Alert "
            "Verify your account "
            "Password expired "
            "Account suspended "
            "Login immediately "
            "Update your account "
            "Confirm your identity"
        ),
        "body": (
            "Wire transfer. "
            "Payment failed. "
            "Click below. "
            "Reset your password."
        )
    }

    result = detector.analyze(email)

    assert result.triggered is True
    assert result.score_impact == detector.weight


def test_case_insensitive():

    email = {
        "subject": "SECURITY ALERT",
        "body": "VERIFY YOUR ACCOUNT"
    }

    result = detector.analyze(email)

    assert result.triggered is True
    assert result.evidence["count"] == 2


def test_empty_body():

    email = {
        "subject": "",
        "body": ""
    }

    result = detector.analyze(email)

    assert result.triggered is False
    assert result.score_impact == 0


def test_missing_fields():

    email = {}

    result = detector.analyze(email)

    assert result.triggered is False
    assert result.score_impact == 0


def test_no_false_positive():

    email = {
        "subject": "Password Manager Tips",
        "body": "This article explains how to create strong passwords."
    }

    result = detector.analyze(email)

    assert result.triggered is False


def test_multiple_duplicate_keywords():

    email = {
        "subject": "",
        "body": (
            "Verify your account. "
            "Verify your account. "
            "Verify your account."
        )
    }

    result = detector.analyze(email)

    # Regex counts each keyword pattern once,
    # even if it appears multiple times.
    assert result.triggered is True
    assert result.evidence["count"] == 1
    assert result.score_impact == 5