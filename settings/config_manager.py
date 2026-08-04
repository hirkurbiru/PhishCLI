"""
PhishCLI - Configuration Manager

Loads and saves application settings.
"""

import json
from pathlib import Path


CONFIG_DIR = Path("config_data")
CONFIG_DIR.mkdir(exist_ok=True)

CONFIG_FILE = CONFIG_DIR / "settings.json"


DEFAULT_SETTINGS = {
    "report_directory": "reports_output",
    "max_recent_emails": 10,
    "virustotal_enabled": True,
    "theme": "default",
}


class ConfigManager:
    """
    Handles application configuration.
    """

    @staticmethod
    def load():

        if not CONFIG_FILE.exists():

            ConfigManager.save(DEFAULT_SETTINGS)

        with open(
            CONFIG_FILE,
            "r",
            encoding="utf-8",
        ) as file:

            return json.load(file)

    @staticmethod
    def save(settings):

        with open(
            CONFIG_FILE,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                settings,
                file,
                indent=4,
            )

    @staticmethod
    def get(key):

        settings = ConfigManager.load()

        return settings.get(key)

    @staticmethod
    def set(key, value):

        settings = ConfigManager.load()

        settings[key] = value

        ConfigManager.save(settings)