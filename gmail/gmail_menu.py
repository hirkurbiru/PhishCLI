"""
PhishCLI - Gmail Manager

Handles Gmail profile management.
"""

from accounts.login import LoginManager
from accounts.account_manager import AccountManager
from accounts.session import SessionManager

from cli.display import pause


def show_gmail_menu():
    """
    Displays the Gmail Manager menu.
    """

    while True:

        print("\n" + "=" * 60)
        print("GMAIL MANAGER")
        print("=" * 60)

        if SessionManager.is_connected():

            print("Status            : Connected")
            print(
                f"Current Profile   : {SessionManager.get_profile()}"
            )
            print(
                f"Connected Gmail   : {SessionManager.get_email()}"
            )

            connect_text = "Connect Another Gmail"

        else:

            print("Status            : Not Connected")

            connect_text = "Connect Gmail"

        print("\n" + "-" * 60)

        print(f"1. {connect_text}")
        print("2. View Profiles")
        print("3. Switch Profile")
        print("4. Delete Profile")
        print("5. Back")

        print("\n" + "-" * 60)

        choice = input("\nSelect an option: ").strip()

        # ----------------------------------------------
        # Connect Gmail
        # ----------------------------------------------

        if choice == "1":

            LoginManager.login()

            pause()

        # ----------------------------------------------
        # View Profiles
        # ----------------------------------------------

        elif choice == "2":

            AccountManager.show_accounts()

            pause()

        # ----------------------------------------------
        # Switch Profile
        # ----------------------------------------------

        elif choice == "3":

            AccountManager.switch_account()

            pause()

        # ----------------------------------------------
        # Delete Profile
        # ----------------------------------------------

        elif choice == "4":

            AccountManager.remove_account()

            pause()

        # ----------------------------------------------
        # Back
        # ----------------------------------------------

        elif choice == "5":

            break

        else:

            print("\nInvalid option.")

            pause()