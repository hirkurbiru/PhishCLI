"""
PhishCLI - AbuseIPDB Intelligence Connector (v2 API)
Queries AbuseIPDB to retrieve IP address abuse confidence scores and reports.
"""

import requests
from typing import Dict, Any, Optional
from config.settings import settings
from config.logging_config import logger


class AbuseIPDBClient:
    """Interacts with the AbuseIPDB v2 REST API."""

    BASE_URL = "https://api.abuseipdb.com/api/v2/check"

    def __init__(self):
        self.api_key: str = settings.ABUSEIPDB_API_KEY or ""
        self.enabled = bool(self.api_key)

        if not self.enabled:
            logger.info(
                "AbuseIPDB API key not configured. IP reputation bypassed."
            )

    def check_ip(self, ip_address: str) -> Optional[Dict[str, Any]]:
        """Queries AbuseIPDB for an IP abuse confidence rating."""

        if not self.enabled:
            return None

        headers = {
            "Key": self.api_key,
            "Accept": "application/json",
        }

        params = {
            "ipAddress": ip_address,
            "maxAgeInDays": "90",
        }

        try:
            response = requests.get(
                self.BASE_URL,
                headers=headers,
                params=params,
                timeout=settings.HTTP_TIMEOUT_SECONDS,
            )

            if response.status_code == 200:
                data = response.json().get("data", {})

                return {
                    "ip_address": data.get("ipAddress"),
                    "abuse_confidence_score": data.get(
                        "abuseConfidenceScore", 0
                    ),
                    "country": data.get("countryCode"),
                    "total_reports": data.get("totalReports", 0),
                    "is_public": data.get("isPublic", True),
                    "engine_source": "AbuseIPDB",
                }

            elif response.status_code == 404:
                return {
                    "ip_address": ip_address,
                    "abuse_confidence_score": 0,
                    "country": None,
                    "total_reports": 0,
                    "is_public": True,
                    "status": "Not Found",
                    "engine_source": "AbuseIPDB",
                }

            else:
                logger.warning(
                    f"AbuseIPDB returned status code {response.status_code}"
                )

                return {
                    "ip_address": ip_address,
                    "abuse_confidence_score": 0,
                    "country": None,
                    "total_reports": 0,
                    "is_public": True,
                    "status": f"HTTP {response.status_code}",
                    "engine_source": "AbuseIPDB",
                }

        except Exception as e:
            logger.error(f"AbuseIPDB API error: {e}")

        return None