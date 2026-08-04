"""
PhishCLI - Database ORM Models

Defines the relational tables for scans, email data,
analysis results, detector findings, and IOCs.
"""

import datetime
import uuid
from typing import List, Optional

from sqlalchemy import (
    String,
    Integer,
    Float,
    Text,
    DateTime,
    ForeignKey,
    JSON,
    Boolean,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from database.connection import Base


# ==========================================================
# Scan Session
# ==========================================================

class ScanSession(Base):
    """Represents one investigation session."""

    __tablename__ = "scan_sessions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    session_uuid: Mapped[str] = mapped_column(
        String(36),
        unique=True,
        index=True,
        default=lambda: str(uuid.uuid4()),
    )

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.datetime.now(datetime.UTC),
    )

    total_emails_scanned: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    target_source: Mapped[str] = mapped_column(
        String(50),
        default="GMAIL",
    )

    emails: Mapped[List["EmailRecord"]] = relationship(
        "EmailRecord",
        back_populates="session",
        cascade="all, delete-orphan",
    )


# ==========================================================
# Email Record
# ==========================================================

class EmailRecord(Base):
    """Stores extracted email metadata and content."""

    __tablename__ = "email_records"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    session_id: Mapped[int] = mapped_column(
        ForeignKey("scan_sessions.id"),
    )

    message_id: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
    )

    subject: Mapped[str] = mapped_column(
        Text,
        default="",
    )

    sender: Mapped[str] = mapped_column(
        String(320),
        index=True,
    )

    recipient: Mapped[str] = mapped_column(
        String(320),
        default="",
    )

    reply_to: Mapped[Optional[str]] = mapped_column(
        String(320),
        nullable=True,
    )

    return_path: Mapped[Optional[str]] = mapped_column(
        String(320),
        nullable=True,
    )

    date_sent: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )

    body_text: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    raw_headers: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True,
    )

    scanned_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.datetime.now(datetime.UTC),
    )

    session: Mapped["ScanSession"] = relationship(
        "ScanSession",
        back_populates="emails",
    )

    analysis: Mapped[Optional["AnalysisResult"]] = relationship(
        "AnalysisResult",
        uselist=False,
        back_populates="email",
        cascade="all, delete-orphan",
    )

    findings: Mapped[List["DetectorFinding"]] = relationship(
        "DetectorFinding",
        back_populates="email",
        cascade="all, delete-orphan",
    )

    iocs: Mapped[List["IOCRecord"]] = relationship(
        "IOCRecord",
        back_populates="email",
        cascade="all, delete-orphan",
    )


# ==========================================================
# Analysis Result
# ==========================================================

class AnalysisResult(Base):
    """Stores risk engine output."""

    __tablename__ = "analysis_results"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    email_id: Mapped[int] = mapped_column(
        ForeignKey("email_records.id"),
        unique=True,
    )

    risk_score: Mapped[float] = mapped_column(
        Float,
        index=True,
    )

    classification: Mapped[str] = mapped_column(
        String(50),
        index=True,
    )

    explanation_summary: Mapped[str] = mapped_column(
        Text,
    )

    analyzed_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.datetime.now(datetime.UTC),
    )

    email: Mapped["EmailRecord"] = relationship(
        "EmailRecord",
        back_populates="analysis",
    )


# ==========================================================
# Detector Findings
# ==========================================================

class DetectorFinding(Base):
    """Stores individual detector outputs."""

    __tablename__ = "detector_findings"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    email_id: Mapped[int] = mapped_column(
        ForeignKey("email_records.id"),
    )

    detector_name: Mapped[str] = mapped_column(
        String(100),
        index=True,
    )

    score_impact: Mapped[float] = mapped_column(
        Float,
    )

    triggered: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
    )

    evidence: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True,
    )

    email: Mapped["EmailRecord"] = relationship(
        "EmailRecord",
        back_populates="findings",
    )


# ==========================================================
# IOC Records
# ==========================================================

class IOCRecord(Base):
    """Stores extracted Indicators of Compromise."""

    __tablename__ = "ioc_records"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    email_id: Mapped[int] = mapped_column(
        ForeignKey("email_records.id"),
    )

    ioc_type: Mapped[str] = mapped_column(
        String(50),
        index=True,
    )

    ioc_value: Mapped[str] = mapped_column(
        Text,
        index=True,
    )

    reputation_score: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
    )

    enrichment_data: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True,
    )

    email: Mapped["EmailRecord"] = relationship(
        "EmailRecord",
        back_populates="iocs",
    )