"""
PhishCLI - Typer Command Line Interface Entrypoint
Defines interactive commands for scanning emails and generating reports.
"""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

# Database
from database.connection import init_db
from database.connection import SessionLocal
from database.repository import ScanRepository

# Analysis
from analysis.eml_parser import EMLParser
from analysis.engine import AnalysisOrchestrator

# Reports
from reports.terminal_report import TerminalReporter
from reports.json_report import JSONExporter
from reports.pdf_report import PDFExporter

app = typer.Typer(
    name="phishcli",
    help="PhishCLI - Anti-Phishing Email Investigation Framework",
    add_completion=False,
)

console = Console()


@app.callback()
def setup_environment():
    """Initialize the application."""
    init_db()


@app.command()
def scan(
    file_path: str = typer.Argument(..., help="Path to the .eml file"),
    export_json: Optional[str] = typer.Option(
        None,
        "--json",
        help="Export JSON report",
    ),
    export_pdf: Optional[str] = typer.Option(
        None,
        "--pdf",
        help="Export PDF report",
    ),
):
    """Analyze an email file."""

    path = Path(file_path)

    if not path.exists():
        console.print(f"[bold red]Error:[/] File not found: {file_path}")
        raise typer.Exit(code=1)

    console.print(f"[cyan]Scanning:[/] {path.name}")

    # Parse
    try:
        parsed_email = EMLParser.parse_file(str(path))
    except Exception as e:
        console.print(f"[red]Parser Error:[/] {e}")
        raise typer.Exit(code=1)

    # Analyze
    try:
        orchestrator = AnalysisOrchestrator()
        results = orchestrator.analyze_email(parsed_email)
    except Exception as e:
        console.print(f"[red]Analysis Error:[/] {e}")
        raise typer.Exit(code=1)

    # Database Persistence
    db = None
    try:
        db = SessionLocal()
        repo = ScanRepository(db)

        scan_session = repo.create_scan_session("LOCAL_EML")

        findings = [
            {
                "detector_name": r.detector_name,
                "score_impact": r.score_impact,
                "triggered": r.triggered,
                "description": r.description,
                "evidence": r.evidence,
            }
            for r in results["detector_results"]
        ]
        
        from rich import print
        
        repo.save_email_analysis(
            session_id=scan_session.id,
            email_meta=results["email_data"],
            risk_score=results["risk_score"],
            classification=results["classification"],
            explanation=results["explanation"],
            findings=findings,
            iocs=results["iocs"],
        )

        console.print("[green]✓ Scan saved to database[/green]")

    except Exception as e:
        console.print(f"[red]Database Error:[/] {e}")

    finally:
        if db is not None:
            db.close()

    # Terminal Report
    try:
        reporter = TerminalReporter()
        reporter.print_scan_results(results)
    except Exception as e:
        console.print(f"[yellow]Terminal report skipped:[/] {e}")

    # JSON Export
    if export_json:
        try:
            JSONExporter.export(results, export_json)
            console.print(f"[green]JSON exported:[/] {export_json}")
        except Exception as e:
            console.print(f"[red]JSON export failed:[/] {e}")

    # PDF Export
    if export_pdf:
        try:
            PDFExporter.export(results, export_pdf)
            console.print(f"[green]PDF exported:[/] {export_pdf}")
        except Exception as e:
            console.print(f"[red]PDF export failed:[/] {e}")


@app.command()
def history():
    """Display previously scanned emails."""

    from rich.table import Table
    from database.connection import SessionLocal
    from database.repository import ScanRepository

    db = SessionLocal()

    try:
        repo = ScanRepository(db)
        history = repo.get_scan_history()

        if not history:
            console.print("[yellow]No scan history found.[/yellow]")
            return

        table = Table(title="PhishCLI Scan History")

        table.add_column("ID", style="cyan")
        table.add_column("Date", style="green")
        table.add_column("Sender", style="yellow")
        table.add_column("Score", justify="right")
        table.add_column("Classification", style="bold")

        for email, analysis in history:
            table.add_row(
                str(email.id),
                str(email.scanned_at)[:19],
                email.sender or "-",
                f"{analysis.risk_score:.1f}",
                analysis.classification,
            )

        console.print(table)

    except Exception as e:
        console.print(f"[red]History Error:[/] {e}")

    finally:
        db.close()

if __name__ == "__main__":
    app()