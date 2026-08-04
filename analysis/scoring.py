"""
PhishCLI - Risk Scoring Engine

Calculates the final risk score and classification.
"""

from typing import Dict, Any, List

from analysis.detectors.base import DetectorResult

from config.constants import (
    SCORE_MAX,
    SCORE_THRESHOLD_SAFE,
    SCORE_THRESHOLD_SUSPICIOUS,
    SCORE_THRESHOLD_HIGH_RISK,
    CLASS_SAFE,
    CLASS_SUSPICIOUS,
    CLASS_HIGH_RISK,
    CLASS_PHISHING,
)


class RiskEngine:
    """
    Calculates overall email risk.
    """

    @classmethod
    def calculate_risk(
        cls,
        detector_results: List[DetectorResult],
        osint_data: Dict[str, Any],
    ):

        score = 0.0

        # ----------------------------------------
        # Detector Scores
        # ----------------------------------------

        for detector in detector_results:

            if detector.triggered:

                score += detector.score_impact

        # ----------------------------------------
        # WHOIS
        # ----------------------------------------

        if osint_data.get("is_new_domain"):

            score += 15

        # ----------------------------------------
        # VirusTotal
        # ----------------------------------------

        vt = osint_data.get(
            "virustotal",
            {},
        )

        if vt:

            malicious = vt.get(
                "malicious",
                0,
            )

            if malicious >= 5:

                score += 25

            elif malicious > 0:

                score += 10

        # ----------------------------------------
        # AbuseIPDB
        # ----------------------------------------

        abuse = osint_data.get(
            "abuseipdb",
            {},
        )

        if abuse:

            confidence = abuse.get(
                "abuse_confidence_score",
                0,
            )

            if confidence >= 75:

                score += 20

            elif confidence >= 40:

                score += 10

        # ----------------------------------------
        # Final Score
        # ----------------------------------------

        score = min(
            float(score),
            float(SCORE_MAX),
        )

        classification = cls.classify_score(
            score
        )

        return round(
            score,
            1,
        ), classification

    @staticmethod
    def classify_score(
        score: float,
    ):

        if score <= SCORE_THRESHOLD_SAFE:

            return CLASS_SAFE

        elif score <= SCORE_THRESHOLD_SUSPICIOUS:

            return CLASS_SUSPICIOUS

        elif score <= SCORE_THRESHOLD_HIGH_RISK:

            return CLASS_HIGH_RISK

        return CLASS_PHISHING