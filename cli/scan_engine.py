"""
PhishCLI - Scan Engine

Handles bulk mailbox scanning and investigation storage.
"""

from gmail.gmail_fetcher import GmailFetcher
from gmail.gmail_parser import GmailParser

from analysis.engine import AnalysisOrchestrator

from database.connection import SessionLocal
from database.repository import ScanRepository


class ScanEngine:
    """
    Core mailbox scanning engine.
    """

    def __init__(self):

        self.fetcher = GmailFetcher()
        self.parser = GmailParser()
        self.analyzer = AnalysisOrchestrator()

    def scan(self, email_limit=10):
        """
        Scan Gmail mailbox.

        Returns:
            dict
        """

        emails = self.fetcher.get_email_list(email_limit)

        db = SessionLocal()

        repository = ScanRepository(db)

        session = repository.create_scan_session(
            target_source="GMAIL"
        )

        statistics = {
            "total": 0,
            "safe": 0,
            "suspicious": 0,
            "high_risk": 0,
            "phishing": 0,
        }

        for email in emails:

            raw_email = self.fetcher.get_message(
                email["id"]
            )

            parsed = self.parser.parse(raw_email)

            result = self.analyzer.analyze_email(
                parsed
            )

            repository.save_email_analysis(
                session_id=session.id,
                email_meta=parsed,
                risk_score=result.get(
                    "risk_score",
                    0,
                ),
                classification=result.get(
                    "classification",
                    "Unknown",
                ),
                explanation=result.get(
                    "explanation",
                    "",
                ),
                findings=result.get(
                    "detector_results",
                    [],
                ),
                iocs=result.get(
                    "iocs",
                    [],
                ),
            )

            statistics["total"] += 1

            classification = result.get(
                "classification",
                "",
            ).lower()

            if classification == "safe":

                statistics["safe"] += 1

            elif classification == "suspicious":

                statistics["suspicious"] += 1

            elif classification == "high risk":

                statistics["high_risk"] += 1

            elif classification == "phishing":

                statistics["phishing"] += 1

        db.close()

        return statistics