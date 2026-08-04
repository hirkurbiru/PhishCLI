"""
PhishCLI - Login System

Handles Gmail account login and selection.
"""

from accounts.storage import AccountStorage
from accounts.account_manager import AccountManager

from gmail.gmail_auth import GmailAuthenticator


class LoginManager:
    """
    Handles Gmail login operations.
    """

    @staticmethod
    def login():

        print("\n" + "=" * 60)
        print("GMAIL LOGIN")
        print("=" * 60)

        print("\nOpening browser for Gmail authentication...")

        try:

            GmailAuthenticator.authenticate()

        except Exception as e:

            print(f"\nLogin failed: {e}")

            return

        email = input(
            "\nEnter your Gmail address: "
        ).strip()

        if not email:

            print("\nInvalid email.")

            return

        AccountStorage.add_account(email)

        print("\nLogin successful.")

        print(f"Active Account: {email}")

    @staticmethod
    def login_menu():

        while True:

            print("\n" + "=" * 60)
            print("ACCOUNT MANAGER")
            print("=" * 60)

            print("1. Login Gmail")
            print("2. View Accounts")
            print("3. Switch Account")
            print("4. Remove Account")
            print("5. Back")

            choice = input("\nSelect an option: ").strip()

            if choice == "1":

                LoginManager.login()

            elif choice == "2":

                AccountManager.show_accounts()

            elif choice == "3":

                AccountManager.switch_account()

            elif choice == "4":

                AccountManager.remove_account()

            elif choice == "5":

                break

            else:

                print("\nInvalid option.")