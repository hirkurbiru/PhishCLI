"""
PhishCLI - Attachment Safety Detector
Screens attachment file types against hazardous executable and macro extension vectors.
"""

from pathlib import Path
from typing import Dict, Any, List
from analysis.detectors.base import BaseDetector, DetectorResult


class AttachmentDetector(BaseDetector):
    """Detects high-risk or executable attachment formats."""

    EXECUTABLE_EXTENSIONS = {".exe", ".bat", ".cmd", ".ps1", ".vbs", ".js", ".scr", ".pif", ".hta", ".jar"}
    MACRO_EXTENSIONS = {".docm", ".xlsm", ".pptm", ".dotm"}
    ARCHIVE_EXTENSIONS = {".zip", ".rar", ".7z", ".iso", ".img", ".gz"}

    @property
    def name(self) -> str:
        return "Attachment Payload Analyzer"

    @property
    def weight(self) -> float:
        return 35.0

    def analyze(self, email_data: Dict[str, Any]) -> DetectorResult:
        attachments: List[Dict[str, Any]] = email_data.get("attachments", [])
        if not attachments:
            return DetectorResult(
                detector_name=self.name,
                score_impact=0.0,
                triggered=False,
                description="No attachments present in email.",
                evidence={},
            )

        penalty = 0.0
        flagged_files = []

        for att in attachments:
            filename = att.get("filename", "")
            ext = Path(filename).suffix.lower()

            if ext in self.EXECUTABLE_EXTENSIONS:
                penalty += 25.0
                flagged_files.append(f"{filename} (High Risk: Executable/Script)")
            elif ext in self.MACRO_EXTENSIONS:
                penalty += 15.0
                flagged_files.append(f"{filename} (Medium Risk: Macro-Enabled Office Document)")
            elif ext in self.ARCHIVE_EXTENSIONS:
                penalty += 5.0
                flagged_files.append(f"{filename} (Low Risk: Compressed Archive)")

        triggered = len(flagged_files) > 0
        desc = (
            f"Potentially dangerous attachments identified: {'; '.join(flagged_files)}"
            if triggered
            else "Attachments present, but no hazardous extensions detected."
        )

        return DetectorResult(
            detector_name=self.name,
            score_impact=min(penalty, self.weight),
            triggered=triggered,
            description=desc,
            evidence={"attachments_scanned": len(attachments), "flagged": flagged_files},
        )