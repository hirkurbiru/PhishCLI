"""
Tests for AttachmentDetector.
"""

from analysis.detectors.attachment_detector import AttachmentDetector


detector = AttachmentDetector()


def test_no_attachments():

    email = {
        "attachments": []
    }

    result = detector.analyze(email)

    assert result.triggered is False
    assert result.score_impact == 0


def test_safe_attachment():

    email = {
        "attachments": [
            {
                "filename": "report.pdf"
            }
        ]
    }

    result = detector.analyze(email)

    assert result.triggered is False
    assert result.score_impact == 0


def test_executable_attachment():

    email = {
        "attachments": [
            {
                "filename": "virus.exe"
            }
        ]
    }

    result = detector.analyze(email)

    assert result.triggered is True
    assert result.score_impact == 25
    assert len(result.evidence["flagged"]) == 1


def test_script_attachment():

    email = {
        "attachments": [
            {
                "filename": "payload.js"
            }
        ]
    }

    result = detector.analyze(email)

    assert result.triggered is True
    assert result.score_impact == 25


def test_macro_attachment():

    email = {
        "attachments": [
            {
                "filename": "invoice.docm"
            }
        ]
    }

    result = detector.analyze(email)

    assert result.triggered is True
    assert result.score_impact == 15


def test_archive_attachment():

    email = {
        "attachments": [
            {
                "filename": "documents.zip"
            }
        ]
    }

    result = detector.analyze(email)

    assert result.triggered is True
    assert result.score_impact == 5


def test_multiple_attachments():

    email = {
        "attachments": [
            {
                "filename": "virus.exe"
            },
            {
                "filename": "macro.docm"
            },
            {
                "filename": "archive.zip"
            },
        ]
    }

    result = detector.analyze(email)

    assert result.triggered is True

    # 25 + 15 + 5 = 45
    # capped at detector weight
    assert result.score_impact == 35

    assert len(result.evidence["flagged"]) == 3


def test_double_extension():

    email = {
        "attachments": [
            {
                "filename": "invoice.pdf.exe"
            }
        ]
    }

    result = detector.analyze(email)

    assert result.triggered is True
    assert result.score_impact == 25


def test_uppercase_extension():

    email = {
        "attachments": [
            {
                "filename": "MALWARE.EXE"
            }
        ]
    }

    result = detector.analyze(email)

    assert result.triggered is True
    assert result.score_impact == 25


def test_missing_filename():

    email = {
        "attachments": [
            {}
        ]
    }

    result = detector.analyze(email)

    assert result.triggered is False
    assert result.score_impact == 0