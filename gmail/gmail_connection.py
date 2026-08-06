"""
PhishCLI - Gmail Connection Manager

Handles Gmail API connection.
"""

from googleapiclient.discovery import build

from gmail.gmail_auth import GmailAuthenticator
from accounts.session import SessionManager


class GmailConnection:
    """
    Handles Gmail API connection.
    """

    @staticmethod
    def connect(force_login: bool = False):
        """
        Connect to Gmail using OAuth.

        Args:
            force_login (bool):
                If True, forces a new Gmail authentication.

        Returns:
            str: Authenticated Gmail address.
        """

        print("\n" + "=" * 60)
        print("CONNECT GMAIL")
        print("=" * 60)

        print("\nOpening Google authentication...\n")

        # Authenticate Gmail
        email = GmailAuthenticator.get_authenticated_email(
            force_login=force_login,
        )

        profile = SessionManager.get_profile()

        if profile:

            SessionManager.save(
                profile,
                email,
            )

        print("\n✓ Gmail connected successfully.")
        print(f"Profile       : {profile}")
        print(f"Gmail Account : {email}")

        return email

    @staticmethod
    def disconnect():
        """
        Disconnect Gmail from the active profile.
        """

        print("\n" + "=" * 60)
        print("DISCONNECT GMAIL")
        print("=" * 60)

        GmailAuthenticator.logout()

        SessionManager.clear()

        print("\n✓ Gmail disconnected successfully.")

    @staticmethod
    def is_connected():
        """
        Returns True if the active profile is connected.
        """

        return (
            GmailAuthenticator.is_authenticated()
            and SessionManager.is_connected()
        )

    @staticmethod
    def get_service(force_login: bool = False):
        """
        Returns an authenticated Gmail API service.

        Args:
            force_login (bool):
                If True, forces a new Gmail authentication.
        """

        creds = GmailAuthenticator.authenticate(
            force_login=force_login,
        )

        return build(
            "gmail",
            "v1",
            credentials=creds,
        )