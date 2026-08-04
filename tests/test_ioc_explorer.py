"""
Tests for IOC Explorer repository methods.
"""

import uuid

from database.connection import SessionLocal
from database.repository import ScanRepository


def unique_message_id():
    return f"<{uuid.uuid4()}@pytest>"


def prepare_email(repo, session):

    email = {
        "message_id": unique_message_id(),
        "subject": "IOC Test",
        "sender": "ioc@example.com",
        "recipient": "user@example.com",
        "reply_to": "ioc@example.com",
        "return_path": "ioc@example.com",
        "date": "2026-08-04",
        "body": "IOC testing",
        "headers": {},
    }

    iocs = [
        {"type": "DOMAIN", "value": "example.com"},
        {"type": "URL", "value": "https://example.com"},
        {"type": "EMAIL_ADDRESS", "value": "ioc@example.com"},
    ]

    repo.save_email_analysis(
        session_id=session.id,
        email_meta=email,
        risk_score=10,
        classification="Safe",
        explanation="IOC Test",
        findings=[],
        iocs=iocs,
    )


def test_domain_iocs():

    db = SessionLocal()
    repo = ScanRepository(db)

    session = repo.create_scan_session("TEST")
    prepare_email(repo, session)

    results = repo.get_iocs_by_type("DOMAIN")

    assert len(results) >= 1

    db.close()


def test_url_iocs():

    db = SessionLocal()
    repo = ScanRepository(db)

    session = repo.create_scan_session("TEST")
    prepare_email(repo, session)

    results = repo.get_iocs_by_type("URL")

    assert len(results) >= 1

    db.close()


def test_email_iocs():

    db = SessionLocal()
    repo = ScanRepository(db)

    session = repo.create_scan_session("TEST")
    prepare_email(repo, session)

    results = repo.get_iocs_by_type("EMAIL_ADDRESS")

    assert len(results) >= 1

    db.close()


def test_top_iocs():

    db = SessionLocal()
    repo = ScanRepository(db)

    session = repo.create_scan_session("TEST")

    prepare_email(repo, session)

    results = repo.get_top_iocs("DOMAIN")

    assert len(results) >= 1

    db.close()