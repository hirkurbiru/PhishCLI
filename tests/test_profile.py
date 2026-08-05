"""
Tests for the PhishCLI Profile model.
"""

from pathlib import Path
from datetime import datetime

from accounts.profile import Profile


def test_create_default_profile():
    """
    Test creating a profile with default values.
    """

    profile = Profile()

    assert profile.profile_id != ""
    assert profile.profile_name == ""
    assert profile.email == ""
    assert isinstance(profile.created_at, datetime)
    assert isinstance(profile.last_login, datetime)
    assert profile.profile_directory == Path()
    assert profile.database_path == Path()
    assert profile.token_path == Path()
    assert profile.reports_path == Path()
    assert profile.active is False


def test_create_custom_profile():
    """
    Test creating a profile with custom values.
    """

    profile = Profile(
        profile_name="Biru",
        email="biru@example.com",
        profile_directory=Path("profiles/biru"),
        database_path=Path("profiles/biru/phishcli.db"),
        token_path=Path("profiles/biru/token.json"),
        reports_path=Path("profiles/biru/reports"),
        active=True,
    )

    assert profile.profile_name == "Biru"
    assert profile.email == "biru@example.com"
    assert profile.profile_directory == Path("profiles/biru")
    assert profile.database_path == Path("profiles/biru/phishcli.db")
    assert profile.token_path == Path("profiles/biru/token.json")
    assert profile.reports_path == Path("profiles/biru/reports")
    assert profile.active is True


def test_profile_id_is_unique():
    """
    Every profile should have a unique UUID.
    """

    profile1 = Profile()
    profile2 = Profile()

    assert profile1.profile_id != profile2.profile_id


def test_created_and_last_login_are_initialized():
    """
    Datetime fields should be initialized automatically.
    """

    profile = Profile()

    assert profile.created_at is not None
    assert profile.last_login is not None


def test_profile_paths_are_path_objects():
    """
    Path fields should use pathlib.Path.
    """

    profile = Profile()

    assert isinstance(profile.profile_directory, Path)
    assert isinstance(profile.database_path, Path)
    assert isinstance(profile.token_path, Path)
    assert isinstance(profile.reports_path, Path)