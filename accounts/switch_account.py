"""
PhishCLI - Switch Gmail Account

Handles switching between Gmail accounts.
"""

from cli.display import pause

from gmail.gmail_connection import GmailConnection


def switch_account():
    """
    Switch to a different Gmail account.
    """

    print("\n" + "=" * 60)
    print("SWITCH GMAIL ACCOUNT")
    print("=" * 60)

    if GmailConnection.is_connected():

        print("\nCurrent Gmail account will be disconnected.")

        confirm = input(
            "\nContinue? (y/n): "
        ).strip().lower()

        if confirm != "y":

            return

        GmailConnection.disconnect()

    print("\nConnecting a new Gmail account...\n")

    GmailConnection.connect()

    pause()