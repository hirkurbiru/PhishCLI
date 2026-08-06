"""
PhishCLI - Profile Paths

Provides profile-specific workspace paths.
"""

from pathlib import Path

from accounts.session import SessionManager
from accounts.storage import AccountStorage


class ProfilePaths:
    """
    Returns directories and files for the active profile.
    """

    @staticmethod
    def get_profile_dir() -> Path:
        """
        Returns the active profile directory.
        """

        profile = SessionManager.get_profile()

        if not profile:

            raise RuntimeError(
                "No active profile."
            )

        return AccountStorage.get_profile_directory(
            profile
        )

    @staticmethod
    def get_reports_dir() -> Path:
        """
        Returns the reports directory.
        """

        return (
            ProfilePaths.get_profile_dir()
            / "reports"
        )

    @staticmethod
    def get_database_dir() -> Path:
        """
        Returns the database directory.
        """

        return (
            ProfilePaths.get_profile_dir()
            / "database"
        )

    @staticmethod
    def get_logs_dir() -> Path:
        """
        Returns the logs directory.
        """

        return (
            ProfilePaths.get_profile_dir()
            / "logs"
        )

    @staticmethod
    def get_exports_dir() -> Path:
        """
        Returns the exports directory.
        """

        return (
            ProfilePaths.get_profile_dir()
            / "exports"
        )

    @staticmethod
    def get_investigations_dir() -> Path:
        """
        Returns the investigations directory.
        """

        return (
            ProfilePaths.get_profile_dir()
            / "investigations"
        )

    @staticmethod
    def get_attachments_dir() -> Path:
        """
        Returns the attachments directory.
        """

        return (
            ProfilePaths.get_profile_dir()
            / "attachments"
        )

    @staticmethod
    def get_cache_dir() -> Path:
        """
        Returns the cache directory.
        """

        return (
            ProfilePaths.get_profile_dir()
            / "cache"
        )

    @staticmethod
    def get_settings_dir() -> Path:
        """
        Returns the settings directory.
        """

        return (
            ProfilePaths.get_profile_dir()
            / "settings"
        )

    @staticmethod
    def get_temp_dir() -> Path:
        """
        Returns the temporary directory.
        """

        return (
            ProfilePaths.get_profile_dir()
            / "temp"
        )

    @staticmethod
    def get_token_file() -> Path:
        """
        Returns the Gmail OAuth token file.
        """

        return (
            ProfilePaths.get_profile_dir()
            / "token.json"
        )

    @staticmethod
    def get_metadata_file() -> Path:
        """
        Returns the profile metadata file.
        """

        return (
            ProfilePaths.get_profile_dir()
            / "metadata.json"
        )