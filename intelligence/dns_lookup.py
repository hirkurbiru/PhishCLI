"""
PhishCLI - DNS Resolution Analyzer
Resolves DNS records (A, MX, TXT) for target domains.
"""

import dns.resolver
from typing import Dict, List
from config.logging_config import logger


class DNSResolver:
    """Resolves DNS infrastructure details for domain validation."""

    @staticmethod
    def resolve_records(domain: str) -> Dict[str, List[str]]:
        """Resolves A, MX, and TXT DNS records for a given domain."""

        records = {
            "A": [],
            "MX": [],
            "TXT": []
        }

        resolver = dns.resolver.Resolver(configure=False)

        # Use Google's public DNS servers
        resolver.nameservers = [
            "8.8.8.8",
            "8.8.4.4"
        ]

        resolver.timeout = 5
        resolver.lifetime = 10

        for rtype in ["A", "MX", "TXT"]:
            try:
                answers = resolver.resolve(domain, rtype)
                records[rtype] = [answer.to_text() for answer in answers]

            except Exception as e:
                logger.warning(f"{rtype} lookup failed for {domain}: {e}")
                records[rtype] = []

        return records