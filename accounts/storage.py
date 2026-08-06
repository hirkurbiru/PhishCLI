"""
PhishCLI - Account Storage

Stores Gmail accounts and manages user profiles
for PhishCLI v1.1.

Backward compatible with v1.0.
"""

import json
import shutil
from datetime import datetime
from pathlib import Path


DATA_DIR = Path("accounts_data")
DATA_DIR.mkdir(exist_ok=True)

ACCOUNTS_FILE = DATA_DIR / "accounts.json"

PROFILES_DIR = DATA_DIR / "profiles"
PROFILES_DIR.mkdir(exist_ok=True)


class AccountStorage:
    """Handles account and profile storage."""

    @staticmethod
    def _default_data():
        """Returns the default storage structure."""
        return {
            "version": "1.1",
            "active_account": None,
            "accounts": [],
            "active_profile": None,
            "profiles": [],
        }

    @staticmethod
    def load_accounts():
        """Loads account storage."""
        if not ACCOUNTS_FILE.exists():
            return AccountStorage._default_data()

        with open(ACCOUNTS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if "version" not in data:
            data["version"] = "1.1"

        if "active_profile" not in data:
            data["active_profile"] = None

        if "profiles" not in data:
            data["profiles"] = []

        return data

    @staticmethod
    def save_accounts(data):
        """Saves account storage."""
        with open(ACCOUNTS_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def get_accounts():
        """Returns all Gmail accounts."""
        return AccountStorage.load_accounts()["accounts"]

    @staticmethod
    def get_active_account():
        """Returns the active Gmail account."""
        return AccountStorage.load_accounts()["active_account"]

    @staticmethod
    def add_account(email):
        """Adds a Gmail account."""
        data = AccountStorage.load_accounts()

        if email not in data["accounts"]:
            data["accounts"].append(email)

        data["active_account"] = email
        AccountStorage.save_accounts(data)

    @staticmethod
    def switch_account(email):
        """Switches active Gmail account."""
        data = AccountStorage.load_accounts()

        if email in data["accounts"]:
            data["active_account"] = email
            AccountStorage.save_accounts(data)

    @staticmethod
    def remove_account(email):
        """Removes a Gmail account."""
        data = AccountStorage.load_accounts()

        if email in data["accounts"]:
            data["accounts"].remove(email)

            if data["active_account"] == email:
                if data["accounts"]:
                    data["active_account"] = data["accounts"][0]
                else:
                    data["active_account"] = None

            AccountStorage.save_accounts(data)

    @staticmethod
    def get_profile_directory(profile_name: str) -> Path:
        """Returns the directory of a profile."""
        safe_name = profile_name.strip().lower().replace(" ", "_")
        return PROFILES_DIR / safe_name

    @staticmethod
    def profile_exists(profile_name: str) -> bool:
        """Checks whether a profile exists."""
        return AccountStorage.get_profile_directory(profile_name).exists()

    @staticmethod
    def create_profile(profile_name: str, email: str = ""):
        """Creates a new profile workspace."""
        profile_dir = AccountStorage.get_profile_directory(profile_name)

        if profile_dir.exists():
            raise ValueError("Profile already exists.")

        profile_dir.mkdir(parents=True, exist_ok=True)

        folders = [
            "reports",
            "database",
            "investigations",
            "exports",
            "logs",
            "attachments",
            "cache",
        ]

        for folder in folders:
            (profile_dir / folder).mkdir(exist_ok=True)

        metadata = {
            "profile_name": profile_name,
            "email": email,
            "created_at": datetime.now().isoformat(),
            "last_login": None,
            "workspace": {
                "database": "database",
                "reports": "reports",
                "investigations": "investigations",
                "exports": "exports",
                "logs": "logs",
                "attachments": "attachments",
                "cache": "cache",
                "token": "token.json",
            },
        }

        with open(profile_dir / "metadata.json", "w", encoding="utf-8") as file:
            json.dump(metadata, file, indent=4)

        data = AccountStorage.load_accounts()
        safe_name = profile_dir.name

        if safe_name not in data["profiles"]:
            data["profiles"].append(safe_name)

        data["active_profile"] = safe_name
        AccountStorage.save_accounts(data)

    @staticmethod
    def list_profiles():
        """Returns all profile names."""
        if not PROFILES_DIR.exists():
            return []

        return sorted(folder.name for folder in PROFILES_DIR.iterdir() if folder.is_dir())

    @staticmethod
    def get_active_profile():
        """Returns the active profile."""
        return AccountStorage.load_accounts()["active_profile"]

    @staticmethod
    def switch_profile(profile_name: str):
        """Switches the active profile."""
        data = AccountStorage.load_accounts()

        if profile_name not in data["profiles"]:
            raise ValueError("Profile not found.")

        data["active_profile"] = profile_name
        AccountStorage.save_accounts(data)

    @staticmethod
    def delete_profile(profile_name: str):
        """Deletes a profile."""
        profile_dir = AccountStorage.get_profile_directory(profile_name)

        if profile_dir.exists():
            shutil.rmtree(profile_dir)

        data = AccountStorage.load_accounts()

        if profile_name in data["profiles"]:
            data["profiles"].remove(profile_name)

            if data["active_profile"] == profile_name:
                if data["profiles"]:
                    data["active_profile"] = data["profiles"][0]
                else:
                    data["active_profile"] = None

            AccountStorage.save_accounts(data)

        if (
            data["active_profile"]
            == profile_name
        ):

            if data["profiles"]:

                data["active_profile"] = (
                    data["profiles"][0]
                )

            else:

                data["active_profile"] = None

        AccountStorage.save_accounts(data)