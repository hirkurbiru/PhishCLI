"""
PhishCLI - Rich Terminal Visualizer

Formats PhishCLI scan reports into a professional Rich terminal UI.
"""

from typing import Any, Dict, List

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


class TerminalReporter:
    """Render scan results in a Rich terminal interface."""

    def __init__(self):
        self.console = Console()

    def print_scan_results(self, scan_data: Dict[str, Any]) -> None:
        """Main entry point for rendering a scan."""

        email = scan_data.get("email_data", {})

        score = scan_data.get("risk_score", 0.0)
        classification = scan_data.get("classification", "Safe")
        explanation = scan_data.get(
            "explanation",
            "No explanation available.",
        )

        color = self._classification_color(classification)

        self.console.print()

        self.console.print(
            Panel(
                Text(
                    f"PhishCLI Analysis Report - {classification.upper()}",
                    style=f"bold white on {color}",
                ),
                expand=True,
            )
        )

        self._print_metadata(
            email,
            score,
            classification,
            color,
        )

        self._print_authentication(email)
        self._print_urls(email)
        self._print_attachments(email)
        self._print_detector_results(scan_data)
        self._print_iocs(scan_data)

        self.console.print(
            Panel(
                explanation,
                title="Threat Explanation",
                border_style=color,
            )
        )

        self.console.print()

    def _classification_color(
        self,
        classification: str,
    ) -> str:

        mapping = {
            "Safe": "green",
            "Suspicious": "yellow",
            "High Risk": "bright_red",
            "Phishing": "red",
        }

        return mapping.get(classification, "cyan")

    def _print_metadata(
        self,
        email: Dict[str, Any],
        score: float,
        classification: str,
        color: str,
    ):

        table = Table(
            title="Email Metadata",
            show_header=False,
            expand=True,
        )

        table.add_column(
            "Field",
            style="bold cyan",
            width=18,
        )

        table.add_column("Value")

        table.add_row(
            "Subject",
            str(email.get("subject", "N/A")),
        )

        table.add_row(
            "From",
            str(email.get("sender", "N/A")),
        )

        table.add_row(
            "To",
            str(email.get("recipient", "N/A")),
        )

        table.add_row(
            "Reply-To",
            str(email.get("reply_to", "N/A")),
        )

        table.add_row(
            "Return-Path",
            str(email.get("return_path", "N/A")),
        )

        table.add_row(
            "Date",
            str(email.get("date_sent", "N/A")),
        )

        table.add_row(
            "Message-ID",
            str(email.get("message_id", "N/A")),
        )

        table.add_row(
            "Risk Score",
            f"[{color}]{score:.1f}/100[/{color}]",
        )

        table.add_row(
            "Classification",
            f"[{color}]{classification}[/{color}]",
        )

        self.console.print(table)

    def _print_authentication(
        self,
        email: Dict[str, Any],
    ):

        auth = email.get("auth_results", {})

        if not auth:
            return

        table = Table(
            title="Authentication Results",
            expand=True,
        )

        table.add_column(
            "Protocol",
            style="cyan",
        )

        table.add_column("Status")

        table.add_row(
            "SPF",
            auth.get("spf", "Unknown"),
        )

        table.add_row(
            "DKIM",
            auth.get("dkim", "Unknown"),
        )

        table.add_row(
            "DMARC",
            auth.get("dmarc", "Unknown"),
        )

        self.console.print(table)

    def _print_urls(
        self,
        email: Dict[str, Any],
    ):

        urls = email.get("urls", [])

        if not urls:
            return

        table = Table(
            title="Extracted URLs",
            expand=True,
        )

        table.add_column(
            "Domain",
            style="yellow",
        )

        table.add_column("URL")

        for url in urls:

            table.add_row(
                str(url.get("domain", "")),
                str(url.get("raw_url", "")),
            )

        self.console.print(table)

    def _print_attachments(
        self,
        email: Dict[str, Any],
    ):

        attachments = email.get(
            "attachments",
            [],
        )

        if not attachments:
            return

        table = Table(
            title="Attachments",
            expand=True,
        )

        table.add_column("Filename")
        table.add_column("Type")
        table.add_column("Size")

        for attachment in attachments:

            table.add_row(
                str(
                    attachment.get(
                        "filename",
                        "",
                    )
                ),
                str(
                    attachment.get(
                        "content_type",
                        "",
                    )
                ),
                f'{attachment.get("size_bytes",0)} bytes',
            )

        self.console.print(table)
        
    def _print_detector_results(
        self,
        scan_data: Dict[str, Any],
    ):

        findings = scan_data.get(
            "detector_results",
            [],
        )

        if not findings:
            return

        table = Table(
            title="Detector Findings",
            expand=True,
        )

        table.add_column(
            "Detector",
            style="bold cyan",
        )

        table.add_column("Severity")
        table.add_column("Finding")
        table.add_column("Score")

        for finding in findings:

            if isinstance(finding, dict):

                detector = (
                    finding.get("detector")
                    or finding.get("name")
                    or "Unknown"
                )

                severity = (
                    finding.get("severity")
                    or finding.get("risk")
                    or "N/A"
                )

                message = (
                    finding.get("message")
                    or finding.get("description")
                    or finding.get("reason")
                    or ""
                )

                score = (
                    finding.get("score")
                    or finding.get("risk_score")
                    or ""
                )

            else:

                detector = (
                     getattr(finding, "detector_name", None)
                     or getattr(finding, "detector", None)
                     or getattr(finding, "name", None)
                     or finding.__class__.__name__
                )

                severity = (
                    getattr(finding, "severity", None)
                    or getattr(finding, "risk", None)
                    or "N/A"
                )

                message = (
                    getattr(finding, "message", None)
                    or getattr(finding, "description", None)
                    or getattr(finding, "reason", None)
                    or str(finding)
                )

                score = (
                    getattr(finding, "score_impact", None)
                    or getattr(finding, "score", None)
                    or getattr(finding, "risk_score", None)
                    or ""
                )

            table.add_row(
                str(detector),
                str(severity),
                str(message),
                str(score),
            )

        self.console.print(table)

    def _print_iocs(
        self,
        scan_data: Dict[str, Any],
    ):

        iocs: List[Dict[str, Any]] = scan_data.get(
            "iocs",
            [],
        )

        if not iocs:
            return

        table = Table(
            title="Indicators of Compromise (IOCs)",
            expand=True,
        )

        table.add_column(
            "Type",
            style="bold yellow",
        )

        table.add_column("Value")

        for ioc in iocs:

            if isinstance(ioc, dict):

                ioc_type = ioc.get(
                    "type",
                    "",
                )

                value = ioc.get(
                    "value",
                    "",
                )

            else:

                ioc_type = getattr(
                    ioc,
                    "type",
                    "",
                )

                value = getattr(
                    ioc,
                    "value",
                    "",
                )

            table.add_row(
                str(ioc_type),
                str(value),
            )

        self.console.print(table)