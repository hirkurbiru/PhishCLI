"""
PhishCLI - Sender & Mismatch Detector

Analyzes sender identity consistency between
From, Reply-To and Return-Path.
"""

import re

from typing import Dict, Any

from analysis.detectors.base import (
    BaseDetector,
    DetectorResult,
)


class SenderDetector(BaseDetector):
    """
    Detects suspicious sender header mismatches.
    """

    TRUSTED_PARENT_DOMAINS = {
        "google.com",
        "microsoft.com",
        "amazon.com",
        "amazonses.com",
        "outlook.com",
        "office365.com",
        "canva.com",
        "netflix.com",
        "github.com",
        "apple.com",
        "paypal.com",
    }

    @property
    def name(self) -> str:
        return "Header & Sender Mismatch Detector"

    @property
    def weight(self) -> float:
        return 20.0

    def analyze(
        self,
        email_data: Dict[str, Any],
    ) -> DetectorResult:

        sender = self._extract_email_address(
            email_data.get("sender", "")
        )

        reply_to = self._extract_email_address(
            email_data.get("reply_to", "")
        )

        return_path = self._extract_email_address(
            email_data.get("return_path", "")
        )

        sender_domain = self._parent_domain(sender)
        reply_domain = self._parent_domain(reply_to)
        return_domain = self._parent_domain(return_path)

        penalty = 0.0

        mismatches = []

        # -------------------------------------
        # Reply-To mismatch
        # -------------------------------------

        if (
            reply_domain
            and sender_domain
            and reply_domain != sender_domain
        ):

            if (
                sender_domain not in self.TRUSTED_PARENT_DOMAINS
                or reply_domain not in self.TRUSTED_PARENT_DOMAINS
            ):

                penalty += 15.0

                mismatches.append(
                    f"Reply-To domain differs "
                    f"({sender_domain} → {reply_domain})"
                )

        # -------------------------------------
        # Return-Path mismatch
        # -------------------------------------

        if (
            return_domain
            and sender_domain
            and return_domain != sender_domain
        ):

            if (
                sender_domain not in self.TRUSTED_PARENT_DOMAINS
                or return_domain not in self.TRUSTED_PARENT_DOMAINS
            ):

                penalty += 10.0

                mismatches.append(
                    f"Return-Path domain differs "
                    f"({sender_domain} → {return_domain})"
                )

        triggered = penalty > 0

        if triggered:

            description = (
                "Header mismatch detected: "
                + "; ".join(mismatches)
            )

        else:

            description = (
                "Sender headers appear consistent."
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
                "sender": sender,
                "reply_to": reply_to,
                "return_path": return_path,
                "mismatches": mismatches,
            },
        )

    @staticmethod
    def _extract_email_address(raw_header: str) -> str:

        if not raw_header:
            return ""

        match = re.search(
            r"[\w\.-]+@[\w\.-]+\.\w+",
            raw_header,
        )

        if match:
            return match.group(0).lower()

        return raw_header.lower()

    @staticmethod
    def _parent_domain(email: str) -> str:

        if "@" not in email:
            return ""

        domain = email.split("@")[-1]

        parts = domain.split(".")

        if len(parts) >= 2:
            return ".".join(parts[-2:])

        return domain