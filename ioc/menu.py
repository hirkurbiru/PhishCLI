"""
IOC Explorer Menu
"""


def show_ioc_menu():

    print("\n" + "=" * 60)
    print("IOC EXPLORER")
    print("=" * 60)

    print("\n1. Domains")
    print("2. URLs")
    print("3. IP Addresses")
    print("4. Email Addresses")
    print("5. SHA256")
    print("6. MD5")
    print("7. Attachments")
    print("8. Back")

    return input("\nSelect an option: ").strip()