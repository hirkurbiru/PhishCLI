"""
PhishCLI - Search Menu
"""


def show_search_menu():
    """
    Display search menu.
    """

    print("\n" + "=" * 60)
    print("SEARCH")
    print("=" * 60)

    print("\n1. Global Search")
    print("2. Search Sender")
    print("3. Search Subject")
    print("4. Search Message ID")
    print("5. Search IOC")
    print("6. Back")

    return input("\nSelect an option: ").strip()