"""
PhishCLI - Gmail Connection Manager

Handles connecting to and disconnecting from Gmail.
"""

from googleapiclient.discovery import build

from gmail.gmail_auth import GmailAuthenticator


class GmailConnection:
    """
    Handles Gmail connection management.
    """

    @staticmethod
    def connect():
        """
        Connects to Gmail using OAuth.
        """

        print("\n" + "=" * 60)
        print("CONNECT GMAIL")
        print("=" * 60)

        print("\nOpening Google authentication...\n")

        creds = GmailAuthenticator.authenticate()

        service = build(
            "gmail",
            "v1",
            credentials=creds,
        )

        profile = (
            service.users()
            .getProfile(userId="me")
            .execute()
        )

        email = profile.get("emailAddress", "Unknown")

        print("\n✓ Gmail connected successfully.")
        print(f"Connected Account : {email}")

        return email

    @staticmethod
    def disconnect():
        """
        Disconnects Gmail by removing the saved OAuth token.
        """

        print("\n" + "=" * 60)
        print("DISCONNECT GMAIL")
        print("=" * 60)

        if GmailAuthenticator.logout():

            print("\n✓ Gmail disconnected successfully.")

        else:

            print("\nNo Gmail account is currently connected.")

    @staticmethod
    def is_connected():
        """
        Returns True if Gmail is already connected.
        """

        return GmailAuthenticator.is_authenticated()