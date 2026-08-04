"""
Tests for JSON report generation.
"""

import json
from pathlib import Path

from reports.json_report import export_json_report


def test_json_report_creation():
    """
    Verify that the JSON report is created successfully.
    """

    export_json_report()

    report_file = Path(
        "reports_output/investigation_report.json"
    )

    assert report_file.exists()

    with open(
        report_file,
        "r",
        encoding="utf-8",
    ) as f:
        report = json.load(f)

    assert report["tool"] == "PhishCLI"
    assert "generated_at" in report
    assert "summary" in report
    assert "emails" in report