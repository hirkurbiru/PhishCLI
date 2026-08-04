"""
PhishCLI - Report Manager

Controls report generation.
"""

from reports.json_report import export_json_report
from reports.pdf_report import export_pdf_report


def reports_menu():
    """
    Reports menu.
    """

    while True:

        print("\n" + "=" * 60)
        print("REPORTS")
        print("=" * 60)

        print("1. Export JSON Report")
        print("2. Export PDF Report")
        print("3. Back")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":

            export_json_report()

        elif choice == "2":

            export_pdf_report()

        elif choice == "3":

            break

        else:

            print("\nInvalid option.")