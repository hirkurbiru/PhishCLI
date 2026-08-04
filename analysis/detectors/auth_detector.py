"""
PhishCLI - Authentication Detector

Checks SPF, DKIM and DMARC authentication results.
"""

from typing import Dict, Any

from analysis.detectors.base import (
    BaseDetector,
    DetectorResult,
)


class AuthDetector(BaseDetector):
    """
    Detects email authentication failures.
    """

    @property
    def name(self) -> str:
        return "Authentication Detector (SPF/DKIM/DMARC)"

    @property
    def weight(self) -> float:
        return 30.0

    def analyze(
        self,
        email_data: Dict[str, Any],
    ) -> DetectorResult:

        auth = email_data.get(
            "auth_results",
            {},
        )

        spf = auth.get(
            "spf",
            "unknown",
        )

        dkim = auth.get(
            "dkim",
            "unknown",
        )

        dmarc = auth.get(
            "dmarc",
            "unknown",
        )

        findings = []

        penalty = 0.0

        # -------------------------------------
        # SPF
        # -------------------------------------

        if str(spf).strip().lower() == "fail":

            penalty += 10

            findings.append("SPF Failed")

        # -------------------------------------
        # DKIM
        # -------------------------------------

        if str(dkim).strip().lower() == "fail":

            penalty += 10

            findings.append("DKIM Failed")

        # -------------------------------------
        # DMARC
        # -------------------------------------

        if str(dmarc).strip().lower() == "fail":

            penalty += 10

            findings.append("DMARC Failed")

        triggered = penalty > 0

        if triggered:

            description = (
                "Authentication failures detected: "
                + ", ".join(findings)
            )

        else:

            description = (
                "SPF, DKIM and DMARC passed "
                "or no failures detected."
            )

        return DetectorResult(

            detector_name=self.name,

            score_impact=min(
                penalty,
                self.weight,
            ),

            triggered=triggered,

            description=description,

            evidence={

                "spf": spf,

                "dkim": dkim,

                "dmarc": dmarc,

                "findings": findings,

            },
        )