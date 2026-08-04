"""
PhishCLI - Investigation History

Displays saved investigations from the local database.
"""

from database.connection import SessionLocal
from database.repository import ScanRepository

from cli.display import pause


def show_history():
    """
    Displays all investigations and allows the
    user to view one.
    """

    db = SessionLocal()

    try:

        repository = ScanRepository(db)

        history = repository.get_scan_history()

        if not history:

            print("\nNo investigations found.")

            pause()

            return

        print("\n" + "=" * 80)
        print("                    INVESTIGATION HISTORY")
        print("=" * 80)

        print(
            f"{'ID':<5}"
            f"{'Risk':<8}"
            f"{'Status':<15}"
            f"Subject"
        )

        print("-" * 80)

        for email, analysis in history:

            subject = email.subject or "No Subject"

            if len(subject) > 40:
                subject = subject[:37] + "..."

            print(
                f"{email.id:<5}"
                f"{analysis.risk_score:<8}"
                f"{analysis.classification:<15}"
                f"{subject}"
            )

        print("-" * 80)

        while True:

            try:

                choice = int(
                    input(
                        "\nEnter Investigation ID (0 = Back): "
                    )
                )

                if choice == 0:
                    return

                email = repository.get_email_by_id(choice)

                if email is None:
                    print("Invalid ID.")
                    continue

                show_investigation_details(email)

                break

            except ValueError:

                print("Please enter a valid number.")

    finally:

        db.close()


def show_investigation_details(email):
    """
    Displays one investigation.
    """

    print("\n" + "=" * 80)
    print("                 INVESTIGATION DETAILS")
    print("=" * 80)

    print(f"Subject      : {email.subject}")
    print(f"Sender       : {email.sender}")
    print(f"Recipient    : {email.recipient}")
    print(f"Reply-To     : {email.reply_to}")
    print(f"Return-Path  : {email.return_path}")
    print(f"Date         : {email.date_sent}")

    if email.analysis:

        print(f"\nRisk Score   : {email.analysis.risk_score}")
        print(f"Status       : {email.analysis.classification}")

        print("\nExplanation")
        print("-" * 80)

        print(email.analysis.explanation_summary)

    print("\nIndicators of Compromise")
    print("-" * 80)

    if email.iocs:

        for ioc in email.iocs:

            print(
                f"[{ioc.ioc_type}] {ioc.ioc_value}"
            )

    else:

        print("No IOCs found.")

    pause()