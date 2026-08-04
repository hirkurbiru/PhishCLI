"""
PhishCLI - Primary Scan Analysis Orchestrator
Coordinates ingestion, detector pipeline execution, threat intel lookups, and score calculations.
"""

from typing import Dict, Any, List
from analysis.detectors.auth_detector import AuthDetector
from analysis.detectors.sender_detector import SenderDetector
from analysis.detectors.url_detector import URLDetector
from analysis.detectors.attachment_detector import AttachmentDetector
from analysis.detectors.keyword_detector import KeywordDetector
from analysis.scoring import RiskEngine
from analysis.explainer import ExplanationEngine
from config.logging_config import logger
from intelligence.manager import IntelligenceManager


class AnalysisOrchestrator:
    """Orchestrates the entire execution flow for a single email scan."""

    def __init__(self):
        # Register independent detectors
        self.detectors = [
            AuthDetector(),
            SenderDetector(),
            URLDetector(),
            AttachmentDetector(),
            KeywordDetector(),
        ]
        # Register OSINT clients
        # Threat Intelligence Manager
        self.intelligence = IntelligenceManager()
        
    def analyze(self, parsed_email: Dict[str, Any]) -> Dict[str, Any]:
        """
         Public entry point for email analysis.
        """
        return self.analyze_email(parsed_email)

    def analyze_email(self, parsed_email: Dict[str, Any]) -> Dict[str, Any]:
        """Runs all detectors, enriches with OSINT, and calculates composite risk."""
        logger.info(f"Analyzing email ID: {parsed_email.get('message_id', 'UNKNOWN')}")

        # 1. Execute Detector Pipeline
        detector_results: List = []
        for detector in self.detectors:
            try:
                res = detector.analyze(parsed_email)
                detector_results.append(res)
            except Exception as e:
                logger.error(f"Detector {detector.name} failed: {e}")

        # 2. Execute Threat Intelligence Enrichments
        osint_data: Dict[str, Any] = {}

        sender = parsed_email.get("sender", "")
        domain = sender.split("@")[-1].rstrip(">") if "@" in sender else ""

        # Domain Intelligence (WHOIS + DNS + VirusTotal)
        if domain:
            domain_intel = self.intelligence.analyze_domain(domain)
            osint_data.update(domain_intel)

            whois_data = domain_intel.get("whois", {})
            osint_data["is_new_domain"] = whois_data.get("is_new_domain", False)

        # URL Intelligence (VirusTotal)
        urls = parsed_email.get("urls", [])
        if urls:
            first_url = urls[0].get("raw_url")
            if first_url:
                osint_data["url_intelligence"] = self.intelligence.analyze_url(first_url)

        # Attachment Hash Intelligence (VirusTotal)
        attachments = parsed_email.get("attachments", [])
        if attachments:
            first_hash = attachments[0].get("sha256")
            if first_hash:
                vt_result = self.intelligence.virustotal.check_hash(first_hash)
                if vt_result:
                    osint_data["attachment_virustotal"] = vt_result

        # 3. Calculate Risk & Classification
        risk_score, classification = RiskEngine.calculate_risk(
            detector_results, osint_data
        )

        # 4. Generate Explanation Summary
        explanation = ExplanationEngine.generate_explanation(
            detector_results, osint_data, classification
        )

        # 5. Extract IOCs for Database Persistence
        iocs = self._extract_iocs(parsed_email)

        return {
            "email_data": parsed_email,
            "risk_score": risk_score,
            "classification": classification,
            "explanation": explanation,
            "detector_results": detector_results,
            "osint_data": osint_data,
            "iocs": iocs,
        }
    @staticmethod
    def _extract_iocs(parsed_email: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Collect Indicators of Compromise (IOCs) from parsed email."""
        iocs = []

        # Sender
        sender = parsed_email.get("sender")
        if sender:
            iocs.append({"type": "EMAIL_ADDRESS", "value": sender})

            if "@" in sender:
                domain = sender.split("@")[-1].rstrip(">")
                iocs.append({"type": "DOMAIN", "value": domain})

        # Reply-To
        reply_to = parsed_email.get("reply_to")
        if reply_to:
            iocs.append({"type": "REPLY_TO", "value": reply_to})

        # Return-Path
        return_path = parsed_email.get("return_path")
        if return_path:
            iocs.append({"type": "RETURN_PATH", "value": return_path})

        # URLs
        for url in parsed_email.get("urls", []):
            raw_url = url.get("raw_url")

            if raw_url:
                iocs.append({"type": "URL", "value": raw_url})

            domain = url.get("domain")
            if domain:
                iocs.append({"type": "DOMAIN", "value": domain})

            if url.get("has_ip_host"):
                iocs.append({"type": "IP_ADDRESS", "value": domain})

        # Attachments
        for att in parsed_email.get("attachments", []):
            filename = att.get("filename")
            if filename:
                iocs.append({"type": "ATTACHMENT", "value": filename})

            sha256 = att.get("sha256")
            if sha256:
                iocs.append({"type": "SHA256", "value": sha256})

            md5 = att.get("md5")
            if md5:
                iocs.append({"type": "MD5", "value": md5})

        # Message-ID
        message_id = parsed_email.get("message_id")
        if message_id:
            iocs.append({"type": "MESSAGE_ID", "value": message_id})

        return iocs