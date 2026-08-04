"""
PhishCLI - IOC Explorer
"""

from database.connection import SessionLocal
from database.repository import ScanRepository

from ioc.menu import show_ioc_menu


IOC_TYPES = {
    "1": "DOMAIN",
    "2": "URL",
    "3": "IP_ADDRESS",
    "4": "EMAIL_ADDRESS",
    "5": "SHA256",
    "6": "MD5",
    "7": "ATTACHMENT",
}


def show_ioc_explorer():
    """
    Launch the IOC Explorer.
    """

    while True:

        choice = show_ioc_menu()

        if choice == "8":
            break

        ioc_type = IOC_TYPES.get(choice)

        if not ioc_type:
            print("\nInvalid option.")
            input("\nPress Enter...")
            continue

        display_iocs(ioc_type)


def display_iocs(ioc_type: str):

    db = SessionLocal()

    try:

        repository = ScanRepository(db)

        iocs = repository.get_iocs_by_type(ioc_type)

        print("\n" + "=" * 60)
        print(f"{ioc_type}")
        print("=" * 60)

        if not iocs:

            print("\nNo IOC records found.")

        else:

            for index, ioc in enumerate(iocs, start=1):

                print(
                    f"{index}. {ioc.ioc_value}"
                )

        print(f"\nTotal: {len(iocs)}")

        input("\nPress Enter to continue...")

    finally:

        db.close()