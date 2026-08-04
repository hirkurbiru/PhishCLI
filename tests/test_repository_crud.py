"""
Tests for ScanRepository CRUD operations.
"""

import uuid

from database.connection import SessionLocal
from database.repository import ScanRepository


def unique_message_id():
    """Generate a unique message ID for testing."""
    return f"<{uuid.uuid4()}@pytest>"


def sample_email():
    """Return sample email metadata."""
    return {
        "message_id": unique_message_id(),
        "subject": "Pytest Email",
        "sender": "alice@example.com",
        "recipient": "bob@example.com",
        "reply_to": "alice@example.com",
        "return_path": "alice@example.com",
        "date": "2026-08-04",
        "body": "Hello from pytest.",
        "headers": {},
    }


def test_create_scan_session():

    db = SessionLocal()
    repo = ScanRepository(db)

    session = repo.create_scan_session(
        target_source="TEST"
    )

    assert session.id is not None
    assert session.target_source == "TEST"

    db.close()


def test_save_email_analysis():

    db = SessionLocal()
    repo = ScanRepository(db)

    session = repo.create_scan_session(
        target_source="TEST"
    )

    email = sample_email()

    record = repo.save_email_analysis(

        session_id=session.id,

        email_meta=email,

        risk_score=20,

        classification="Suspicious",

        explanation="Unit Test",

        findings=[],

        iocs=[],
    )

    assert record.id is not None
    assert record.message_id == email["message_id"]

    db.close()


def test_duplicate_email():

    db = SessionLocal()
    repo = ScanRepository(db)

    session = repo.create_scan_session(
        target_source="TEST"
    )

    email = sample_email()

    first = repo.save_email_analysis(
        session.id,
        email,
        10,
        "Safe",
        "",
        [],
        [],
    )

    second = repo.save_email_analysis(
        session.id,
        email,
        50,
        "Phishing",
        "",
        [],
        [],
    )

    assert first.id == second.id

    db.close()


def test_save_with_findings():

    db = SessionLocal()
    repo = ScanRepository(db)

    session = repo.create_scan_session(
        target_source="TEST"
    )

    email = sample_email()

    findings = [
        {
            "detector_name": "Unit Test Detector",
            "score_impact": 10,
            "triggered": True,
            "description": "Example",
            "evidence": {},
        }
    ]

    record = repo.save_email_analysis(

        session.id,
        email,
        30,
        "Suspicious",
        "Test",
        findings,
        [],
    )

    assert len(record.findings) == 1

    db.close()


def test_save_with_iocs():

    db = SessionLocal()
    repo = ScanRepository(db)

    session = repo.create_scan_session(
        target_source="TEST"
    )

    email = sample_email()

    iocs = [
        {
            "type": "DOMAIN",
            "value": "example.com",
        }
    ]

    record = repo.save_email_analysis(

        session.id,
        email,
        10,
        "Safe",
        "",
        [],
        iocs,
    )

    assert len(record.iocs) == 1

    db.close()