"""
Tests for ScanRepository search methods.
"""

import uuid

from database.connection import SessionLocal
from database.repository import ScanRepository


def unique_message_id():
    return f"<{uuid.uuid4()}@pytest>"


def create_email(repo, session):

    email = {
        "message_id": unique_message_id(),
        "subject": "Invoice Payment",
        "sender": "alice@example.com",
        "recipient": "bob@example.com",
        "reply_to": "alice@example.com",
        "return_path": "alice@example.com",
        "date": "2026-08-04",
        "body": "Invoice attached.",
        "headers": {},
    }

    iocs = [
        {
            "type": "DOMAIN",
            "value": "example.com",
        }
    ]

    repo.save_email_analysis(
        session.id,
        email,
        15,
        "Suspicious",
        "Unit Test",
        [],
        iocs,
    )

    return email


def test_search_sender():

    db = SessionLocal()
    repo = ScanRepository(db)

    session = repo.create_scan_session("TEST")

    create_email(repo, session)

    results = repo.search_by_sender("alice")

    assert len(results) >= 1

    db.close()


def test_search_subject():

    db = SessionLocal()
    repo = ScanRepository(db)

    session = repo.create_scan_session("TEST")

    create_email(repo, session)

    results = repo.search_by_subject("Invoice")

    assert len(results) >= 1

    db.close()


def test_search_message_id():

    db = SessionLocal()
    repo = ScanRepository(db)

    session = repo.create_scan_session("TEST")

    email = create_email(repo, session)

    results = repo.search_by_message_id(
        email["message_id"]
    )

    assert len(results) == 1

    db.close()


def test_search_ioc():

    db = SessionLocal()
    repo = ScanRepository(db)

    session = repo.create_scan_session("TEST")

    create_email(repo, session)

    results = repo.search_ioc(
        "example.com"
    )

    assert len(results) >= 1

    db.close()


def test_global_search():

    db = SessionLocal()
    repo = ScanRepository(db)

    session = repo.create_scan_session("TEST")

    create_email(repo, session)

    results = repo.global_search(
        "alice"
    )

    assert len(results) >= 1

    db.close()