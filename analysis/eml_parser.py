"""
PhishCLI - Local EML File Ingestion Parser
Allows offline ingestion and security analysis of raw .eml export files.
"""

from pathlib import Path
from typing import Dict, Any, Union

from analysis.extractor import EmailExtractor
from utils.exceptions import IngestionError
from config.logging_config import logger


class EMLParser:
    """Parses exported local .eml email files."""

    @classmethod
    def parse_file(cls, eml_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Reads a local .eml file and converts it into a standardized
        email dictionary.

        Accepts either:
        - str
        - pathlib.Path
        """

        # Convert string paths into Path objects
        eml_path = Path(eml_path)

        # Validate file
        if not eml_path.exists():
            raise IngestionError(f"Target .eml file does not exist: {eml_path}")

        if not eml_path.is_file():
            raise IngestionError(f"Target is not a file: {eml_path}")

        try:
            logger.info(f"Parsing local .eml file: {eml_path}")

            with eml_path.open("rb") as f:
                raw_bytes = f.read()

            parsed_data = EmailExtractor.parse_raw_bytes(raw_bytes)

            if not isinstance(parsed_data, dict):
                raise IngestionError(
                    "EmailExtractor returned an invalid result."
                )

            parsed_data["file_source"] = str(eml_path.resolve())

            return parsed_data

        except IngestionError:
            raise

        except Exception as e:
            logger.exception("Failed to parse .eml file")

            raise IngestionError(
                f"Invalid or unreadable .eml file: {eml_path.name}",
                details=str(e),
            ) from e