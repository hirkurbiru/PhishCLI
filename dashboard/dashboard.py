"""
PhishCLI - Dashboard

Displays investigation statistics, top senders,
classification statistics and recent investigations.
"""

from database.connection import SessionLocal
from database.repository import ScanRepository

from cli.display import pause


def show_dashboard():
    """
    Display the PhishCLI dashboard.
    """

    db = SessionLocal()

    try:

        repository = ScanRepository(db)

        summary = repository.get_mailbox_summary()

        top_senders = repository.get_top_senders()

        classifications = repository.get_classification_statistics()

        history = repository.get_recent_scans()

        print("\n" + "=" * 80)
        print("                        PHISHCLI DASHBOARD")
        print("=" * 80)

        # ==================================================
        # Overview
        # ==================================================

        print("\nSYSTEM OVERVIEW")
        print("-" * 80)

        print(
            f"Total Scan Sessions : "
            f"{summary.get('total_sessions', 0)}"
        )

        print(
            f"Total Emails        : "
            f"{summary.get('total_emails', 0)}"
        )

        print(
            f"Safe Emails         : "
            f"{summary.get('safe', 0)}"
        )

        print(
            f"Suspicious Emails   : "
            f"{summary.get('suspicious', 0)}"
        )

        print(
            f"High Risk Emails    : "
            f"{summary.get('high_risk', 0)}"
        )

        print(
            f"Phishing Emails     : "
            f"{summary.get('phishing', 0)}"
        )

        # ==================================================
        # Classification Statistics
        # ==================================================

        print("\nCLASSIFICATION BREAKDOWN")
        print("-" * 80)

        if classifications:

            total = sum(
                count for _, count in classifications
            )

            for classification, count in classifications:

                percentage = (
                    (count / total) * 100
                    if total
                    else 0
                )

                print(
                    f"{classification:<20}"
                    f"{count:<8}"
                    f"{percentage:>6.1f}%"
                )

        else:

            print("No classification data available.")

        # ==================================================
        # Top Senders
        # ==================================================

        print("\nTOP SENDERS")
        print("-" * 80)

        if top_senders:

            for sender, count in top_senders:

                print(
                    f"{sender:<60}"
                    f"{count}"
                )

        else:

            print("No sender data available.")

        # ==================================================
        # Recent Investigations
        # ==================================================

        print("\nRECENT INVESTIGATIONS")
        print("-" * 80)

        if history:

            print(
                f"{'ID':<6}"
                f"{'Risk':<8}"
                f"{'Class':<15}"
                f"Subject"
            )

            print("-" * 80)

            for email, analysis in history:

                subject = email.subject or "No Subject"

                if len(subject) > 45:

                    subject = subject[:42] + "..."

                print(
                    f"{email.id:<6}"
                    f"{analysis.risk_score:<8}"
                    f"{analysis.classification:<15}"
                    f"{subject}"
                )

        else:

            print("No investigations available.")

        # ==================================================
        # Dashboard Footer
        # ==================================================

        print("\n" + "=" * 80)
        print("PhishCLI Professional Email Investigation Dashboard")
        print("=" * 80)

        pause()

    finally:

        db.close()

