"""
PhishCLI - Email Investigation Viewer

Displays the complete investigation details for a selected email.
"""

from cli.display import pause


def investigate_email(finding):
    """
    Display the complete investigation details.

    Args:
        finding (dict)
    """

    email = finding.get("email", {})
    analysis = finding.get("analysis", {})

    print("\n" + "=" * 70)
    print("                EMAIL INVESTIGATION")
    print("=" * 70)

    print(f"Risk Score      : {analysis.get('risk_score', 0)}")
    print(f"Classification  : {analysis.get('classification', 'Unknown')}")

    print("-" * 70)

    print(f"From            : {email.get('sender', 'Unknown')}")
    print(f"To              : {email.get('recipient', 'Unknown')}")
    print(f"Subject         : {email.get('subject', 'No Subject')}")
    print(f"Date            : {email.get('date', 'Unknown')}")

    reply_to = email.get("reply_to")

    if reply_to:
        print(f"Reply-To        : {reply_to}")

    return_path = email.get("return_path")

    if return_path:
        print(f"Return-Path     : {return_path}")

    print("-" * 70)

    print("Triggered Detectors")

    detector_results = analysis.get(
        "detector_results",
        [],
    )

    if detector_results:

        for detector in detector_results:

            if detector.triggered:

                print(
                    f"✓ {detector.detector_name}"
                )

                print(
                    f"  Score : +{detector.score_impact}"
                )

                print(
                    f"  {detector.description}"
                )

                print()

    else:

        print("None")

    print("-" * 70)

    print("Threat Intelligence")

    osint = analysis.get(
        "osint_data",
        {},
    )

    if osint:

        whois = osint.get(
            "whois",
            {},
        )

        if whois:

            print(
                f"Domain Age : "
                f"{whois.get('domain_age_days', 'Unknown')} days"
            )

            print(
                f"Registrar  : "
                f"{whois.get('registrar', 'Unknown')}"
            )

        vt = osint.get(
            "virustotal",
            {},
        )

        if vt:

            print(
                f"VirusTotal Malicious : "
                f"{vt.get('malicious', 0)}"
            )

    else:

        print("No threat intelligence available.")

    print("-" * 70)

    print("Indicators of Compromise")

    iocs = analysis.get(
        "iocs",
        [],
    )

    if iocs:

        for ioc in iocs:

            print(
                f"- {ioc['type']} : {ioc['value']}"
            )

    else:

        print("None")

    print("-" * 70)

    print("Recommendation")

    classification = analysis.get(
        "classification",
        "",
    )

    if classification == "Safe":

        print("✓ Email appears legitimate.")

    elif classification == "Suspicious":

        print("⚠ Verify the sender before interacting.")
        print("⚠ Check all links carefully.")

    elif classification == "High Risk":

        print("⚠ Do not open links or attachments.")
        print("⚠ Verify through another communication channel.")

    else:

        print("❌ Treat this email as phishing.")
        print("❌ Delete or report immediately.")

    print("=" * 70)

    pause()