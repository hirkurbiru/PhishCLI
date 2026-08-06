"""
PhishCLI - Session Manager

Manages the active PhishCLI profile session.
"""

import json
from pathlib import Path

from accounts.storage import AccountStorage


BASE_DIR = Path(__file__).resolve().parent.parent

SECRETS_DIR = BASE_DIR / "secrets"
SECRETS_DIR.mkdir(parents=True, exist_ok=True)

SESSION_FILE = SECRETS_DIR / "session.json"


class SessionManager:
    """
    Handles the active profile session.
    """

    @staticmethod
    def save(profile_name: str, email: str):
        """
        Save the active profile session.
        """

        with open(
            SESSION_FILE,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                {
                    "connected": True,
                    "profile": profile_name,
                    "email": email,
                },
                file,
                indent=4,
            )

    @staticmethod
    def load():
        """
        Load the active session.
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
        Remove the active session.
        """

        if SESSION_FILE.exists():

            SESSION_FILE.unlink()

    @staticmethod
    def is_connected():
        """
        Returns True if a profile is connected.
        """

        session = SessionManager.load()

        if session is None:

            return False

        return session.get(
            "connected",
            False,
        )

    @staticmethod
    def get_email():
        """
        Returns the active email address.
        """

        session = SessionManager.load()

        if session is None:

            return None

        return session.get("email")

    @staticmethod
    def get_profile():
        """
        Returns the active profile name.
        """

        session = SessionManager.load()

        if session is None:

            return None

        return session.get("profile")

    @staticmethod
    def switch_profile(profile_name: str):
        """
        Switch to another existing profile.
        """

        data = AccountStorage.load_accounts()

        if profile_name not in data["profiles"]:

            raise ValueError(
                "Profile not found."
            )

        AccountStorage.switch_profile(
            profile_name
        )

        session = SessionManager.load()

        if session:

            session["profile"] = profile_name

            with open(
                SESSION_FILE,
                "w",
                encoding="utf-8",
            ) as file:

                json.dump(
                    session,
                    file,
                    indent=4,
                )

    @staticmethod
    def get_session():
        """
        Returns the complete session data.
        """

        return SessionManager.load()