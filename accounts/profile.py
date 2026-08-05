"""
PhishCLI - User Profile Model

Defines a PhishCLI user profile.

A profile stores information about one user's
workspace and account configuration.

This module only defines the profile object.
It does NOT create folders, authenticate users,
or manage sessions.
"""

from dataclasses import dataclass, field
from datetime import datetime, UTC
from pathlib import Path
import uuid


@dataclass(slots=True)
class Profile:
    """
    Represents a PhishCLI user profile.
    """

    profile_id: str = field(
        default_factory=lambda: str(uuid.uuid4())
    )

    profile_name: str = ""

    email: str = ""

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    last_login: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    profile_directory: Path = Path()

    database_path: Path = Path()

    token_path: Path = Path()

    reports_path: Path = Path()

    active: bool = False