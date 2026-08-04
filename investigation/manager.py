"""
PhishCLI - Investigation Manager

Controls the complete investigation workflow.
"""

from cli.display import pause

from gmail.gmail_connection import GmailConnection

from investigation.start_investigation import start_investigation
from investigation.mailbox_analyzer import analyze_mailbox
from investigation.result_filter import filter_results
from investigation.summary import show_summary
from investigation.results_view import show_results
from investigation.email_investigation import investigate_email


class InvestigationManager:
    """
    Controls the complete investigation process.
    """

    @staticmethod
    def start():
        """
        Starts a mailbox investigation.
        """

        # --------------------------------------------------
        # Check Gmail Connection
        # --------------------------------------------------

        if not GmailConnection.is_connected():

            print("\n" + "=" * 60)
            print("START INVESTIGATION")
            print("=" * 60)

            print("\nNo Gmail account is connected.")
            print("Please connect your Gmail account first.")

            pause()
            return

        # --------------------------------------------------
        # Select Investigation Scope
        # --------------------------------------------------

        email_limit = start_investigation()

        if email_limit is None:
            return

        # --------------------------------------------------
        # Analyze Mailbox
        # --------------------------------------------------

        investigation = analyze_mailbox(email_limit)

        # --------------------------------------------------
        # Display Investigation Summary
        # --------------------------------------------------

        show_summary(investigation)

        # --------------------------------------------------
        # Filter Results
        # --------------------------------------------------

        flagged_emails = filter_results(
            investigation["findings"],
            minimum_score=60,
        )

        if not flagged_emails:

            print(
                "\nNo emails exceeded the investigation threshold "
                "(Risk Score ≥ 60)."
            )

            pause()
            return

        # --------------------------------------------------
        # Results Viewer
        # --------------------------------------------------

        selected_email = show_results(flagged_emails)

        if selected_email is None:
            return

        # --------------------------------------------------
        # Detailed Investigation
        # --------------------------------------------------

        investigate_email(selected_email)