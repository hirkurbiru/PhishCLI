"""
PhishCLI - Account Manager

Manages saved Gmail accounts.
"""

from accounts.storage import AccountStorage


class AccountManager:
    """
    High-level account management.
    """

    @staticmethod
    def show_accounts():
        """
        Displays all saved accounts.
        """

        accounts = AccountStorage.get_accounts()

        active = AccountStorage.get_active_account()

        if not accounts:

            print("\nNo Gmail accounts saved.")

            return

        print("\n" + "=" * 60)
        print("SAVED GMAIL ACCOUNTS")
        print("=" * 60)

        for index, account in enumerate(accounts, start=1):

            marker = ""

            if account == active:

                marker = " (Active)"

            print(f"{index}. {account}{marker}")

    @staticmethod
    def switch_account():
        """
        Switch the active Gmail account.
        """

        accounts = AccountStorage.get_accounts()

        if not accounts:

            print("\nNo saved accounts.")

            return

        AccountManager.show_accounts()

        while True:

            try:

                choice = int(input("\nSelect account: "))

                if 1 <= choice <= len(accounts):

                    break

                print("Invalid selection.")

            except ValueError:

                print("Please enter a valid number.")

        selected = accounts[choice - 1]

        AccountStorage.switch_account(selected)

        print(f"\nActive account changed to: {selected}")

    @staticmethod
    def remove_account():
        """
        Remove a saved account.
        """

        accounts = AccountStorage.get_accounts()

        if not accounts:

            print("\nNo saved accounts.")

            return

        AccountManager.show_accounts()

        while True:

            try:

                choice = int(input("\nSelect account to remove: "))

                if 1 <= choice <= len(accounts):

                    break

                print("Invalid selection.")

            except ValueError:

                print("Please enter a valid number.")

        selected = accounts[choice - 1]

        AccountStorage.remove_account(selected)

        print(f"\nRemoved account: {selected}")

    @staticmethod
    def active_account():

        return AccountStorage.get_active_account()