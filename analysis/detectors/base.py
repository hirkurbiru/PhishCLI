"""
PhishCLI - Detector Plugin Framework (Abstract Base Class)
Establishes the strict contract for all threat detection engines.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Any, List


@dataclass
class DetectorResult:
    """Standardized return payload for all PhishCLI detectors."""

    detector_name: str
    score_impact: float
    triggered: bool
    description: str
    evidence: Dict[str, Any] = field(default_factory=dict)


class BaseDetector(ABC):
    """Abstract Base Class enforced across all phishing detectors."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Returns the unique name of the detector."""
        pass

    @property
    @abstractmethod
    def weight(self) -> float:
        """Default penalty score if the rule is triggered."""
        pass

    @abstractmethod
    def analyze(self, email_data: Dict[str, Any]) -> DetectorResult:
        """Processes email data and produces a standardized DetectorResult."""
        pass