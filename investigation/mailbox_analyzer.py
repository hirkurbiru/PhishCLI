"""
PhishCLI - Mailbox Analyzer

Analyzes Gmail mailboxes and stores investigation results.
Provides live progress, statistics, ETA, and investigation summary.
"""

import os
import time

from gmail.gmail_fetcher import GmailFetcher
from gmail.gmail_parser import GmailParser

from analysis.engine import AnalysisOrchestrator

from database.connection import SessionLocal
from database.repository import ScanRepository

from config.logging_config import logger


# ==========================================================
# UI Configuration
# ==========================================================

BAR_WIDTH = 40


# ==========================================================
# Helper Functions
# ==========================================================

def clear_screen():
    """
    Clear the terminal screen.
    """
    os.system("cls" if os.name == "nt" else "clear")


def format_time(seconds):
    """
    Convert seconds to MM:SS.
    """

    minutes = int(seconds // 60)
    seconds = int(seconds % 60)

    return f"{minutes:02}:{seconds:02}"


def create_progress_bar(current, total):
    """
    Create progress bar.
    """

    if total == 0:
        return "░" * BAR_WIDTH, 0

    progress = int((current / total) * BAR_WIDTH)

    bar = (
        "█" * progress +
        "░" * (BAR_WIDTH - progress)
    )

    percent = round((current / total) * 100, 1)

    return bar, percent


def display_dashboard(
    current,
    total,
    parsed_email,
    statistics,
    failed,
    elapsed,
):
    """
    Display live mailbox investigation dashboard.
    """

    clear_screen()

    bar, percent = create_progress_bar(
        current,
        total,
    )

    print("=" * 70)
    print("               PHISHCLI MAILBOX INVESTIGATION")
    print("=" * 70)

    print(f"\nProgress : [{bar}] {percent:.1f}%")

    print(
        f"Emails   : {current}/{total}"
    )

    print("\nCurrent Email")
    print("-" * 70)

    print(
        f"Subject  : "
        f"{parsed_email.get('subject', 'Unknown')[:60]}"
    )

    print(
        f"Sender   : "
        f"{parsed_email.get('sender', 'Unknown')}"
    )

    print("\nStatistics")
    print("-" * 70)

    print(
        f"Safe         : {statistics['safe']}"
    )

    print(
        f"Suspicious   : {statistics['suspicious']}"
    )

    print(
        f"High Risk    : {statistics['high_risk']}"
    )

    print(
        f"Phishing     : {statistics['phishing']}"
    )

    print(
        f"Failed       : {failed}"
    )

    print("\nPerformance")
    print("-" * 70)

    print(
        f"Elapsed Time : {format_time(elapsed)}"
    )

    if current > 0:

        eta = (
            elapsed / current
        ) * (
            total - current
        )

        print(
            f"ETA          : {format_time(eta)}"
        )

    print("=" * 70)


# ==========================================================
# Mailbox Analysis
# ==========================================================

def analyze_mailbox(email_limit):
    """
    Analyze Gmail mailbox.

    Args:
        email_limit (int):
            Number of emails to analyze.
            -1 = Entire Inbox

    Returns:
        dict
    """

    logger.info(
        "Starting mailbox investigation."
    )

    start_time = time.time()

    fetcher = GmailFetcher()

    parser = GmailParser()

    analyzer = AnalysisOrchestrator()

    # ------------------------------------------------------
    # Fetch Emails
    # ------------------------------------------------------

    if email_limit == -1:

        logger.info(
            "Fetching entire mailbox."
        )

        emails = fetcher.get_email_list(-1)

    else:

        logger.info(
            f"Fetching latest {email_limit} emails."
        )

        emails = fetcher.get_email_list(
            email_limit
        )

    total_emails = len(emails)

    logger.info(
        f"{total_emails} emails fetched."
    )

    if total_emails == 0:

        print("\nNo emails found.")

        return {

            "investigation_id": None,

            "statistics": {

                "total": 0,

                "safe": 0,

                "suspicious": 0,

                "high_risk": 0,

                "phishing": 0,

            },

            "findings": [],

            "failed": 0,

            "elapsed_time": round(
                time.time() - start_time,
                2,
            ),
        }

    db = SessionLocal()

    repository = ScanRepository(db)

    investigation = repository.create_scan_session(
        target_source="GMAIL"
    )

    investigation_id = investigation.id

    findings = []

    failed = 0

    statistics = {
        "total": 0,
        "safe": 0,
        "suspicious": 0,
        "high_risk": 0,
        "phishing": 0,
    }

    try:
        # ======================================================
        # Analyze Emails
        # ======================================================

        for index, email in enumerate(emails, start=1):
            try:
                # --------------------------------------------------
                # Fetch Full Email
                # --------------------------------------------------
                raw_email = fetcher.get_message(email["id"])

                # --------------------------------------------------
                # Parse Email
                # --------------------------------------------------
                parsed_email = parser.parse(raw_email)

                # --------------------------------------------------
                # Analyze Email
                # --------------------------------------------------
                analysis = analyzer.analyze_email(parsed_email)

                # --------------------------------------------------
                # Save Analysis
                # --------------------------------------------------
                repository.save_email_analysis(
                    session_id=investigation_id,
                    email_meta=parsed_email,
                    risk_score=analysis.get("risk_score", 0),
                    classification=analysis.get("classification", "Unknown"),
                    explanation=analysis.get("explanation", ""),
                    findings=analysis.get("detector_results", []),
                    iocs=analysis.get("iocs", []),
                )

                # --------------------------------------------------
                # Store Result
                # --------------------------------------------------
                findings.append({
                    "email": parsed_email,
                    "analysis": analysis,
                })

                # --------------------------------------------------
                # Update Statistics
                # --------------------------------------------------
                statistics["total"] += 1

                classification = (
                    analysis.get("classification", "")
                    .lower()
                    .replace(" ", "_")
                )

                if classification in statistics:
                    statistics[classification] += 1

                # --------------------------------------------------
                # Update Live Dashboard
                # --------------------------------------------------
                elapsed = time.time() - start_time
                display_dashboard(
                    current=index,
                    total=total_emails,
                    parsed_email=parsed_email,
                    statistics=statistics,
                    failed=failed,
                    elapsed=elapsed,
                )
            except Exception as e:
                failed += 1
                logger.exception(
                    f"Failed to analyze email {email.get('id')}: {e}"
                )

                # Show dashboard even after a failure
                elapsed = time.time() - start_time
                display_dashboard(
                    current=index,
                    total=total_emails,
                    parsed_email={
                        "subject": "Analysis Failed",
                        "sender": email.get("sender", "Unknown"),
                    },
                    statistics=statistics,
                    failed=failed,
                    elapsed=elapsed,
                )
                continue
    finally:
        db.close()

    # ======================================================
    # Investigation Complete
    # ======================================================
    elapsed_time = round(time.time() - start_time, 2)

    # ======================================================
    # Investigation Summary
    # ======================================================
    clear_screen()

    processed = statistics["total"]
    safe_pct = (statistics["safe"] / processed) * 100 if processed else 0
    suspicious_pct = (statistics["suspicious"] / processed) * 100 if processed else 0
    high_risk_pct = (statistics["high_risk"] / processed) * 100 if processed else 0
    phishing_pct = (statistics["phishing"] / processed) * 100 if processed else 0
    emails_per_second = processed / elapsed_time if elapsed_time > 0 else 0

    print("=" * 70)
    print("                 INVESTIGATION COMPLETED")
    print("=" * 70)

    print(f"\nInvestigation ID : {investigation_id}")
    print(f"Target Source    : Gmail")
    print(f"Emails Processed : {processed}")
    print(f"Emails Failed    : {failed}")

    print("\nRisk Summary")
    print("-" * 70)

    print(
        f"Safe         : {statistics['safe']} ({safe_pct:.1f}%)"
    )
    print(
        f"Suspicious   : {statistics['suspicious']} ({suspicious_pct:.1f}%)"
    )
    print(
        f"High Risk    : {statistics['high_risk']} ({high_risk_pct:.1f}%)"
    )
    print(
        f"Phishing     : {statistics['phishing']} ({phishing_pct:.1f}%)"
    )

    print("\nPerformance")
    print("-" * 70)

    print(
        f"Elapsed Time      : {format_time(elapsed_time)}"
    )
    print(
        f"Average Speed     : {emails_per_second:.2f} emails/sec"
    )

    print("=" * 70)

    logger.info("Mailbox investigation completed successfully.")
    logger.info(f"Investigation ID={investigation_id}")
    logger.info(f"Processed={processed}")
    logger.info(f"Failed={failed}")
    logger.info(f"Elapsed={elapsed_time:.2f}s")
    logger.info(
        f"Safe={statistics['safe']}, "
        f"Suspicious={statistics['suspicious']}, "
        f"High Risk={statistics['high_risk']}, "
        f"Phishing={statistics['phishing']}"
    )

    return {
        "investigation_id": investigation_id,
        "statistics": statistics,
        "findings": findings,
        "failed": failed,
        "elapsed_time": elapsed_time,
    }