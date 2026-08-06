"""
PhishCLI - Login System

Handles Gmail authentication and PhishCLI profile login.
"""

from accounts.storage import AccountStorage
from accounts.session import SessionManager
from accounts.account_manager import AccountManager

from gmail.gmail_connection import GmailConnection


class LoginManager:
    """
    Handles profile login operations.
    """

    @staticmethod
    def login():
        """
        Login using Gmail OAuth.
        """

        print("\n" + "=" * 60)
        print("PROFILE LOGIN")
        print("=" * 60)

        profile_name = input(
            "\nProfile Name: "
        ).strip()

        if not profile_name:

            print("\nProfile name cannot be empty.")

            return

        safe_profile = (
            profile_name
            .strip()
            .lower()
            .replace(" ", "_")
        )

        # ---------------------------------------------
        # Create profile if it does not exist
        # ---------------------------------------------

        created_new_profile = False

        if not AccountStorage.profile_exists(
            safe_profile
        ):

            AccountStorage.create_profile(
                profile_name=safe_profile,
                email="",
            )

            created_new_profile = True

        # ---------------------------------------------
        # Activate Profile
        # ---------------------------------------------

        AccountStorage.switch_profile(
            safe_profile
        )

        SessionManager.save(
            safe_profile,
            "",
        )

        print(
            "\nOpening browser for Gmail authentication..."
        )

        # ---------------------------------------------
        # Gmail Authentication
        # ---------------------------------------------

        try:

            email = GmailConnection.connect(
                force_login=True
            )

        except Exception as e:

            # Remove empty profile if authentication fails
            if created_new_profile:

                AccountStorage.delete_profile(
                    safe_profile
                )

            print(
                f"\nAuthentication failed:\n{e}"
            )

            return

        # ---------------------------------------------
        # Save Session
        # ---------------------------------------------

        SessionManager.save(
            safe_profile,
            email,
        )

        print("\n" + "=" * 60)
        print("LOGIN SUCCESSFUL")
        print("=" * 60)

        print(f"Profile : {safe_profile}")
        print(f"Gmail   : {email}")

    @staticmethod
    def login_menu():
        """
        Displays the profile manager menu.
        """

        while True:

            print("\n" + "=" * 60)
            print("PROFILE MANAGER")
            print("=" * 60)

            print("1. Login / Create Profile")
            print("2. View Profiles")
            print("3. Switch Profile")
            print("4. Delete Profile")
            print("5. Back")

            choice = input(
                "\nSelect an option: "
            ).strip()

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