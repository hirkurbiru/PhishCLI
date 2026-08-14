"""
PhishCLI - System Constants
Defines global immutable constants, paths, and default configurations.
"""

from pathlib import Path

# Application Metadata
APP_NAME = "PhishCLI"
APP_VERSION = "0.1.0"
APP_TAGLINE = "Terminal-Based Phishing Email Investigation Framework"

# File System Paths
USER_HOME = Path.home()
APP_DIR = USER_HOME / ".phishcli"
LOGS_DIR = APP_DIR / "logs"
DATA_DIR = APP_DIR / "data"
TOKENS_DIR = APP_DIR / "tokens"
REPORTS_DIR = APP_DIR / "reports"

# Ensure runtime directories exist securely
for directory in [APP_DIR, LOGS_DIR, DATA_DIR, TOKENS_DIR, REPORTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Database
DB_PATH = DATA_DIR / "phishcli.db"

# OAuth Configuration
GMAIL_READONLY_SCOPE = ["https://www.googleapis.com/auth/gmail.readonly"]
TOKEN_FILE_PATH = TOKENS_DIR / "token.json"
CREDENTIALS_FILE_PATH = APP_DIR / "credentials.json"

# Risk Engine Thresholds
SCORE_THRESHOLD_SAFE = 30
SCORE_THRESHOLD_SUSPICIOUS = 60
SCORE_THRESHOLD_HIGH_RISK = 85
SCORE_MAX = 100

# Classification Labels
CLASS_SAFE = "Safe"
CLASS_SUSPICIOUS = "Suspicious"
CLASS_HIGH_RISK = "High Risk"
CLASS_PHISHING = "Phishing"

