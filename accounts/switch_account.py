"""
PhishCLI - Switch Profile

Handles switching between PhishCLI profiles.
"""

from cli.display import pause

from accounts.account_manager import AccountManager


def switch_account():
    """
    Switch the active PhishCLI profile.
    """

    print("\n" + "=" * 60)
    print("SWITCH PROFILE")
    print("=" * 60)

    AccountManager.switch_account()

    print("\nProfile switched successfully.")

    pause()