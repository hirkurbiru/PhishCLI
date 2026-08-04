"""
PhishCLI - Keyword & Social Engineering Heuristic Detector

Scans email subject and body for phishing and
social engineering indicators.
"""

import re
from typing import Dict, Any

from analysis.detectors.base import (
    BaseDetector,
    DetectorResult,
)


class KeywordDetector(BaseDetector):
    """
    Detects phishing keywords inside the email.
    """

    PHISHING_KEYWORDS = [
        r"\bverify your account\b",
        r"\burgent action required\b",
        r"\bpassword expired\b",
        r"\bbank account\b",
        r"\bpayment failed\b",
        r"\bsecurity alert\b",
        r"\bsuspicious activity\b",
        r"\bclick here to update\b",
        r"\blogin immediately\b",
        r"\bwire transfer\b",
        r"\bconfirm your identity\b",
        r"\bverify your identity\b",
        r"\bupdate your account\b",
        r"\baccount suspended\b",
        r"\bclick below\b",
        r"\breset your password\b",
    ]

    @property
    def name(self) -> str:
        return "Keyword Detector"

    @property
    def weight(self) -> float:
        return 20.0

    def analyze(
        self,
        email_data: Dict[str, Any],
    ) -> DetectorResult:

        # ------------------------------------------
        # Use parser output
        # ------------------------------------------

        body = email_data.get("body", "")

        subject = email_data.get("subject", "")

        text = f"{subject}\n{body}".lower()

        matches = []

        # ------------------------------------------
        # Search patterns
        # ------------------------------------------

        for pattern in self.PHISHING_KEYWORDS:

            if re.search(pattern, text):

                keyword = (
                    pattern.replace(r"\b", "")
                    .replace("\\", "")
                )

                matches.append(keyword)

        triggered = len(matches) > 0

        score = min(
            len(matches) * 5.0,
            self.weight,
        )

        if triggered:

            description = (
                "Potential phishing keywords detected."
            )

        else:

            description = (
                "No phishing keywords detected."
            )

        return DetectorResult(
            detector_name=self.name,
            score_impact=score,
            triggered=triggered,
            description=description,
            evidence={
                "matched_keywords": matches,
                "count": len(matches),
            },
        )