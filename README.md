# 🛡️ PhishCLI v2.0.0

> Terminal-Based Phishing Email Investigation Framework

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-green)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Version](https://img.shields.io/badge/Version-2.0.0-red.svg)

---

## 📌 Overview

PhishCLI is a terminal-based phishing email investigation framework developed in Python. It helps SOC analysts, DFIR investigators, cybersecurity students, and security professionals analyze suspicious emails using Gmail API integration or local EML files.

The framework automates phishing analysis by combining multiple detection techniques, threat intelligence services, and risk scoring to identify malicious emails efficiently.

---

## 🎯 Objectives

- Investigate suspicious Gmail messages
- Analyze local EML files
- Detect phishing indicators
- Perform threat intelligence lookups
- Generate investigation reports
- Provide a clear phishing risk score

---

## ✨ Features

### Gmail Investigation

- Gmail OAuth 2.0 Authentication
- Secure Gmail API integration
- Multi-profile support
- Scan Gmail inbox
- Analyze selected emails

### EML Investigation

- Parse local EML files
- Extract email headers
- Analyze sender information
- Detect phishing indicators

### Detection Engine

- Sender Analysis
- URL Detection
- Authentication Checks
- Keyword Detection
- Attachment Detection

### Threat Intelligence

- VirusTotal
- AbuseIPDB
- WHOIS Lookup
- DNS Lookup

### Investigation

- Risk Score Calculation
- Email Classification
- Investigation Summary
- Investigation History

### Reports

- JSON Reports
- PDF Reports

### Additional Modules

- Dashboard
- IOC Explorer
- Search
- Settings

---

## 📸 Screenshots

> Screenshots are available inside:

docs/screenshots/

Example screenshots:

- Main Menu
- Gmail Investigation
- Dashboard
- IOC Explorer
- Reports
- Search
- Settings

---

## 🏗 Architecture

(Architecture diagram will be added here.)

```
+---------------------+
|      PhishCLI       |
+----------+----------+
           |
   Gmail / EML
           |
   Analysis Engine
           |
Threat Intelligence
           |
     Risk Engine
           |
 Investigation Results
```

---

---

# 💻 Installation

## Prerequisites

Before running PhishCLI, ensure you have:

- Python 3.12 or newer
- Git
- Internet connection
- Google Cloud Project (for Gmail Investigation)
- Gmail API enabled

---

## Clone the Repository

```bash
git clone https://github.com/hirkurbiru/PhishCLI.git
```

```bash
cd PhishCLI
```

---

## Create a Virtual Environment

### Windows

```bash
python -m venv .venv
```

Activate:

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
```

Activate:

```bash
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 📂 Project Structure

```text
PhishCLI
│
├── accounts/
├── analysis/
│   └── detectors/
├── cli/
├── config/
├── dashboard/
├── database/
├── docs/
│   └── screenshots/
├── gmail/
├── intelligence/
├── investigation/
├── ioc/
├── reports/
├── search/
├── settings/
├── utils/
│
├── phishcli.py
├── requirements.txt
├── README.md
├── INSTALL.md
├── CHANGELOG.md
├── LICENSE
├── SECURITY.md
└── .gitignore
```

---

# 🔑 Google OAuth Setup

PhishCLI uses Google OAuth 2.0 to securely access Gmail.

## Step 1

Go to the Google Cloud Console.

Create a new project (or use an existing one).

---

## Step 2

Enable:

- Gmail API

---

## Step 3

Configure the OAuth Consent Screen.

Required scope:

```
https://www.googleapis.com/auth/gmail.readonly
```

---

## Step 4

Create an OAuth Client ID.

Application Type:

```
Desktop Application
```

---

## Step 5

Download:

```
credentials.json
```

---

## Step 6

Copy the file to:

```
~/.phishcli/credentials.json
```

Example (Windows):

```text
C:\Users\<username>\.phishcli\credentials.json
```

---

# ▶ Running PhishCLI

Run the application from the project directory:

```bash
python phishcli.py
```

The main menu will appear:

```text
1. Connect Gmail
2. Start Gmail Investigation
3. Scan EML File
4. Investigation History
5. Dashboard
6. IOC Explorer
7. Reports
8. Search
9. Settings
10. Disconnect Gmail
11. Exit
```

---

# 🔐 First Login

Select:

```
1. Connect Gmail
```

A browser window will open.

Sign in with your Gmail account and grant read-only access.

After successful authentication, PhishCLI securely stores your OAuth token for future sessions.

---

# 📁 Configuration Directory

PhishCLI stores user-specific data in:

```text
~/.phishcli/
```

Example:

```text
.phishcli/
│
├── credentials.json
├── data/
├── logs/
├── reports/
└── tokens/
```

No passwords are stored.

Only OAuth access tokens issued by Google are saved locally.

---
---

# 🔍 Investigation Workflow

PhishCLI follows a structured investigation pipeline to analyze suspicious emails.

```text
                  Start Investigation
                          │
                          ▼
              Select Investigation Type
                ├──────────────┐
                ▼              ▼
         Gmail Investigation   EML Investigation
                │              │
                └──────┬───────┘
                       ▼
                Parse Email Content
                       ▼
              Extract Email Metadata
                       ▼
                Run Detection Engine
                       ▼
         ┌─────────────┼─────────────┐
         ▼             ▼             ▼
   Sender Check    URL Analysis   Auth Analysis
         ▼             ▼             ▼
      Keyword Detection      Attachment Analysis
                       ▼
            Threat Intelligence Lookups
         ┌─────────────┼─────────────┐
         ▼             ▼             ▼
      VirusTotal      WHOIS      AbuseIPDB
                       ▼
               Risk Score Calculation
                       ▼
                Email Classification
                       ▼
              Store Investigation Data
                       ▼
              Generate Reports & Summary
                       ▼
                     Complete
```

---

# 🧠 Detection Engine

The Detection Engine analyzes every email using multiple independent detectors.

## Sender Analysis

Checks:

- Suspicious sender addresses
- Display name spoofing
- Domain reputation
- Unusual sender patterns

---

## URL Detection

Examines URLs for:

- Suspicious domains
- URL shortening services
- Embedded links
- Domain anomalies

---

## Authentication Analysis

Evaluates email authentication:

- SPF
- DKIM
- DMARC

Authentication failures increase the email's overall risk score.

---

## Keyword Detection

Identifies phishing-related keywords commonly used in:

- Account verification emails
- Password reset requests
- Urgent security notifications
- Financial scams

---

## Attachment Detection

Inspects attachments for:

- Suspicious file extensions
- Potentially dangerous attachment types

---

# 🌐 Threat Intelligence

PhishCLI enriches investigations using external intelligence services.

## VirusTotal

Checks:

- Domain reputation
- Malicious detections
- Community analysis

---

## AbuseIPDB

Retrieves:

- Abuse confidence score
- Reported malicious activity

---

## WHOIS Lookup

Collects:

- Domain registration information
- Domain age
- Registrar details

Recently registered domains may indicate phishing infrastructure.

---

## DNS Lookup

Retrieves DNS information including:

- A Records
- MX Records
- Name Servers

---

# 🎯 Risk Scoring

PhishCLI combines detector results and threat intelligence into a single risk score.

## Classification

| Score | Classification |
|-------:|----------------|
| 0–30 | Safe |
| 31–60 | Suspicious |
| 61–85 | High Risk |
| 86–100 | Phishing |

---

## Score Calculation

Risk scores are influenced by:

- Detection engine results
- Authentication failures
- Domain reputation
- VirusTotal detections
- AbuseIPDB confidence
- Domain age

The final score is normalized to a maximum of **100**.

---

# 📊 Investigation Summary

After every investigation, PhishCLI displays:

- Investigation ID
- Emails Analyzed
- Safe Emails
- Suspicious Emails
- High Risk Emails
- Phishing Emails
- Flagged Email Count

Example:

```text
=========================================================
INVESTIGATION SUMMARY
=========================================================

Investigation ID : 201

Emails Analyzed  : 25

Safe             : 20

Suspicious       : 3

High Risk        : 1

Phishing         : 1

Flagged Emails   : 5
```

---

# 📄 Reports

PhishCLI supports two report formats.

## JSON Report

Contains:

- Investigation metadata
- Risk scores
- Email details
- Threat intelligence
- Detection results

Suitable for automation and SIEM ingestion.

---

## PDF Report

Human-readable investigation report including:

- Executive summary
- Risk assessment
- Email information
- Threat intelligence
- Investigation findings

Suitable for incident response documentation.

---

# 📈 Dashboard

The Dashboard provides an overview of investigation activity.

Displayed metrics include:

- Total Investigations
- Emails Analyzed
- Safe Emails
- Suspicious Emails
- High Risk Emails
- Phishing Emails

---

# 🔍 IOC Explorer

IOC Explorer allows analysts to review collected Indicators of Compromise.

Supported IOC types include:

- Domains
- URLs
- IP Addresses
- Email Addresses

---

# 🔎 Search

Search previously analyzed investigations by:

- Sender
- Subject
- Domain
- Email Address
- Investigation ID

This allows investigators to quickly revisit historical results.

---
---

# 🛠 Technologies Used

## Programming Language

- Python 3.12

---

## Gmail Integration

- Gmail API
- Google OAuth 2.0

---

## Database

- SQLite
- SQLAlchemy

---

## Threat Intelligence

- VirusTotal API
- AbuseIPDB API
- WHOIS Lookup
- DNS Lookup

---

## Reporting

- ReportLab (PDF Reports)
- JSON

---

## Python Libraries

- requests
- google-api-python-client
- google-auth-oauthlib
- google-auth-httplib2
- dnspython
- python-whois
- checkdmarc
- tldextract
- click
- rich

---

# 🔒 Security

PhishCLI follows security best practices during investigations.

### OAuth Security

- Uses Google OAuth 2.0
- No Gmail passwords are stored
- Uses Google's official authentication flow
- Read-only Gmail access

### Local Storage

User data is stored inside:

```
~/.phishcli/
```

Stored data includes:

- OAuth Tokens
- Investigation Database
- Reports
- Logs

Sensitive credentials are never uploaded to external services.

---

# 📊 Project Statistics

| Metric | Value |
|---------|------:|
| Language | Python |
| Version | 2.0.0 |
| Architecture | Modular |
| Gmail Support | ✅ |
| EML Support | ✅ |
| Threat Intelligence | 4 Providers |
| Report Formats | JSON / PDF |
| Database | SQLite |
| License | MIT |

---

# 📁 Documentation

| File | Description |
|------|-------------|
| README.md | Project Overview |
| INSTALL.md | Installation Guide |
| CHANGELOG.md | Version History |
| SECURITY.md | Security Information |
| LICENSE | MIT License |

---

# 🧪 Testing

Testing completed before release included:

- Manual Testing
- Gmail Authentication Testing
- Gmail Investigation Testing
- EML Investigation Testing
- Dashboard Testing
- IOC Explorer Testing
- Search Testing
- Report Generation Testing
- Settings Testing
- Multi-profile Testing

Code Coverage:

```
77%
```

---

# ⚠ Known Limitations

Current limitations include:

- Gmail API requires Google OAuth configuration.
- Internet connection is required for threat intelligence lookups.
- Threat intelligence results depend on third-party API availability.
- Currently designed as a terminal-based application.

---

# 📅 Release Information

Project:

```
PhishCLI
```

Version:

```
2.0.0
```

Release Type:

```
Stable
```

Platform:

```
Windows
Linux
```

Python:

```
3.12+
```

---

# 📌 Roadmap

Version **2.0.0** represents the final planned feature release.

Future maintenance, if required, will focus on:

- Bug fixes
- Dependency updates
- Compatibility improvements

No additional features are currently planned.

---

# 🤝 Contributing

Community contributions are welcome.

If you discover:

- Bugs
- Documentation issues
- Security vulnerabilities

please open a GitHub Issue.

---

# 🛡 Responsible Use

PhishCLI is intended for:

- Security Operations Centers (SOC)
- Digital Forensics & Incident Response (DFIR)
- Cybersecurity education
- Security research
- Defensive security operations

Users are responsible for complying with all applicable laws, organizational policies, and service provider terms when analyzing email accounts.

---

# 📄 License

This project is licensed under the MIT License.

See the LICENSE file for details.

---

# 👨‍💻 Author

**Hirkur Birlinegshwar Babu**

GitHub:

https://github.com/hirkurbiru

---

# ⭐ Support

If you found this project useful:

- ⭐ Star the repository
- 🐞 Report issues
- 💡 Share suggestions
- 🤝 Contribute improvements

---

# 🙏 Acknowledgements

Special thanks to the open-source community and the maintainers of the libraries and APIs used in this project, including:

- Google Gmail API
- VirusTotal
- AbuseIPDB
- SQLAlchemy
- ReportLab
- Python Software Foundation

---

## Thank You

Thank you for using **PhishCLI v2.0.0**.

Happy Investigating! 🛡️📧
