"""
PhishCLI - Search Engine
"""

from database.connection import SessionLocal
from database.repository import ScanRepository

from search.menu import show_search_menu
from search.viewer import (
    display_email_results,
    display_ioc_results,
)


def launch_search():

    while True:

        choice = show_search_menu()

        if choice == "6":
            break

        keyword = input("\nEnter search text: ").strip()

        if not keyword:
            print("\nSearch text cannot be empty.")
            continue

        db = SessionLocal()

        try:

            repository = ScanRepository(db)

            if choice == "1":

                results = repository.global_search(keyword)

                display_email_results(results)

            elif choice == "2":

                results = repository.search_by_sender(keyword)

                display_email_results(results)

            elif choice == "3":

                results = repository.search_by_subject(keyword)

                display_email_results(results)

            elif choice == "4":

                results = repository.search_by_message_id(keyword)

                display_email_results(results)

            elif choice == "5":

                results = repository.search_ioc(keyword)

                display_ioc_results(results)

            else:

                print("\nInvalid option.")

        finally:

            db.close()