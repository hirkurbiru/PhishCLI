"""
PhishCLI - Explanation Engine

Generates a human-readable explanation of the
email analysis results.
"""

from typing import List, Dict, Any

from analysis.detectors.base import DetectorResult


class ExplanationEngine:
    """
    Generates investigation summaries.
    """

    @staticmethod
    def generate_explanation(
        detector_results: List[DetectorResult],
        osint_data: Dict[str, Any],
        classification: str,
    ) -> str:

        lines = []

        lines.append(
            f"Classification: {classification}"
        )

        lines.append("")

        lines.append(
            "Analysis Summary:"
        )

        findings = False

        # ----------------------------------------
        # Detector Findings
        # ----------------------------------------

        for detector in detector_results:

            if detector.triggered:

                findings = True

                lines.append(
                    f"- {detector.description}"
                )

        # ----------------------------------------
        # Threat Intelligence
        # ----------------------------------------

        if osint_data.get("is_new_domain"):

            findings = True

            lines.append(
                "- Domain is newly registered."
            )

        vt = osint_data.get(
            "virustotal",
            {},
        )

        if vt:

            malicious = vt.get(
                "malicious",
                0,
            )

            if malicious > 0:

                findings = True

                lines.append(
                    f"- VirusTotal detected "
                    f"{malicious} malicious engines."
                )

        abuse = osint_data.get(
            "abuseipdb",
            {},
        )

        if abuse:

            confidence = abuse.get(
                "abuse_confidence_score",
                0,
            )

            if confidence > 0:

                findings = True

                lines.append(
                    f"- AbuseIPDB confidence: "
                    f"{confidence}%."
                )

        # ----------------------------------------
        # No Findings
        # ----------------------------------------

        if not findings:

            lines.append(
                "- No suspicious indicators detected."
            )

        # ----------------------------------------
        # Recommendation
        # ----------------------------------------

        lines.append("")
        lines.append("Recommendation:")

        if classification == "Safe":

            lines.append(
                "- Email appears legitimate."
            )

        elif classification == "Suspicious":

            lines.append(
                "- Verify sender before interacting."
            )

            lines.append(
                "- Be cautious with links and attachments."
            )

        elif classification == "High Risk":

            lines.append(
                "- Do not click any links."
            )

            lines.append(
                "- Verify through another communication channel."
            )

        else:

            lines.append(
                "- Treat this email as phishing."
            )

            lines.append(
                "- Delete or report immediately."
            )

        return "\n".join(lines)