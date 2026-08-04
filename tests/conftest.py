"""
Shared pytest fixtures for PhishCLI.
"""

import pytest


@pytest.fixture
def sample_email():
    """
    Sample parsed email used across multiple tests.
    """
    return {
        "message_id": "msg-001",
        "sender": "attacker@example.com",
        "recipient": "victim@example.com",
        "subject": "Urgent: Verify Your Account",
        "reply_to": "reply@example.com",
        "return_path": "bounce@example.com",
        "body": (
            "Please verify your account immediately by clicking "
            "the link below."
        ),
        "urls": [
            {
                "raw_url": "http://example.com/login",
                "domain": "example.com",
                "has_ip_host": False,
            }
        ],
        "attachments": [
            {
                "filename": "invoice.pdf",
                "sha256": (
                    "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                    "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                ),
                "md5": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
            }
        ],
    }


@pytest.fixture
def sample_statistics():
    """
    Sample statistics dictionary.
    """
    return {
        "total": 10,
        "safe": 6,
        "suspicious": 2,
        "high_risk": 1,
        "phishing": 1,
    }