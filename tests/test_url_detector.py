"""
Tests for URLDetector.
"""

from analysis.detectors.url_detector import URLDetector


detector = URLDetector()


def test_no_urls():

    email = {
        "urls": []
    }

    result = detector.analyze(email)

    assert result.triggered is False
    assert result.score_impact == 0


def test_http_url():

    email = {
        "urls": [
            {
                "raw_url": "http://example.com",
                "scheme": "http",
                "domain": "example.com",
                "has_ip_host": False,
            }
        ]
    }

    result = detector.analyze(email)

    assert result.triggered is True
    assert result.score_impact == 10
    assert len(result.evidence["http_urls"]) == 1


def test_ip_url():

    email = {
        "urls": [
            {
                "raw_url": "http://192.168.1.10/login",
                "scheme": "http",
                "domain": "192.168.1.10",
                "has_ip_host": True,
            }
        ]
    }

    result = detector.analyze(email)

    assert result.triggered is True
    assert len(result.evidence["ip_urls"]) == 1


def test_shortener():

    email = {
        "urls": [
            {
                "raw_url": "https://bit.ly/abc123",
                "scheme": "https",
                "domain": "bit.ly",
                "has_ip_host": False,
            }
        ]
    }

    result = detector.analyze(email)

    assert result.triggered is True
    assert len(result.evidence["shortened_urls"]) == 1


def test_suspicious_tld():

    email = {
        "urls": [
            {
                "raw_url": "https://bank-login.zip",
                "scheme": "https",
                "domain": "bank-login.zip",
                "has_ip_host": False,
            }
        ]
    }

    result = detector.analyze(email)

    assert result.triggered is True
    assert len(result.evidence["suspicious_tld_urls"]) == 1


def test_http_and_ip():

    email = {
        "urls": [
            {
                "raw_url": "http://10.0.0.1/login",
                "scheme": "http",
                "domain": "10.0.0.1",
                "has_ip_host": True,
            }
        ]
    }

    result = detector.analyze(email)

    assert result.triggered is True
    assert result.score_impact == 25


def test_all_url_risks():

    email = {
        "urls": [
            {
                "raw_url": "http://bit.ly/login.zip",
                "scheme": "http",
                "domain": "bit.ly",
                "has_ip_host": True,
            },
            {
                "raw_url": "https://fakebank.zip",
                "scheme": "https",
                "domain": "fakebank.zip",
                "has_ip_host": False,
            },
        ]
    }

    result = detector.analyze(email)

    assert result.triggered is True

    # capped at detector weight
    assert result.score_impact == 40


def test_https_legitimate():

    email = {
        "urls": [
            {
                "raw_url": "https://google.com",
                "scheme": "https",
                "domain": "google.com",
                "has_ip_host": False,
            }
        ]
    }

    result = detector.analyze(email)

    assert result.triggered is False
    assert result.score_impact == 0


def test_multiple_http_urls():

    email = {
        "urls": [
            {
                "raw_url": "http://example1.com",
                "scheme": "http",
                "domain": "example1.com",
                "has_ip_host": False,
            },
            {
                "raw_url": "http://example2.com",
                "scheme": "http",
                "domain": "example2.com",
                "has_ip_host": False,
            },
        ]
    }

    result = detector.analyze(email)

    assert len(result.evidence["http_urls"]) == 2
    assert result.score_impact == 10


def test_missing_url_fields():

    email = {
        "urls": [
            {}
        ]
    }

    result = detector.analyze(email)

    assert result.triggered is False
    assert result.score_impact == 0