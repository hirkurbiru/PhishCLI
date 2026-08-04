"""
PhishCLI - Session Manager

Manages the current Gmail session.
"""

from pathlib import Path
import json


BASE_DIR = Path(__file__).resolve().parent.parent

SECRETS_DIR = BASE_DIR / "secrets"

SESSION_FILE = SECRETS_DIR / "session.json"


class SessionManager:
    """
    Handles the active Gmail session.
    """

    @staticmethod
    def save(email):
        """
        Save the connected Gmail account.
        """

        SECRETS_DIR.mkdir(parents=True, exist_ok=True)

        with open(SESSION_FILE, "w", encoding="utf-8") as file:

            json.dump(
                {
                    "connected": True,
                    "email": email,
                },
                file,
                indent=4,
            )

    @staticmethod
    def load():
        """
        Load the current Gmail session.
        """

        if not SESSION_FILE.exists():

            return None

        with open(
            SESSION_FILE,
            "r",
            encoding="utf-8",
        ) as file:

            return json.load(file)

    @staticmethod
    def clear():
        """
        Remove the current Gmail session.
        """

        if SESSION_FILE.exists():

            SESSION_FILE.unlink()

    @staticmethod
    def is_connected():
        """
        Returns True if a Gmail account is connected.
        """

        session = SessionManager.load()

        if not session:

            return False

        return session.get(
            "connected",
            False,
        )

    @staticmethod
    def get_email():
        """
        Returns the connected Gmail address.
        """

        session = SessionManager.load()

        if not session:

            return None

        return session.get("email")