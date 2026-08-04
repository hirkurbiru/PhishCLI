"""
PhishCLI - Settings Menu

Allows the user to view and modify application settings.
"""

from settings.config_manager import (
    ConfigManager,
    DEFAULT_SETTINGS,
)


def show_settings():
    """
    Displays the Settings menu.
    """

    while True:

        settings = ConfigManager.load()

        print("\n" + "=" * 60)
        print("SETTINGS")
        print("=" * 60)

        print(f"1. Recent Email Limit      : {settings['max_recent_emails']}")
        print(f"2. VirusTotal Enabled      : {settings['virustotal_enabled']}")
        print(f"3. Report Directory        : {settings['report_directory']}")
        print(f"4. Theme                  : {settings['theme']}")
        print("5. Reset to Default")
        print("6. Back")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":

            try:

                value = int(
                    input(
                        "New Recent Email Limit: "
                    )
                )

                ConfigManager.set(
                    "max_recent_emails",
                    value,
                )

                print("\nUpdated successfully.")

            except ValueError:

                print("\nPlease enter a valid number.")

        elif choice == "2":

            current = settings["virustotal_enabled"]

            ConfigManager.set(
                "virustotal_enabled",
                not current,
            )

            print("\nVirusTotal setting updated.")

        elif choice == "3":

            value = input(
                "Report Directory: "
            ).strip()

            if value:

                ConfigManager.set(
                    "report_directory",
                    value,
                )

                print("\nDirectory updated.")

        elif choice == "4":

            value = input(
                "Theme Name: "
            ).strip()

            if value:

                ConfigManager.set(
                    "theme",
                    value,
                )

                print("\nTheme updated.")

        elif choice == "5":

            ConfigManager.save(
                DEFAULT_SETTINGS.copy()
            )

            print("\nSettings reset successfully.")

        elif choice == "6":

            break

        else:

            print("\nInvalid option.")