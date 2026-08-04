"""
PhishCLI - Display Utilities

Centralized display functions for the CLI.
"""


def show_banner():
    """Displays the application banner."""

    print("\n" + "=" * 60)
    print("                 PHISHCLI")
    print("=" * 60)


def show_analysis_result(parsed_email, result):
    """Displays analysis results."""

    print("\n" + "=" * 60)
    print("ANALYSIS RESULT")
    print("=" * 60)

    print(f"Subject : {parsed_email.get('subject', 'N/A')}")
    print(f"Sender  : {parsed_email.get('sender', 'N/A')}")
    print(f"Risk    : {result.get('risk_score', 0)}")
    print(f"Status  : {result.get('classification', 'Unknown')}")

    print("\nExplanation")
    print("-" * 60)

    print(result.get("explanation", "No explanation available."))


def show_investigation_details(email):
    """Displays a saved investigation."""

    print("\n" + "=" * 60)
    print("INVESTIGATION DETAILS")
    print("=" * 60)

    print(f"Subject      : {email.subject}")
    print(f"Sender       : {email.sender}")
    print(f"Recipient    : {email.recipient}")
    print(f"Reply-To     : {email.reply_to}")
    print(f"Return-Path  : {email.return_path}")
    print(f"Date         : {email.date_sent}")

    if email.analysis:

        print("\nRisk Score")
        print("-" * 60)

        print(f"Score        : {email.analysis.risk_score}")
        print(f"Status       : {email.analysis.classification}")

        print("\nExplanation")
        print("-" * 60)

        print(email.analysis.explanation_summary)

    print("\nIndicators of Compromise")
    print("-" * 60)

    if email.iocs:

        for ioc in email.iocs:

            print(f"[{ioc.ioc_type}] {ioc.ioc_value}")

    else:

        print("No IOCs found.")


def show_no_emails():
    """Displays no email message."""

    print("\nNo emails found.")


def show_invalid_option():
    """Displays invalid menu selection."""

    print("\nInvalid option.")


def show_message(message):
    """Displays a generic message."""

    print(f"\n{message}")


def pause():
    """Waits for user input."""

    input("\nPress Enter to continue...")