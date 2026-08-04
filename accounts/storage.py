"""
PhishCLI - Account Storage

Stores multiple Gmail accounts and the active account.
"""

import json
from pathlib import Path


DATA_DIR = Path("accounts_data")
DATA_DIR.mkdir(exist_ok=True)

ACCOUNTS_FILE = DATA_DIR / "accounts.json"


class AccountStorage:
    """
    Handles account storage.
    """

    @staticmethod
    def load_accounts():

        if not ACCOUNTS_FILE.exists():

            return {
                "active_account": None,
                "accounts": []
            }

        with open(
            ACCOUNTS_FILE,
            "r",
            encoding="utf-8",
        ) as file:

            return json.load(file)

    @staticmethod
    def save_accounts(data):

        with open(
            ACCOUNTS_FILE,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
            )

    @staticmethod
    def get_accounts():

        return AccountStorage.load_accounts()["accounts"]

    @staticmethod
    def get_active_account():

        return AccountStorage.load_accounts()["active_account"]

    @staticmethod
    def add_account(email):

        data = AccountStorage.load_accounts()

        if email not in data["accounts"]:

            data["accounts"].append(email)

        data["active_account"] = email

        AccountStorage.save_accounts(data)

    @staticmethod
    def switch_account(email):

        data = AccountStorage.load_accounts()

        if email in data["accounts"]:

            data["active_account"] = email

            AccountStorage.save_accounts(data)

    @staticmethod
    def remove_account(email):

        data = AccountStorage.load_accounts()

        if email in data["accounts"]:

            data["accounts"].remove(email)

            if data["active_account"] == email:

                if data["accounts"]:

                    data["active_account"] = data["accounts"][0]

                else:

                    data["active_account"] = None

            AccountStorage.save_accounts(data)