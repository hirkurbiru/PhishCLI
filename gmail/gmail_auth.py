"""
PhishCLI - Gmail OAuth Authentication

Handles Google OAuth authentication and token management.
"""

from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from utils.profile_paths import ProfilePaths
from config.constants import CREDENTIALS_FILE_PATH


SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly"
]


class GmailAuthenticator:
    """
    Handles Gmail OAuth authentication.
    """

    @classmethod
    def get_token_file(cls) -> Path:
        """
        Returns the OAuth token file for the active profile.
        """

        token_file = ProfilePaths.get_token_file()

        token_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        return token_file

    @classmethod
    def authenticate(
        cls,
        force_login: bool = False,
    ):
        """
        Authenticate with Gmail.

        Args:
            force_login:
                If True, ignore the saved token and
                force a new Google authentication.
        """

        token_file = cls.get_token_file()

        creds = None

        # ------------------------------------------
        # Force New Login
        # ------------------------------------------

        if force_login and token_file.exists():

            token_file.unlink()

        # ------------------------------------------
        # Load Existing Token
        # ------------------------------------------

        if token_file.exists():

            creds = Credentials.from_authorized_user_file(
                str(token_file),
                SCOPES,
            )

        # ------------------------------------------
        # Valid Token
        # ------------------------------------------

        if creds and creds.valid:

            return creds

        # ------------------------------------------
        # Refresh Expired Token
        # ------------------------------------------

        if creds and creds.expired and creds.refresh_token:

            creds.refresh(Request())

        else:

            # ------------------------------------------
            # Check Google OAuth Credentials
            # ------------------------------------------

            if not CREDENTIALS_FILE_PATH.exists():

                raise FileNotFoundError(
                    "\n"
                    "Google OAuth credentials were not found.\n\n"
                    f"Expected location:\n{CREDENTIALS_FILE_PATH}\n\n"
                    "Copy your credentials.json file to this location "
                    "and try again."
                )

            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE_PATH),
                SCOPES,
            )

            creds = flow.run_local_server(
                port=0,
                open_browser=True,
            )

        # ------------------------------------------
        # Save Token
        # ------------------------------------------

        with open(
            token_file,
            "w",
            encoding="utf-8",
        ) as token:

            token.write(
                creds.to_json()
            )

        return creds

    @classmethod
    def get_authenticated_email(
        cls,
        force_login: bool = False,
    ):
        """
        Returns the authenticated Gmail address.
        """

        service = cls.get_service(
            force_login=force_login,
        )

        profile = (
            service.users()
            .getProfile(userId="me")
            .execute()
        )

        return profile["emailAddress"]

    @classmethod
    def get_service(
        cls,
        force_login: bool = False,
    ):
        """
        Returns an authenticated Gmail API service.
        """

        creds = cls.authenticate(
            force_login=force_login,
        )

        return build(
            "gmail",
            "v1",
            credentials=creds,
        )

    @classmethod
    def is_authenticated(cls):
        """
        Returns True if the active profile
        has an OAuth token.
        """

        return cls.get_token_file().exists()

    @classmethod
    def logout(cls):
        """
        Deletes the active profile token.
        """

        token_file = cls.get_token_file()

        if token_file.exists():

            token_file.unlink()

            return True

        return False