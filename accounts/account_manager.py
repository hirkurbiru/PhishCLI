"""
PhishCLI - Account Manager

Manages PhishCLI profiles.
"""

from accounts.storage import AccountStorage
from accounts.session import SessionManager

from gmail.gmail_auth import GmailAuthenticator


class AccountManager:
    """
    High-level profile management.
    """

    @staticmethod
    def show_accounts():
        """
        Displays all available profiles.
        """

        profiles = AccountStorage.list_profiles()

        active = AccountStorage.get_active_profile()

        if not profiles:

            print("\nNo profiles found.")

            return

        print("\n" + "=" * 60)
        print("PHISHCLI PROFILES")
        print("=" * 60)

        for index, profile in enumerate(
            profiles,
            start=1,
        ):

            marker = ""

            if profile == active:

                marker = " (Active)"

            print(
                f"{index}. {profile}{marker}"
            )

    @staticmethod
    def switch_account():
        """
        Switch the active profile.
        """

        profiles = AccountStorage.list_profiles()

        if not profiles:

            print("\nNo profiles found.")

            return

        AccountManager.show_accounts()

        while True:

            try:

                choice = int(
                    input(
                        "\nSelect profile: "
                    )
                )

                if 1 <= choice <= len(profiles):

                    break

                print("\nInvalid selection.")

            except ValueError:

                print(
                    "\nPlease enter a valid number."
                )

        selected = profiles[
            choice - 1
        ]

        AccountStorage.switch_profile(
            selected
        )

        session = SessionManager.load()

        if session:

            SessionManager.save(
                selected,
                session.get(
                    "email",
                    "",
                ),
            )

        print(
            f"\nActive profile: {selected}"
        )

    @staticmethod
    def remove_account():
        """
        Deletes a profile.
        """

        profiles = AccountStorage.list_profiles()

        if not profiles:

            print("\nNo profiles found.")

            return

        AccountManager.show_accounts()

        while True:

            try:

                choice = int(
                    input(
                        "\nSelect profile to remove: "
                    )
                )

                if 1 <= choice <= len(profiles):

                    break

                print("\nInvalid selection.")

            except ValueError:

                print(
                    "\nPlease enter a valid number."
                )

        selected = profiles[
            choice - 1
        ]

        confirm = input(
            f'\nDelete profile "{selected}"? (y/n): '
        ).strip().lower()

        if confirm != "y":

            print("\nCancelled.")

            return

        # -------------------------------
        # Was this the active profile?
        # -------------------------------

        active_profile = SessionManager.get_profile()

        AccountStorage.delete_profile(
            selected
        )

        if active_profile == selected:

            SessionManager.clear()

            GmailAuthenticator.logout()

        print(
            f'\nProfile "{selected}" deleted.'
        )

    @staticmethod
    def active_account():
        """
        Returns the active profile.
        """

        return AccountStorage.get_active_profile()