"""
PhishCLI - Gmail OAuth Authentication

Handles Google OAuth authentication and token management.
"""

from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly"
]


class GmailAuthenticator:
    """
    Handles Gmail OAuth authentication.
    """

    BASE_DIR = Path(__file__).resolve().parent.parent

    SECRETS_DIR = BASE_DIR / "secrets"

    CREDENTIALS_FILE = SECRETS_DIR / "credentials.json"

    TOKEN_FILE = SECRETS_DIR / "token.json"

    @classmethod
    def authenticate(cls):
        """
        Authenticates the user with Gmail OAuth.

        Returns:
            Credentials: Authorized Gmail credentials.
        """

        creds = None

        # --------------------------------------------------
        # Load existing OAuth token
        # --------------------------------------------------

        if cls.TOKEN_FILE.exists():

            creds = Credentials.from_authorized_user_file(
                str(cls.TOKEN_FILE),
                SCOPES,
            )

        # --------------------------------------------------
        # Valid token
        # --------------------------------------------------

        if creds and creds.valid:

            return creds

        # --------------------------------------------------
        # Refresh expired token
        # --------------------------------------------------

        if creds and creds.expired and creds.refresh_token:

            creds.refresh(Request())

        else:

            if not cls.CREDENTIALS_FILE.exists():

                raise FileNotFoundError(
                    f"credentials.json not found:\n{cls.CREDENTIALS_FILE}"
                )

            flow = InstalledAppFlow.from_client_secrets_file(
                str(cls.CREDENTIALS_FILE),
                SCOPES,
            )

            creds = flow.run_local_server(port=0)

        # --------------------------------------------------
        # Save token
        # --------------------------------------------------

        cls.TOKEN_FILE.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(cls.TOKEN_FILE, "w") as token:

            token.write(creds.to_json())

        return creds

    @classmethod
    def is_authenticated(cls):
        """
        Returns True if a Gmail OAuth token exists.
        """

        return cls.TOKEN_FILE.exists()

    @classmethod
    def logout(cls):
        """
        Removes the saved Gmail OAuth token.
        """

        if cls.TOKEN_FILE.exists():

            cls.TOKEN_FILE.unlink()

            return True

        return False