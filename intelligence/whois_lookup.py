"""
PhishCLI - WHOIS Domain Intelligence Analyzer
"""

import datetime
import whois

from typing import Dict

from config.logging_config import logger


class WhoisAnalyzer:

    TRUSTED_DOMAINS = {
        "google.com",
        "gmail.com",
        "microsoft.com",
        "amazon.com",
        "apple.com",
        "paypal.com",
        "outlook.com",
    }

    @classmethod
    def get_domain_info(cls, domain: str) -> Dict:

        domain = domain.lower().strip()

        # Skip WHOIS for trusted domains
        if domain in cls.TRUSTED_DOMAINS:

            return {
                "domain": domain,
                "registrar": "Trusted Domain",
                "creation_date": "Skipped",
                "domain_age_days": None,
                "country": "Unknown",
                "is_new_domain": False,
            }

        try:

            w = whois.whois(domain)

            creation_date = (
                w.get("creation_date")
                if isinstance(w, dict)
                else getattr(w, "creation_date", None)
            )

            if isinstance(creation_date, list):
                creation_date = creation_date[0]

            age = None

            if creation_date:

                if isinstance(creation_date, datetime.datetime):

                    age = (
                        datetime.datetime.now(
                            creation_date.tzinfo
                        )
                        - creation_date
                    ).days

                elif isinstance(
                    creation_date,
                    datetime.date,
                ):

                    age = (
                        datetime.date.today()
                        - creation_date
                    ).days

            registrar = (
                w.get("registrar")
                if isinstance(w, dict)
                else getattr(w, "registrar", None)
            )

            country = (
                w.get("country")
                if isinstance(w, dict)
                else getattr(w, "country", None)
            )

            return {
                "domain": domain,
                "registrar": registrar or "Unknown",
                "creation_date": str(creation_date)
                if creation_date
                else "Unknown",
                "domain_age_days": age,
                "country": country or "Unknown",
                "is_new_domain": (
                    age is not None and age < 30
                ),
            }

        except Exception as e:

            logger.warning(
                f"WHOIS lookup failed for {domain}: {e}"
            )

            return {
                "domain": domain,
                "registrar": "Lookup Failed",
                "creation_date": "Unknown",
                "domain_age_days": None,
                "country": "Unknown",
                "is_new_domain": False,
            }