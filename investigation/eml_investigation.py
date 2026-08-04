"""
PhishCLI - EML Investigation

Investigates an exported .eml email.
"""

from pathlib import Path
from tkinter import Tk
from tkinter.filedialog import askopenfilename

from cli.display import pause

from gmail.eml_parser import EMLParser
from analysis.engine import AnalysisOrchestrator
from investigation.email_investigation import investigate_email


def investigate_eml():
    """
    Investigate an EML file.
    """

    print("\n" + "=" * 60)
    print("EML FILE INVESTIGATION")
    print("=" * 60)

    # Hide tkinter root window
    root = Tk()
    root.withdraw()

    file_path = askopenfilename(

        title="Select an EML File",

        filetypes=[
            ("Email Files", "*.eml"),
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

        parser = EMLParser()

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
            f"\nUnable to investigate EML file.\n\n{e}"
        )

        pause()