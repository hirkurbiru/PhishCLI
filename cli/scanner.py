"""
PhishCLI - Mailbox Scanner

Controls mailbox scanning.
"""

from cli.scan_engine import ScanEngine
from cli.display import pause, show_invalid_option


def scan_mailbox():
    """
    Scan Gmail mailbox.
    """

    print("\n" + "=" * 60)
    print("SCAN MAILBOX")
    print("=" * 60)

    print("\nHow many emails would you like to scan?\n")

    print("1. Latest 10")
    print("2. Latest 25")
    print("3. Latest 50")
    print("4. Latest 100")
    print("5. Custom")
    print("6. Back")

    option = input("\nSelect an option: ").strip()

    if option == "1":

        email_limit = 10

    elif option == "2":

        email_limit = 25

    elif option == "3":

        email_limit = 50

    elif option == "4":

        email_limit = 100

    elif option == "5":

        try:

            email_limit = int(
                input("Enter number of emails: ")
            )

        except ValueError:

            show_invalid_option()
            pause()
            return

    elif option == "6":

        return

    else:

        show_invalid_option()
        pause()
        return

    print("\nScanning mailbox...\n")

    engine = ScanEngine()

    summary = engine.scan(email_limit)

    print("=" * 60)
    print("SCAN COMPLETED")
    print("=" * 60)

    print(f"Emails Scanned : {summary['total']}")
    print(f"Safe           : {summary['safe']}")
    print(f"Suspicious     : {summary['suspicious']}")
    print(f"High Risk      : {summary['high_risk']}")
    print(f"Phishing       : {summary['phishing']}")

    pause()