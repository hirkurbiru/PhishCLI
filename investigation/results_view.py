"""
PhishCLI - Investigation Results Viewer

Displays flagged emails and lets the user select
an email for detailed investigation.
"""

from cli.display import (
    show_invalid_option,
    pause,
)


def show_results(flagged_emails):
    """
    Display flagged emails and return the selected email.

    Args:
        flagged_emails (list)

    Returns:
        dict | None
    """

    print("\n" + "=" * 70)
    print("                 INVESTIGATION RESULTS")
    print("=" * 70)

    if not flagged_emails:

        print("\nNo flagged emails found.")

        pause()

        return None

    print(
        f"{'ID':<5}"
        f"{'RISK':<8}"
        f"{'CLASSIFICATION':<18}"
        f"{'SENDER':<35}"
    )

    print("-" * 70)

    for index, finding in enumerate(flagged_emails, start=1):

        email = finding.get("email", {})

        analysis = finding.get("analysis", {})

        sender = email.get("sender", "Unknown")

        if len(sender) > 30:
            sender = sender[:27] + "..."

        print(
            f"{index:<5}"
            f"{analysis.get('risk_score', 0):<8}"
            f"{analysis.get('classification', 'Unknown'):<18}"
            f"{sender:<35}"
        )

    print("-" * 70)

    while True:

        choice = input(
            "\nSelect Email (0 = Back): "
        ).strip()

        if choice == "0":

            return None

        if choice.isdigit():

            number = int(choice)

            if 1 <= number <= len(flagged_emails):

                return flagged_emails[number - 1]

        show_invalid_option()