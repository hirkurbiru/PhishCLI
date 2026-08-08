"""
PhishCLI - Welcome Screen

Displays the first-time setup screen.
"""

from cli.display import show_banner


def show_welcome():
    """
    Display the welcome screen.
    """

    show_banner()

    print("\nEmail Investigation Tool")
    print("=" * 60)

    print("\nWelcome to PhishCLI!")

    print(
        "\nNo Gmail account is currently connected."
    )

    print(
        "\nYou'll need to connect your Gmail account "
        "before starting an investigation."
    )

    input("\nPress ENTER to continue...")
    
