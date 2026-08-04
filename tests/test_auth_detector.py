"""
Tests for AuthDetector.
"""

from analysis.detectors.auth_detector import AuthDetector


detector = AuthDetector()


def test_all_pass():

    email = {
        "auth_results": {
            "spf": "pass",
            "dkim": "pass",
            "dmarc": "pass",
        }
    }

    result = detector.analyze(email)

    assert result.triggered is False
    assert result.score_impact == 0
    assert "passed" in result.description.lower()


def test_spf_fail():

    email = {
        "auth_results": {
            "spf": "fail",
            "dkim": "pass",
            "dmarc": "pass",
        }
    }

    result = detector.analyze(email)

    assert result.triggered is True
    assert result.score_impact == 10
    assert "SPF Failed" in result.evidence["findings"]


def test_dkim_fail():

    email = {
        "auth_results": {
            "spf": "pass",
            "dkim": "fail",
            "dmarc": "pass",
        }
    }

    result = detector.analyze(email)

    assert result.triggered is True
    assert result.score_impact == 10
    assert "DKIM Failed" in result.evidence["findings"]


def test_dmarc_fail():

    email = {
        "auth_results": {
            "spf": "pass",
            "dkim": "pass",
            "dmarc": "fail",
        }
    }

    result = detector.analyze(email)

    assert result.triggered is True
    assert result.score_impact == 10
    assert "DMARC Failed" in result.evidence["findings"]


def test_spf_dkim_fail():

    email = {
        "auth_results": {
            "spf": "fail",
            "dkim": "fail",
            "dmarc": "pass",
        }
    }

    result = detector.analyze(email)

    assert result.triggered is True
    assert result.score_impact == 20
    assert len(result.evidence["findings"]) == 2


def test_all_fail():

    email = {
        "auth_results": {
            "spf": "fail",
            "dkim": "fail",
            "dmarc": "fail",
        }
    }

    result = detector.analyze(email)

    assert result.triggered is True
    assert result.score_impact == 30
    assert len(result.evidence["findings"]) == 3


def test_unknown_results():

    email = {
        "auth_results": {
            "spf": "unknown",
            "dkim": "unknown",
            "dmarc": "unknown",
        }
    }

    result = detector.analyze(email)

    assert result.triggered is False
    assert result.score_impact == 0


def test_missing_auth_results():

    email = {}

    result = detector.analyze(email)

    assert result.triggered is False
    assert result.score_impact == 0