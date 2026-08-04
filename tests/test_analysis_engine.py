"""
Tests for AnalysisOrchestrator.
"""

from analysis.engine import AnalysisOrchestrator


class DummyIntel:
    """Mock threat intelligence manager."""

    def __init__(self):
        self.virustotal = self

    def analyze_domain(self, domain):
        return {
            "whois": {
                "is_new_domain": False
            }
        }

    def analyze_url(self, url):
        return {
            "virustotal": {
                "malicious": 0
            }
        }

    def check_hash(self, sha256):
        return {
            "malicious": 0
        }


def create_engine():
    engine = AnalysisOrchestrator()
    engine.intelligence = DummyIntel()
    return engine


def test_empty_email():

    engine = create_engine()

    result = engine.analyze_email({})

    assert "risk_score" in result
    assert "classification" in result
    assert "iocs" in result
    assert isinstance(result["detector_results"], list)


def test_sender_ioc():

    engine = create_engine()

    email = {
        "sender": "alice@example.com"
    }

    result = engine.analyze_email(email)

    iocs = result["iocs"]

    assert {
        "type": "EMAIL_ADDRESS",
        "value": "alice@example.com"
    } in iocs

    assert {
        "type": "DOMAIN",
        "value": "example.com"
    } in iocs


def test_url_ioc():

    engine = create_engine()

    email = {
        "urls": [
            {
                "raw_url": "https://example.com",
                "domain": "example.com",
                "has_ip_host": False,
            }
        ]
    }

    result = engine.analyze_email(email)

    assert any(
        ioc["type"] == "URL"
        for ioc in result["iocs"]
    )


def test_attachment_ioc():

    engine = create_engine()

    email = {
        "attachments": [
            {
                "filename": "invoice.pdf",
                "sha256": "abc123",
                "md5": "xyz789",
            }
        ]
    }

    result = engine.analyze_email(email)

    assert any(
        ioc["type"] == "ATTACHMENT"
        for ioc in result["iocs"]
    )

    assert any(
        ioc["type"] == "SHA256"
        for ioc in result["iocs"]
    )


def test_message_id_ioc():

    engine = create_engine()

    email = {
        "message_id": "<123@example.com>"
    }

    result = engine.analyze_email(email)

    assert any(
        ioc["type"] == "MESSAGE_ID"
        for ioc in result["iocs"]
    )


def test_result_structure():

    engine = create_engine()

    result = engine.analyze_email({})

    expected = {
        "email_data",
        "risk_score",
        "classification",
        "explanation",
        "detector_results",
        "osint_data",
        "iocs",
    }

    assert expected.issubset(result.keys())