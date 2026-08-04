# PhishCLI

PhishCLI is a command-line phishing email investigation tool built in Python. It integrates with Gmail, analyzes emails using multiple phishing detection techniques, stores investigation history in SQLite, and generates investigation reports in JSON and PDF formats.

---

## Features

- Gmail OAuth Authentication
- Browse and Search Gmail
- Email Parsing
- Phishing Detection Engine
- VirusTotal Integration
- SQLite Database
- Investigation History
- Dashboard
- JSON Report Export
- PDF Report Export
- Multi-Account Management
- Application Settings

---

## Project Structure

```text
PhishCLI/
├── accounts/
├── analysis/
├── cli/
├── dashboard/
├── database/
├── gmail/
├── reports/
├── settings/
├── utils/
├── docs/
├── tests/
├── phishcli.py
├── README.md
└── requirements.txt
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/PhishCLI.git
cd PhishCLI
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Gmail Setup

1. Create a Google Cloud project.
2. Enable the Gmail API.
3. Download `credentials.json`.
4. Place it in the `secrets/` folder.
5. Run the application.

---

## Running

```bash
python phishcli.py
```

---

## Main Menu

```text
1. Browse Latest Emails
2. Search Email
3. Investigation History
4. Dashboard
5. Reports
6. Account Manager
7. Settings
8. Exit
```

---

## Reports

PhishCLI supports exporting:

- JSON Investigation Reports
- PDF Investigation Reports

---

## Dashboard

Displays:

- Total Scan Sessions
- Total Emails
- Classification Statistics
- Top Senders
- Recent Investigations

---

## Technologies Used

- Python
- Gmail API
- SQLite
- SQLAlchemy
- ReportLab
- VirusTotal API

---

## Roadmap

### Version 1.0

- Gmail Integration
- Dashboard
- Reports
- Account Manager
- Settings

### Future Versions

- Web Dashboard
- Email Attachment Analysis
- IOC Enrichment
- Additional Threat Intelligence Providers
- REST API

---

## License

MIT License

---

## Author

Developed by **Hirkur Birlingeshwar Babu**