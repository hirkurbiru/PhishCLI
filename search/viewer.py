"""
PhishCLI - Search Viewer
"""


def display_email_results(results):

    print("\n" + "=" * 70)
    print("SEARCH RESULTS")
    print("=" * 70)

    if not results:

        print("\nNo matching records found.")
        input("\nPress Enter...")
        return

    for index, (email, analysis) in enumerate(results, start=1):

        print(f"\n#{index}")

        print(f"Subject        : {email.subject}")
        print(f"Sender         : {email.sender}")
        print(f"Recipient      : {email.recipient}")
        print(f"Risk Score     : {analysis.risk_score}")
        print(f"Classification : {analysis.classification}")

    print(f"\nTotal Results : {len(results)}")

    input("\nPress Enter...")


def display_ioc_results(results):

    print("\n" + "=" * 70)
    print("IOC RESULTS")
    print("=" * 70)

    if not results:

        print("\nNo IOC found.")
        input("\nPress Enter...")
        return

    for index, ioc in enumerate(results, start=1):

        print(f"{index}. [{ioc.ioc_type}] {ioc.ioc_value}")

    print(f"\nTotal IOC Results : {len(results)}")

    input("\nPress Enter...")