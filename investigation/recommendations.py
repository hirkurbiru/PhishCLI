"""
PhishCLI - Investigation Recommendations

Provides security recommendations based on
the email risk score.
"""


def show_recommendations(risk_score):
    """
    Display recommendations based on the
    calculated risk score.

    Args:
        risk_score (int | float)
    """

    print("Recommendations")

    print("-" * 90)

    if risk_score >= 90:

        recommendations = [

            "Do NOT click any links or open attachments.",

            "Report the email as phishing immediately.",

            "Block the sender.",

            "Delete the email from your mailbox.",

            "Verify the request through an official channel.",

            "Change your password immediately if you interacted with the email.",

            "Enable Multi-Factor Authentication (MFA) if not already enabled."
        ]

    elif risk_score >= 80:

        recommendations = [

            "Do not click any suspicious links.",

            "Verify the sender before responding.",

            "Inspect attachments carefully.",

            "Report the email if it appears malicious.",

            "Monitor your account for unusual activity."
        ]

    elif risk_score >= 60:

        recommendations = [

            "Exercise caution before taking any action.",

            "Verify the sender's identity.",

            "Check all URLs before opening them.",

            "Avoid downloading unexpected attachments."
        ]

    else:

        recommendations = [

            "No immediate security concerns detected.",

            "Continue following normal email security practices."
        ]

    for recommendation in recommendations:

        print(f"• {recommendation}")