"""
PhishCLI - Database Repository Layer

Provides high-level database operations for scan sessions,
email analysis, detector findings, IOC storage, history,
and dashboard statistics.
"""

from typing import Any, Dict, List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from config.logging_config import logger
from database.models import (
    AnalysisResult,
    DetectorFinding,
    EmailRecord,
    IOCRecord,
    ScanSession,
)
from utils.exceptions import DatabaseError


class ScanRepository:
    """Repository for scan sessions and investigation history."""

    def __init__(self, session: Session):
        self.db = session

    # ==========================================================
    # Scan Session
    # ==========================================================

    def create_scan_session(self, target_source: str = "GMAIL") -> ScanSession:
        """
        Creates a new scan session.
        """

        try:

            scan_session = ScanSession(
                target_source=target_source,
                total_emails_scanned=0,
            )

            self.db.add(scan_session)

            self.db.commit()

            self.db.refresh(scan_session)

            return scan_session

        except Exception as e:

            self.db.rollback()

            logger.error(f"Failed to create scan session: {e}")

            raise DatabaseError(
                "Failed to create scan session.",
                details=str(e),
            )

    # ==========================================================
    # Save Analysis
    # ==========================================================

    def save_email_analysis(
        self,
        session_id: int,
        email_meta: Dict[str, Any],
        risk_score: float,
        classification: str,
        explanation: str,
        findings: List[Dict[str, Any]],
        iocs: List[Dict[str, Any]],
    ) -> EmailRecord:
        """
        Saves a complete email investigation.
        """

        try:

            # --------------------------------------------------
            # Prevent duplicate Gmail messages
            # --------------------------------------------------

            message_id = email_meta.get("message_id")

            if message_id:

                existing = (
                    self.db.query(EmailRecord)
                    .filter(
                        EmailRecord.message_id == message_id
                    )
                    .first()
                )

                if existing:
                    logger.info("Email already exists in database.")
                    return existing

            # --------------------------------------------------
            # Email Record
            # --------------------------------------------------

            email = EmailRecord(
                session_id=session_id,
                message_id=email_meta.get("message_id", ""),
                subject=email_meta.get("subject", ""),
                sender=email_meta.get("sender", ""),
                recipient=email_meta.get("recipient", ""),
                reply_to=email_meta.get("reply_to"),
                return_path=email_meta.get("return_path"),
                date_sent=email_meta.get("date", ""),
                body_text=email_meta.get("body", ""),
                raw_headers=email_meta.get("headers", {}),
            )

            self.db.add(email)

            self.db.flush()

            # --------------------------------------------------
            # Analysis Result
            # --------------------------------------------------

            analysis = AnalysisResult(
                email_id=email.id,
                risk_score=risk_score,
                classification=classification,
                explanation_summary=explanation,
            )

            self.db.add(analysis)

            # --------------------------------------------------
            # Detector Findings
            # --------------------------------------------------

            def _get_finding_value(item, key, default=None):
                if isinstance(item, dict):
                    return item.get(key, default)
                return getattr(item, key, default)

            for finding in findings:

                finding_record = DetectorFinding(
                    email_id=email.id,
                    detector_name=_get_finding_value(
                        finding,
                        "detector_name",
                        "Unknown",
                    ),
                    score_impact=_get_finding_value(
                        finding,
                        "score_impact",
                        0.0,
                    ),
                    triggered=_get_finding_value(
                        finding,
                        "triggered",
                        False,
                    ),
                    description=_get_finding_value(
                        finding,
                        "description",
                        "",
                    ),
                    evidence=_get_finding_value(
                        finding,
                        "evidence",
                        {},
                    ),
                )

                self.db.add(finding_record)

            # --------------------------------------------------
            # IOC Records
            # --------------------------------------------------

            for ioc in iocs:

                ioc_record = IOCRecord(
                    email_id=email.id,
                    ioc_type=ioc.get("type", "UNKNOWN"),
                    ioc_value=ioc.get("value", ""),
                    reputation_score=ioc.get("reputation_score"),
                    enrichment_data=ioc.get("enrichment_data", {}),
                )

                self.db.add(ioc_record)

            # --------------------------------------------------
            # Update Scan Counter
            # --------------------------------------------------

            session_obj = self.db.get(ScanSession, session_id)

            if session_obj:

                session_obj.total_emails_scanned += 1

            self.db.commit()

            self.db.refresh(email)

            logger.info(
                f"Saved email investigation: {email.subject}"
            )

            return email

        except Exception as e:

            self.db.rollback()

            logger.error(f"Failed to save email analysis: {e}")

            raise DatabaseError(
                "Failed to save email analysis.",
                details=str(e),
            )

    # ==========================================================
    # Query Methods
    # ==========================================================

    def get_email_by_id(
        self,
        email_id: int,
    ) -> Optional[EmailRecord]:
        """
        Returns a single email record.
        """

        return self.db.get(EmailRecord, email_id)

    def get_scan_history(self):
        """
        Returns all investigations.
        """

        return (
            self.db.query(
                EmailRecord,
                AnalysisResult,
            )
            .join(AnalysisResult)
            .order_by(
                EmailRecord.scanned_at.desc()
            )
            .all()
        )

    def get_emails_by_classification(
        self,
        classification: str,
    ) -> List[EmailRecord]:
        """
        Returns emails filtered by classification.
        """

        return (
            self.db.query(EmailRecord)
            .join(AnalysisResult)
            .filter(
                AnalysisResult.classification == classification
            )
            .all()
        )

    def search_history(
        self,
        keyword: str,
    ) -> List[EmailRecord]:
        """
        Search history by sender or subject.
        """

        return (
            self.db.query(EmailRecord)
            .filter(
                EmailRecord.subject.ilike(f"%{keyword}%")
                |
                EmailRecord.sender.ilike(f"%{keyword}%")
            )
            .all()
        )

    # ==========================================================
    # Dashboard
    # ==========================================================

    def get_mailbox_summary(self) -> Dict[str, Any]:
        """
        Returns dashboard statistics.
        """

        return {
            "total_sessions": self.db.query(ScanSession).count(),
            "total_emails": self.db.query(EmailRecord).count(),
            "safe": self.db.query(AnalysisResult)
            .filter(
                AnalysisResult.classification == "Safe"
            )
            .count(),
            "suspicious": self.db.query(AnalysisResult)
            .filter(
                AnalysisResult.classification == "Suspicious"
            )
            .count(),
            "high_risk": self.db.query(AnalysisResult)
            .filter(
                AnalysisResult.classification == "High Risk"
            )
            .count(),
            "phishing": self.db.query(AnalysisResult)
            .filter(
                AnalysisResult.classification == "Phishing"
            )
            .count(),
        }

    # ==========================================================
    # Delete
    # ==========================================================

    def delete_email(
        self,
        email_id: int,
    ) -> bool:
        """
        Deletes an investigation.
        """

        try:

            email = self.db.get(
                EmailRecord,
                email_id,
            )

            if email is None:
                return False

            self.db.delete(email)

            self.db.commit()

            logger.info(
                f"Deleted email investigation {email_id}"
            )

            return True

        except Exception as e:

            self.db.rollback()

            logger.error(
                f"Failed to delete investigation: {e}"
            )

            raise DatabaseError(
                "Failed to delete investigation.",
                details=str(e),
            )
            
            
    # ==========================================================
    # Dashboard Statistics
    # ==========================================================

    def get_top_senders(self, limit: int = 5):
        """
        Returns the most common email senders.
        """

        return (
            self.db.query(
                EmailRecord.sender,
                func.count(EmailRecord.id).label("count"),
            )
            .filter(
                EmailRecord.sender.isnot(None),
                EmailRecord.sender != "",
            )
            .group_by(EmailRecord.sender)
            .order_by(func.count(EmailRecord.id).desc())
            .limit(limit)
            .all()
        )

    def get_recent_scans(self, limit: int = 5):
        """
        Returns the most recently scanned investigations.
        """

        return (
            self.db.query(
                EmailRecord,
                AnalysisResult,
            )
            .join(AnalysisResult)
            .order_by(
                EmailRecord.scanned_at.desc()
            )
            .limit(limit)
            .all()
        )

    def get_classification_statistics(self):
        """
        Returns investigation counts grouped by classification.
        """

        return (
            self.db.query(
                AnalysisResult.classification,
                func.count(AnalysisResult.id).label("count"),
            )
            .group_by(
                AnalysisResult.classification
            )
            .all()
        )

    # ==========================================================
    # IOC Explorer
    # ==========================================================

    def get_iocs_by_type(self, ioc_type: str):
        """
        Returns all IOCs of a given type.
        """

        return (
            self.db.query(IOCRecord)
            .filter(
                IOCRecord.ioc_type == ioc_type
            )
            .order_by(
                IOCRecord.id.desc()
            )
            .all()
        )

    def get_top_iocs(
        self,
        ioc_type: str,
        limit: int = 20,
    ):
        """
        Returns the most common IOCs.
        """

        return (
            self.db.query(
                IOCRecord.ioc_value,
                func.count(
                    IOCRecord.id
                ).label("count"),
            )
            .filter(
                IOCRecord.ioc_type == ioc_type
            )
            .group_by(
                IOCRecord.ioc_value
            )
            .order_by(
                func.count(
                    IOCRecord.id
                ).desc()
            )
            .limit(limit)
            .all()
        )

    def search_by_sender(self, sender: str):
        """
        Search emails by sender.
        """

        return (
            self.db.query(
                EmailRecord,
                AnalysisResult,
            )
            .join(AnalysisResult)
            .filter(
                EmailRecord.sender.ilike(
                    f"%{sender}%"
                )
            )
            .all()
        )

    def search_by_subject(self, subject: str):
        """
        Search emails by subject.
        """

        return (
            self.db.query(
                EmailRecord,
                AnalysisResult,
            )
            .join(AnalysisResult)
            .filter(
                EmailRecord.subject.ilike(
                    f"%{subject}%"
                )
            )
            .all()
        )

    def search_by_message_id(self, message_id: str):
        """
        Search by Gmail Message-ID.
        """

        return (
            self.db.query(
                EmailRecord,
                AnalysisResult,
            )
            .join(AnalysisResult)
            .filter(
                EmailRecord.message_id.ilike(
                    f"%{message_id}%"
                )
            )
            .all()
        )

    def search_ioc(self, keyword: str):
        """
        Search IOC records.
        """

        return (
            self.db.query(IOCRecord)
            .filter(
                IOCRecord.ioc_value.ilike(
                    f"%{keyword}%"
                )
            )
            .all()
        )

    def global_search(
        self,
        keyword: str,
    ):
        """
        Search sender, subject and message id.
        """

        return (
            self.db.query(
                EmailRecord,
                AnalysisResult,
            )
            .join(AnalysisResult)
            .filter(
                EmailRecord.sender.ilike(f"%{keyword}%")
                |
                EmailRecord.subject.ilike(f"%{keyword}%")
                |
                EmailRecord.message_id.ilike(f"%{keyword}%")
            )
            .all()
        )



