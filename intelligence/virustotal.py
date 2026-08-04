"""
PhishCLI - VirusTotal Intelligence Connector (v3 API)
Queries VirusTotal for file hashes, URLs, and domain reputations.
"""

import requests
from typing import Dict, Any, Optional
from config.settings import settings
from config.logging_config import logger


class VirusTotalClient:
    """Interacts with the VirusTotal v3 REST API."""

    BASE_URL = "https://www.virustotal.com/api/v3"

    def __init__(self):
        self.api_key: str = settings.VIRUSTOTAL_API_KEY or ""
        self.enabled = bool(self.api_key)

        if not self.enabled:
            logger.info(
                "VirusTotal API key not configured. OSINT enrichment bypassed."
            )

    def check_hash(self, file_hash: str) -> Optional[Dict[str, Any]]:
        """Queries VirusTotal for file hash analysis statistics."""

        if not self.enabled:
            return None

        headers = {"x-apikey": self.api_key}

        try:
            response = requests.get(
                f"{self.BASE_URL}/files/{file_hash}",
                headers=headers,
                timeout=settings.HTTP_TIMEOUT_SECONDS,
            )

            if response.status_code == 200:
                attributes = response.json()["data"]["attributes"]
                stats = attributes.get("last_analysis_stats", {})

                return {
                    "malicious": stats.get("malicious", 0),
                    "suspicious": stats.get("suspicious", 0),
                    "harmless": stats.get("harmless", 0),
                    "undetected": stats.get("undetected", 0),
                    "engine_source": "VirusTotal",
                }

            elif response.status_code == 404:
                return {
                    "malicious": 0,
                    "suspicious": 0,
                    "harmless": 0,
                    "undetected": 0,
                    "reputation": 0,
                    "status": "Not Found on VirusTotal",
                    "engine_source": "VirusTotal",
                }

            logger.warning(
                f"VirusTotal hash lookup returned {response.status_code}"
            )

        except Exception as e:
            logger.error(f"VirusTotal hash lookup failed: {e}")

        return None

    def lookup_domain(self, domain: str) -> Optional[Dict[str, Any]]:
        """Queries VirusTotal for a domain reputation."""

        if not self.enabled:
            return None

        headers = {"x-apikey": self.api_key}

        try:
            response = requests.get(
                f"{self.BASE_URL}/domains/{domain}",
                headers=headers,
                timeout=settings.HTTP_TIMEOUT_SECONDS,
            )

            if response.status_code == 200:
                attributes = response.json()["data"]["attributes"]
                stats = attributes.get("last_analysis_stats", {})

                return {
                    "domain": domain,
                    "malicious": stats.get("malicious", 0),
                    "suspicious": stats.get("suspicious", 0),
                    "harmless": stats.get("harmless", 0),
                    "undetected": stats.get("undetected", 0),
                    "reputation": attributes.get("reputation", 0),
                    "engine_source": "VirusTotal",
                }

            elif response.status_code == 404:
                return {
    "domain": domain,
    "malicious": 0,
    "suspicious": 0,
    "harmless": 0,
    "undetected": 0,
    "reputation": 0,
    "status": "Not Found on VirusTotal",
    "engine_source": "VirusTotal",
}

            logger.warning(
                f"VirusTotal domain lookup returned {response.status_code}"
            )

        except Exception as e:
            logger.error(f"VirusTotal domain lookup failed: {e}")

        return None

    def lookup_url(self, url: str) -> Optional[Dict[str, Any]]:
        """Queries VirusTotal for URL reputation."""

        if not self.enabled:
            return None

        import base64

        headers = {"x-apikey": self.api_key}

        # VirusTotal requires the URL to be URL-safe Base64 encoded
        url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")

        try:
            response = requests.get(
                f"{self.BASE_URL}/urls/{url_id}",
                headers=headers,
                timeout=settings.HTTP_TIMEOUT_SECONDS,
            )

            if response.status_code == 200:
                attributes = response.json()["data"]["attributes"]
                stats = attributes.get("last_analysis_stats", {})

                return {
                    "url": url,
                    "malicious": stats.get("malicious", 0),
                    "suspicious": stats.get("suspicious", 0),
                    "harmless": stats.get("harmless", 0),
                    "undetected": stats.get("undetected", 0),
                    "reputation": attributes.get("reputation", 0),
                    "engine_source": "VirusTotal",
                }

            elif response.status_code == 404:
                return {
                    "url": url,
                    "malicious": 0,
                    "suspicious": 0,
                    "harmless": 0,
                    "undetected": 0,
                    "reputation": 0,
                    "status": "Not Found on VirusTotal",
                    "engine_source": "VirusTotal",
                }

            logger.warning(
                f"VirusTotal URL lookup returned {response.status_code}"
            )

        except Exception as e:
            logger.error(f"VirusTotal URL lookup failed: {e}")

        return None