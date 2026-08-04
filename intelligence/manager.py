"""
PhishCLI - Threat Intelligence Manager

Coordinates WHOIS, DNS, VirusTotal and AbuseIPDB lookups.
Provides in-memory caching to improve performance.
"""

from intelligence.whois_lookup import WhoisAnalyzer
from intelligence.dns_lookup import DNSResolver
from intelligence.virustotal import VirusTotalClient
from intelligence.abuseipdb import AbuseIPDBClient


class IntelligenceManager:
    """
    Coordinates all threat intelligence services.
    """

    def __init__(self):

        self.whois = WhoisAnalyzer()
        self.dns = DNSResolver()
        self.virustotal = VirusTotalClient()
        self.abuseipdb = AbuseIPDBClient()

        # --------------------------------------------
        # Runtime Cache
        # --------------------------------------------

        self._domain_cache = {}
        self._url_cache = {}
        self._ip_cache = {}

    # ==================================================
    # Domain Intelligence
    # ==================================================

    def analyze_domain(self, domain: str) -> dict:
        """
        Run all available domain intelligence.

        Cached to avoid duplicate network requests.
        """

        if not domain:
            return {}

        domain = domain.lower().strip()

        if domain in self._domain_cache:
            return self._domain_cache[domain]

        results = {}

        try:

            results["whois"] = self.whois.get_domain_info(domain)

            results["dns"] = self.dns.resolve_records(domain)

            results["virustotal"] = (
                self.virustotal.lookup_domain(domain)
            )

        except Exception:

            results = {}

        self._domain_cache[domain] = results

        return results

    # ==================================================
    # URL Intelligence
    # ==================================================

    def analyze_url(self, url: str) -> dict:
        """
        Run URL reputation lookup.

        Cached to avoid duplicate requests.
        """

        if not url:
            return {}

        if url in self._url_cache:
            return self._url_cache[url]

        results = {}

        try:

            results["virustotal"] = (
                self.virustotal.lookup_url(url)
            )

        except Exception:

            results = {}

        self._url_cache[url] = results

        return results

    # ==================================================
    # IP Intelligence
    # ==================================================

    def analyze_ip(self, ip: str) -> dict:
        """
        Run AbuseIPDB lookup.

        Cached to avoid duplicate requests.
        """

        if not ip:
            return {}

        if ip in self._ip_cache:
            return self._ip_cache[ip]

        results = {}

        try:

            results["abuseipdb"] = (
                self.abuseipdb.check_ip(ip)
            )

        except Exception:

            results = {}

        self._ip_cache[ip] = results

        return results

    # ==================================================
    # Cache Management
    # ==================================================

    def clear_cache(self):
        """
        Clears all runtime caches.
        """

        self._domain_cache.clear()
        self._url_cache.clear()
        self._ip_cache.clear()