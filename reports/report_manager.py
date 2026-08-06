"""
PhishCLI - Report Manager

Controls report generation.
"""

from reports.json_report import export_json_report
from reports.pdf_report import export_pdf_report

from accounts.session import SessionManager


def reports_menu():
    """
    Reports menu.
    """

    while True:

        print("\n" + "=" * 60)
        print("REPORTS")
        print("=" * 60)

        if SessionManager.is_connected():

            print(
                f"Profile : {SessionManager.get_profile()}"
            )

            print(
                f"Gmail   : {SessionManager.get_email()}"
            )

        else:

            print("No active profile.")

        print("\n" + "-" * 60)

        print("1. Export JSON Report")
        print("2. Export PDF Report")
        print("3. Back")

        print("\n" + "-" * 60)

        choice = input(
            "\nSelect an option: "
        ).strip()

        # ------------------------------------
        # JSON Report
        # ------------------------------------

        if choice == "1":

            export_json_report()

        # ------------------------------------
        # PDF Report
        # ------------------------------------

        elif choice == "2":

            export_pdf_report()

        # ------------------------------------
        # Back
        # ------------------------------------

        elif choice == "3":

            break

        else:

            print("\nInvalid option.")