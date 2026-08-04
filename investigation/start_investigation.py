"""
PhishCLI - Start Investigation

Handles investigation scope selection.
"""

from cli.display import (
    show_invalid_option,
    pause,
)


def start_investigation():
    """
    Ask the user how many emails to investigate.

    Returns:
        int | None
        - Returns an integer for the number of emails.
        - Returns -1 for the entire inbox.
        - Returns None if the user cancels.
    """

    print("\n" + "=" * 60)
    print("START INVESTIGATION")
    print("=" * 60)

    print("\nSelect Investigation Scope\n")

    print("1. Latest 10 Emails")
    print("2. Latest 25 Emails")
    print("3. Latest 50 Emails")
    print("4. Latest 100 Emails")
    print("5. Entire Inbox")
    print("6. Back")

    option = input("\nSelect an option: ").strip()

    if option == "1":

        return 10

    elif option == "2":

        return 25

    elif option == "3":

        return 50

    elif option == "4":

        return 100

    elif option == "5":

        print("\nWarning: Entire mailbox scanning may take some time.")

        confirm = input(
            "Continue? (y/n): "
        ).strip().lower()

        if confirm == "y":

            # Special value meaning "scan entire mailbox"
            return -1

        # User cancelled
        return None

    elif option == "6":

        return None

    else:

        show_invalid_option()
        pause()

        return None