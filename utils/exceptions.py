"""
PhishCLI - Custom Exception Hierarchy
Provides explicit exception types for precise handling across all layers.
"""


class PhishCLIError(Exception):
    """Base exception for all PhishCLI errors."""

    def __init__(self, message: str, details: str = ""):
        super().__init__(message)
        self.message = message
        self.details = details

    def __str__(self) -> str:
        if self.details:
            return f"{self.message} | Details: {self.details}"
        return self.message


# ==========================================================
# Gmail & Authentication Exceptions
# ==========================================================

class GmailError(PhishCLIError):
    """Raised when Gmail API operations fail."""

    pass


class AuthenticationError(PhishCLIError):
    """Raised when OAuth flow or credential validation fails."""

    pass


class TokenExpiredError(AuthenticationError):
    """Raised when the OAuth token is expired and cannot be refreshed."""

    pass


# ==========================================================
# Email Processing Exceptions
# ==========================================================

class IngestionError(PhishCLIError):
    """Raised when email fetching or parsing fails."""

    pass


class AnalysisError(PhishCLIError):
    """Raised when an internal detector fails during execution."""

    pass


# ==========================================================
# Threat Intelligence Exceptions
# ==========================================================

class ThreatIntelError(PhishCLIError):
    """Raised when external OSINT services fail."""

    pass


# ==========================================================
# Database Exceptions
# ==========================================================

class DatabaseError(PhishCLIError):
    """Raised on database read/write/connection failures."""

    pass


# ==========================================================
# Reporting Exceptions
# ==========================================================

class ReportGenerationError(PhishCLIError):
    """Raised when generating reports fails."""

    pass