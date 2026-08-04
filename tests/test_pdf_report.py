"""
Tests for PDF report generation.
"""

from pathlib import Path

from reports.pdf_report import export_pdf_report


def test_pdf_report_creation():

    export_pdf_report()

    report_file = Path(
        "reports_output/investigation_report.pdf"
    )

    assert report_file.exists()

    assert report_file.stat().st_size > 0