"""
Tests for SenderDetector.
"""

from analysis.detectors.sender_detector import SenderDetector


detector = SenderDetector()


def test_matching_headers():

    email = {
        "sender": "alice@example.com",
        "reply_to": "alice@example.com",
        "return_path": "alice@example.com",
    }

    result = detector.analyze(email)

    assert result.triggered is False
    assert result.score_impact == 0


def test_reply_to_mismatch():

    email = {
        "sender": "alice@example.com",
        "reply_to": "bob@evil.com",
        "return_path": "alice@example.com",
    }

    result = detector.analyze(email)

    assert result.triggered is True
    assert result.score_impact == 15
    assert len(result.evidence["mismatches"]) == 1


def test_return_path_mismatch():

    email = {
        "sender": "alice@example.com",
        "reply_to": "alice@example.com",
        "return_path": "bounce@evil.com",
    }

    result = detector.analyze(email)

    assert result.triggered is True
    assert result.score_impact == 10
    assert len(result.evidence["mismatches"]) == 1


def test_reply_and_return_path_mismatch():

    email = {
        "sender": "alice@example.com",
        "reply_to": "reply@evil.com",
        "return_path": "bounce@evil.com",
    }

    result = detector.analyze(email)

    assert result.triggered is True

    # capped at detector weight (20)
    assert result.score_impact == 20

    assert len(result.evidence["mismatches"]) == 2


def test_trusted_domains_not_flagged():

    email = {
        "sender": "alerts@google.com",
        "reply_to": "support@google.com",
        "return_path": "mailer@google.com",
    }

    result = detector.analyze(email)

    assert result.triggered is False
    assert result.score_impact == 0


def test_email_address_extraction():

    email = {
        "sender": "Google Support <support@example.com>",
        "reply_to": "Google <support@example.com>",
        "return_path": "<support@example.com>",
    }

    result = detector.analyze(email)

    assert result.triggered is False
    assert result.evidence["sender"] == "support@example.com"


def test_missing_headers():

    email = {}

    result = detector.analyze(email)

    assert result.triggered is False
    assert result.score_impact == 0


def test_empty_headers():

    email = {
        "sender": "",
        "reply_to": "",
        "return_path": "",
    }

    result = detector.analyze(email)

    assert result.triggered is False
    assert result.score_impact == 0


def test_parent_domain_extraction():

    assert (
        detector._parent_domain(
            "user@mail.google.com"
        )
        == "google.com"
    )


def test_extract_email_address():

    assert (
        detector._extract_email_address(
            "John Doe <john@example.com>"
        )
        == "john@example.com"
    )