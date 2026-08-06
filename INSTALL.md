# PhishCLI v2.0.0 Installation Guide

## Requirements

Before installing PhishCLI, ensure you have:

- Python 3.12 or later
- Git
- Internet connection
- Google Account (for Gmail Investigation)

---

# Step 1 - Clone the Repository

```bash
git clone https://github.com/hirkurbiru/PhishCLI.git
```

```bash
cd PhishCLI
```

---

# Step 2 - Create a Virtual Environment

## Windows

```bash
python -m venv .venv
```

Activate:

```bash
.venv\Scripts\activate
```

## Linux

```bash
python3 -m venv .venv
```

Activate:

```bash
source .venv/bin/activate
```

---

# Step 3 - Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Step 4 - Configure Google OAuth

## Create a Google Cloud Project

1. Go to Google Cloud Console.
2. Create a project.
3. Enable Gmail API.
4. Configure the OAuth Consent Screen.
5. Create a Desktop OAuth Client.
6. Download `credentials.json`.

---

# Step 5 - Place Credentials

Copy the downloaded file to:

## Windows

```text
C:\Users\<username>\.phishcli\credentials.json
```

## Linux

```text
~/.phishcli/credentials.json
```

---

# Step 6 - Run PhishCLI

```bash
python phishcli.py
```

---

# First Login

1. Select **Connect Gmail**.
2. A browser window will open.
3. Sign in with your Gmail account.
4. Grant read-only Gmail access.
5. OAuth token will be stored locally.

---

# Troubleshooting

## credentials.json not found

Ensure the file exists at:

```text
~/.phishcli/credentials.json
```

---

## Authentication Failed

- Verify Gmail API is enabled.
- Verify OAuth Consent Screen is configured.
- Ensure your Google account is authorized (if using Testing mode).

---

## Gmail API Errors

Check:

- Internet connection
- Google Cloud configuration
- OAuth credentials
- Gmail API status

---

# Updating

```bash
git pull
pip install -r requirements.txt
```

---

# Uninstall

Delete:

```text
Project Folder
```

and optionally remove:

```text
~/.phishcli/
```

to delete:

- OAuth Tokens
- Reports
- Logs
- Database

---

# Support

If you encounter issues:

- Open a GitHub Issue.
- Review the README.
- Verify your Google OAuth configuration.
