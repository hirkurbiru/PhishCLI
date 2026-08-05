"""
Tests for AccountStorage.
"""

import shutil

from accounts.storage import (
    AccountStorage,
    PROFILES_DIR,
)


def setup_function():
    """
    Clean test profiles before each test.
    """

    if PROFILES_DIR.exists():

        shutil.rmtree(PROFILES_DIR)

    PROFILES_DIR.mkdir(parents=True, exist_ok=True)


def teardown_function():
    """
    Clean test profiles after each test.
    """

    if PROFILES_DIR.exists():

        shutil.rmtree(PROFILES_DIR)

    PROFILES_DIR.mkdir(parents=True, exist_ok=True)


def test_create_profile():

    AccountStorage.create_profile(
        "SOC Lab"
    )

    assert AccountStorage.profile_exists(
        "SOC Lab"
    )


def test_list_profiles():

    AccountStorage.create_profile(
        "SOC Lab"
    )

    AccountStorage.create_profile(
        "Testing"
    )

    profiles = AccountStorage.list_profiles()

    assert "soc_lab" in profiles

    assert "testing" in profiles


def test_switch_profile():

    AccountStorage.create_profile(
        "SOC Lab"
    )

    AccountStorage.switch_profile(
        "soc_lab"
    )

    assert (
        AccountStorage.get_active_profile()
        == "soc_lab"
    )


def test_delete_profile():

    AccountStorage.create_profile(
        "SOC Lab"
    )

    AccountStorage.delete_profile(
        "soc_lab"
    )

    assert not AccountStorage.profile_exists(
        "SOC Lab"
    )


def test_duplicate_profile():

    AccountStorage.create_profile(
        "SOC Lab"
    )

    try:

        AccountStorage.create_profile(
            "SOC Lab"
        )

        assert False

    except ValueError:

        assert True