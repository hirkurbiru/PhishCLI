"""
PhishCLI - Main CLI Controller

Controls application navigation.
"""

from cli.menu import show_main_menu
from cli.history import show_history

from dashboard.dashboard import show_dashboard
from reports.report_manager import reports_menu
from settings.settings import show_settings

from gmail.gmail_connection import GmailConnection

from investigation.manager import InvestigationManager
from investigation.eml_investigation import investigate_eml

from ioc.explorer import show_ioc_explorer
from search.search_engine import launch_search


def main():
    """
    Starts the PhishCLI application.
    """

    while True:

        choice = show_main_menu()

        # --------------------------------------------------
        # Connect Gmail
        # --------------------------------------------------

        if choice == "1":

            GmailConnection.connect()

        # --------------------------------------------------
        # Gmail Investigation
        # --------------------------------------------------

        elif choice == "2":

            InvestigationManager.start()

        # --------------------------------------------------
        # EML Investigation
        # --------------------------------------------------

        elif choice == "3":

            investigate_eml()

        # --------------------------------------------------
        # Investigation History
        # --------------------------------------------------

        elif choice == "4":

            show_history()

        # --------------------------------------------------
        # Dashboard
        # --------------------------------------------------

        elif choice == "5":

            show_dashboard()

        # --------------------------------------------------
        # IOC Explorer
        # --------------------------------------------------

        elif choice == "6":

            show_ioc_explorer()

        # --------------------------------------------------
        # Reports
        # --------------------------------------------------

        elif choice == "7":

            reports_menu()

        # --------------------------------------------------
        # Search
        # --------------------------------------------------

        elif choice == "8":

            launch_search()

        # --------------------------------------------------
        # Settings
        # --------------------------------------------------

        elif choice == "9":

            show_settings()

        # --------------------------------------------------
        # Disconnect Gmail
        # --------------------------------------------------

        elif choice == "10":

            GmailConnection.disconnect()

        # --------------------------------------------------
        # Exit
        # --------------------------------------------------

        elif choice == "11":

            print("\nThank you for using PhishCLI.")
            print("Goodbye!\n")
            break

        # --------------------------------------------------
        # Invalid Option
        # --------------------------------------------------

        else:

            print("\nInvalid option. Please try again.")


if __name__ == "__main__":
    main()