"""
Tests for ScanRepository dashboard methods.
"""

import uuid

from database.connection import SessionLocal
from database.repository import ScanRepository


def unique_message_id():
    return f"<{uuid.uuid4()}@pytest>"


def create_sample_email(repo, session):

    email = {
        "message_id": unique_message_id(),
        "subject": "Dashboard Test",
        "sender": "dashboard@example.com",
        "recipient": "user@example.com",
        "reply_to": "dashboard@example.com",
        "return_path": "dashboard@example.com",
        "date": "2026-08-04",
        "body": "Dashboard sample email",
        "headers": {},
    }

    repo.save_email_analysis(
        session_id=session.id,
        email_meta=email,
        risk_score=10,
        classification="Safe",
        explanation="Dashboard Test",
        findings=[],
        iocs=[],
    )


def test_mailbox_summary():

    db = SessionLocal()
    repo = ScanRepository(db)

    session = repo.create_scan_session("TEST")

    create_sample_email(repo, session)

    summary = repo.get_mailbox_summary()

    assert summary["total_sessions"] >= 1
    assert summary["total_emails"] >= 1

    db.close()


def test_top_senders():

    db = SessionLocal()
    repo = ScanRepository(db)

    session = repo.create_scan_session("TEST")

    create_sample_email(repo, session)

    senders = repo.get_top_senders()

    assert len(senders) >= 1

    db.close()


def test_recent_scans():

    db = SessionLocal()
    repo = ScanRepository(db)

    session = repo.create_scan_session("TEST")

    create_sample_email(repo, session)

    scans = repo.get_recent_scans()

    assert len(scans) >= 1

    db.close()


def test_classification_statistics():

    db = SessionLocal()
    repo = ScanRepository(db)

    session = repo.create_scan_session("TEST")

    create_sample_email(repo, session)

    stats = repo.get_classification_statistics()

    assert len(stats) >= 1

    db.close()