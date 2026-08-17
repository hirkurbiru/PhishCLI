"""
PhishCLI - Main Menu

Displays the application's main menu.
"""

from cli.display import show_banner


def show_main_menu():
    """
    Display the main menu and return the user's choice.
    """

    show_banner()

    print("\nEmail Investigation Tool")
    print("=" * 60)

    print("\n1. Connect Gmail")
    print("2. Start Gmail Investigation")
    print("3. Scan EML File")
    print("4. Investigation History")
    print("5. Dashboard")
    print("6. IOC Explorer")
    print("7. Reports")
    print("8. Search")
    print("9. Settings")
    
    print("10. Disconnect Gmail")
    print("11. Exit")

    return input("\nSelect an option: ").strip()
