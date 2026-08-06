"""
PhishCLI - PDF Report Generator

Exports investigation history into a professional PDF report.
"""

from datetime import datetime

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib import colors

from database.connection import SessionLocal
from database.repository import ScanRepository

from utils.profile_paths import ProfilePaths
from accounts.session import SessionManager


def export_pdf_report():
    """
    Export investigation history into a professional PDF report.
    """

    report_dir = ProfilePaths.get_reports_dir()

    report_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    report_file = (
        report_dir
        / "investigation_report.pdf"
    )

    db = SessionLocal()

    try:

        repository = ScanRepository(db)

        history = repository.get_scan_history()

        summary = repository.get_mailbox_summary()

        document = SimpleDocTemplate(str(report_file))

        styles = getSampleStyleSheet()

        elements = []

        # ======================================================
        # Title
        # ======================================================

        elements.append(
            Paragraph(
                "PhishCLI Investigation Report",
                styles["Title"],
            )
        )

        elements.append(
            Paragraph(
                f"Generated: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}",
                styles["Normal"],
            )
        )

        elements.append(
            Paragraph(
                f"Profile: {SessionManager.get_profile()}",
                styles["Normal"],
            )
        )

        elements.append(
            Paragraph(
                f"Gmail: {SessionManager.get_email()}",
                styles["Normal"],
            )
        )

        elements.append(Spacer(1, 20))

        # ======================================================
        # Executive Summary
        # ======================================================

        elements.append(
            Paragraph(
                "Executive Summary",
                styles["Heading1"],
            )
        )

        summary_table = Table(
            [
                ["Metric", "Value"],
                ["Total Scan Sessions", summary["total_sessions"]],
                ["Total Emails", summary["total_emails"]],
                ["Safe", summary["safe"]],
                ["Suspicious", summary["suspicious"]],
                ["High Risk", summary["high_risk"]],
                ["Phishing", summary["phishing"]],
            ]
        )

        summary_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ]
            )
        )

        elements.append(summary_table)

        elements.append(Spacer(1, 20))

        # ======================================================
        # Investigation Details
        # ======================================================

        elements.append(
            Paragraph(
                "Investigation Details",
                styles["Heading1"],
            )
        )

        for index, (email, analysis) in enumerate(
            history,
            start=1,
        ):

            elements.append(
                Paragraph(
                    f"<b>Email #{index}</b>",
                    styles["Heading2"],
                )
            )

            elements.append(
                Paragraph(
                    f"<b>Subject:</b> {email.subject}",
                    styles["Normal"],
                )
            )

            elements.append(
                Paragraph(
                    f"<b>Sender:</b> {email.sender}",
                    styles["Normal"],
                )
            )

            elements.append(
                Paragraph(
                    f"<b>Recipient:</b> {email.recipient}",
                    styles["Normal"],
                )
            )

            elements.append(
                Paragraph(
                    f"<b>Date:</b> {email.date_sent}",
                    styles["Normal"],
                )
            )

            elements.append(
                Paragraph(
                    f"<b>Risk Score:</b> {analysis.risk_score}",
                    styles["Normal"],
                )
            )

            elements.append(
                Paragraph(
                    f"<b>Classification:</b> {analysis.classification}",
                    styles["Normal"],
                )
            )

            elements.append(
                Paragraph(
                    f"<b>Summary:</b> {analysis.explanation_summary}",
                    styles["Normal"],
                )
            )

            elements.append(
                Spacer(1, 12)
            )

        # ======================================================
        # Recommendations
        # ======================================================

        elements.append(
            Paragraph(
                "Recommendations",
                styles["Heading1"],
            )
        )

        recommendations = [
            "• Review all Suspicious and High Risk emails.",
            "• Verify sender identity before responding.",
            "• Block malicious domains and URLs.",
            "• Review suspicious attachments before opening.",
            "• Educate users on phishing awareness.",
            "• Enable SPF, DKIM and DMARC validation.",
        ]

        for item in recommendations:

            elements.append(
                Paragraph(
                    item,
                    styles["Normal"],
                )
            )

        elements.append(
            Spacer(1, 20)
        )

        # ======================================================
        # Footer
        # ======================================================

        elements.append(
            Paragraph(
                "<b>Generated by PhishCLI</b>",
                styles["Heading2"],
            )
        )

        elements.append(
            Paragraph(
                "Professional Multi-Profile Email Investigation Framework",
                styles["Normal"],
            )
        )

        document.build(elements)

        print("\n" + "=" * 60)
        print("PDF REPORT EXPORTED")
        print("=" * 60)

        print(f"\nLocation : {report_file}")

        return report_file

    finally:

        db.close()