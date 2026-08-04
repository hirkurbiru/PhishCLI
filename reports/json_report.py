"""
PhishCLI - JSON Report Generator

Exports investigation history into a structured JSON report.
"""

import json
from pathlib import Path
from datetime import datetime

from database.connection import SessionLocal
from database.repository import ScanRepository

REPORT_DIR = Path("reports_output")
REPORT_DIR.mkdir(exist_ok=True)


def export_json_report():
    """
    Export investigation history as a JSON report.
    """

    db = SessionLocal()

    try:

        repository = ScanRepository(db)

        history = repository.get_scan_history()

        summary = repository.get_mailbox_summary()

        report = {

            "tool": "PhishCLI",

            "version": "1.0",

            "generated_at": datetime.now().isoformat(),

            "summary": {

                "total_sessions": summary["total_sessions"],

                "total_emails": summary["total_emails"],

                "safe": summary["safe"],

                "suspicious": summary["suspicious"],

                "high_risk": summary["high_risk"],

                "phishing": summary["phishing"],

            },

            "emails": [],
        }

        for email, analysis in history:

            report["emails"].append(

                {

                    "email_id": email.id,

                    "message_id": email.message_id,

                    "sender": email.sender,

                    "recipient": email.recipient,

                    "subject": email.subject,

                    "reply_to": email.reply_to,

                    "return_path": email.return_path,

                    "date_sent": email.date_sent,

                    "risk_score": analysis.risk_score,

                    "classification": analysis.classification,

                    "analysis_summary": analysis.explanation_summary,

                }

            )

        report_file = REPORT_DIR / "investigation_report.json"

        with open(
            report_file,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                report,
                file,
                indent=4,
                default=str,
            )

        print("\n" + "=" * 60)
        print("JSON REPORT EXPORTED")
        print("=" * 60)

        print(f"\nLocation : {report_file}")

        print(
            f"Emails   : {summary['total_emails']}"
        )

        print(
            f"Safe     : {summary['safe']}"
        )

        print(
            f"Suspicious : {summary['suspicious']}"
        )

        print(
            f"High Risk : {summary['high_risk']}"
        )

        print(
            f"Phishing : {summary['phishing']}"
        )

    finally:

        db.close()