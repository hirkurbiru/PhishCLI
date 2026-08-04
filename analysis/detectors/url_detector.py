"""
PhishCLI - URL Analysis & Typosquatting Detector
Inspects embedded URLs for IP hosts, HTTP protocol usage, URL shorteners, and suspicious TLDs.
"""

from typing import Dict, Any, List
import tldextract
from analysis.detectors.base import BaseDetector, DetectorResult


class URLDetector(BaseDetector):
    """Analyzes embedded URLs for high-risk attributes."""

    SUSPICIOUS_TLDS = {"zip", "mov", "top", "xyz", "work", "click", "country", "kim", "science"}
    KNOWN_SHORTENERS = {"bit.ly", "tinyurl.com", "t.co", "goo.gl", "is.gd", "buff.ly", "ow.ly"}

    @property
    def name(self) -> str:
        return "Embedded URL & Domain Analyzer"

    @property
    def weight(self) -> float:
        return 40.0

    def analyze(self, email_data: Dict[str, Any]) -> DetectorResult:
        urls: List[Dict[str, Any]] = email_data.get("urls", [])
        penalty = 0.0
        findings = []

        ip_urls = []
        http_urls = []
        shortened_urls = []
        suspicious_tld_urls = []

        for u in urls:
            raw_url = u.get("raw_url", "")
            scheme = u.get("scheme", "")
            domain = u.get("domain", "")
            has_ip = u.get("has_ip_host", False)

            # Check 1: IP address used as hostname
            if has_ip:
                ip_urls.append(raw_url)

            # Check 2: Unencrypted HTTP connection
            if scheme == "http":
                http_urls.append(raw_url)

            # Check 3: Known URL Shorteners
            if domain in self.KNOWN_SHORTENERS:
                shortened_urls.append(raw_url)

            # Check 4: High-risk TLDs
            ext = tldextract.extract(domain)
            if ext.suffix in self.SUSPICIOUS_TLDS:
                suspicious_tld_urls.append(raw_url)

        if ip_urls:
            penalty += 15.0
            findings.append(f"Contains {len(ip_urls)} URL(s) using raw IP hosts instead of domain names")
        if http_urls:
            penalty += 10.0
            findings.append(f"Contains {len(http_urls)} unencrypted HTTP link(s)")
        if shortened_urls:
            penalty += 10.0
            findings.append(f"Contains {len(shortened_urls)} URL shortener redirect(s)")
        if suspicious_tld_urls:
            penalty += 10.0
            findings.append(f"Contains {len(suspicious_tld_urls)} link(s) registered under suspicious TLDs")

        triggered = len(findings) > 0
        desc = (
            f"URL risks identified: {'; '.join(findings)}"
            if triggered
            else "No suspicious URL indicators detected in email body."
        )

        return DetectorResult(
            detector_name=self.name,
            score_impact=min(penalty, self.weight),
            triggered=triggered,
            description=desc,
            evidence={
                "ip_urls": ip_urls,
                "http_urls": http_urls,
                "shortened_urls": shortened_urls,
                "suspicious_tld_urls": suspicious_tld_urls,
            },
        )
        