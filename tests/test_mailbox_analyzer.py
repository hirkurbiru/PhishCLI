"""
Tests for Mailbox Analyzer.
"""

from unittest.mock import MagicMock, patch

from investigation.mailbox_analyzer import (
    analyze_mailbox,
    format_time,
    create_progress_bar,
)


def test_format_time():

    assert format_time(0) == "00:00"
    assert format_time(65) == "01:05"
    assert format_time(125) == "02:05"


def test_progress_bar():

    bar, percent = create_progress_bar(5, 10)

    assert len(bar) == 40
    assert percent == 50.0


def test_progress_bar_zero():

    bar, percent = create_progress_bar(0, 0)

    assert len(bar) == 40
    assert percent == 0


@patch("investigation.mailbox_analyzer.GmailFetcher")
def test_empty_mailbox(mock_fetcher):

    mock_fetcher.return_value.get_email_list.return_value = []

    result = analyze_mailbox(10)

    assert result["investigation_id"] is None
    assert result["statistics"]["total"] == 0
    assert result["failed"] == 0


@patch("investigation.mailbox_analyzer.ScanRepository")
@patch("investigation.mailbox_analyzer.SessionLocal")
@patch("investigation.mailbox_analyzer.AnalysisOrchestrator")
@patch("investigation.mailbox_analyzer.GmailParser")
@patch("investigation.mailbox_analyzer.GmailFetcher")
def test_single_email(
    mock_fetcher,
    mock_parser,
    mock_analyzer,
    mock_session,
    mock_repo,
):

    mock_fetcher.return_value.get_email_list.return_value = [
        {"id": "1"}
    ]

    mock_fetcher.return_value.get_message.return_value = {}

    mock_parser.return_value.parse.return_value = {
        "subject": "Test",
        "sender": "alice@example.com",
    }

    mock_analyzer.return_value.analyze_email.return_value = {
        "risk_score": 10,
        "classification": "Safe",
        "explanation": "",
        "detector_results": [],
        "iocs": [],
    }

    repo = MagicMock()

    repo.create_scan_session.return_value.id = 1

    mock_repo.return_value = repo

    result = analyze_mailbox(1)

    assert result["statistics"]["total"] == 1
    assert result["failed"] == 0


@patch("investigation.mailbox_analyzer.ScanRepository")
@patch("investigation.mailbox_analyzer.SessionLocal")
@patch("investigation.mailbox_analyzer.AnalysisOrchestrator")
@patch("investigation.mailbox_analyzer.GmailParser")
@patch("investigation.mailbox_analyzer.GmailFetcher")
def test_failed_email(
    mock_fetcher,
    mock_parser,
    mock_analyzer,
    mock_session,
    mock_repo,
):

    mock_fetcher.return_value.get_email_list.return_value = [
        {"id": "1"}
    ]

    mock_fetcher.return_value.get_message.side_effect = Exception(
        "Failure"
    )

    repo = MagicMock()

    repo.create_scan_session.return_value.id = 1

    mock_repo.return_value = repo

    result = analyze_mailbox(1)

    assert result["failed"] == 1