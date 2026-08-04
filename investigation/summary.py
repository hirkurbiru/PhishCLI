"""
PhishCLI - Investigation Summary

Displays investigation statistics.
"""


def show_summary(investigation):
    """
    Display investigation statistics.
    """

    statistics = investigation["statistics"]

    findings = investigation.get("findings", [])

    flagged = sum(
        1
        for finding in findings
        if finding.get("analysis", {}).get("risk_score", 0) >= 60
    )

    print("\n" + "=" * 70)
    print("                 INVESTIGATION SUMMARY")
    print("=" * 70)

    print(
        f"Investigation ID : {investigation['investigation_id']}"
    )

    print(
        f"Emails Analyzed  : {statistics['total']}"
    )

    print(
        f"Safe Emails      : {statistics['safe']}"
    )

    print(
        f"Suspicious       : {statistics['suspicious']}"
    )

    print(
        f"High Risk        : {statistics['high_risk']}"
    )

    print(
        f"Phishing         : {statistics['phishing']}"
    )

    print("-" * 70)

    print(
        f"Flagged Emails   : {flagged}"
    )

    print("=" * 70)