"""
PhishCLI - Investigation Result Filter

Filters investigation results based on risk score.
"""


def filter_results(findings, minimum_score=60):
    """
    Returns only emails whose risk score is greater than
    or equal to the specified minimum score.

    Args:
        findings (list): Investigation findings.
        minimum_score (int): Minimum risk score.

    Returns:
        list
    """

    filtered = []

    for finding in findings:

        analysis = finding.get("analysis", {})

        risk_score = analysis.get(
            "risk_score",
            0,
        )

        if risk_score >= minimum_score:

            filtered.append(finding)

    filtered.sort(
        key=lambda finding: finding["analysis"].get(
            "risk_score",
            0,
        ),
        reverse=True,
    )

    return filtered