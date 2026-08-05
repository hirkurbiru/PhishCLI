"""
PhishCLI - Account Manager

Displays information about the connected Gmail account.
"""

from accounts.session import SessionManager


class AccountManager:
    """
    Handles connected Gmail account information.
    """

    @staticmethod
    def is_connected():
        """
        Returns True if a Gmail account is connected.
        """

        return SessionManager.is_connected()

    @staticmethod
    def get_email():
        """
        Returns the connected Gmail address.
        """

        return SessionManager.get_email()

    @staticmethod
    def show_account():
        """
        Displays the connected Gmail account.
        """

        print("\n" + "=" * 60)
        print("CONNECTED ACCOUNT")
        print("=" * 60)

        if not SessionManager.is_connected():

            print("\nNo Gmail account connected.")

            return

        print(f"\nEmail : {SessionManager.get_email()}")
        