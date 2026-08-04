"""
PhishCLI - MSG Investigation

Investigates Microsoft Outlook .msg email files.
"""

from pathlib import Path
from tkinter import Tk
from tkinter.filedialog import askopenfilename

from cli.display import pause

from gmail.msg_parser import MSGParser
from analysis.engine import AnalysisOrchestrator
from investigation.email_investigation import investigate_email


def investigate_msg():
    """
    Investigate a Microsoft Outlook .msg file.
    """

    print("\n" + "=" * 60)
    print("OUTLOOK MSG INVESTIGATION")
    print("=" * 60)

    root = Tk()
    root.withdraw()

    file_path = askopenfilename(

        title="Select a MSG File",

        filetypes=[
            ("Outlook Email", "*.msg"),
            ("All Files", "*.*"),
        ],

    )

    root.destroy()

    if not file_path:

        print("\nNo file selected.")

        pause()

        return

    path = Path(file_path)

    if not path.exists():

        print("\nFile not found.")

        pause()

        return

    try:

        parser = MSGParser()

        parsed_email = parser.parse(
            file_path
        )

        analyzer = AnalysisOrchestrator()

        analysis = analyzer.analyze_email(
            parsed_email
        )

        finding = {

            "email": parsed_email,

            "analysis": analysis,

        }

        investigate_email(
            finding
        )

    except Exception as e:

        print(
            "\nUnable to investigate MSG file."
        )

        print(e)

        pause()