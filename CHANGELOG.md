# Changelog

All notable changes to this project will be documented in this file.

This project follows the principles of [Keep a Changelog](https://keepachangelog.com/) and Semantic Versioning.

---

# [2.0.0] - 2026-08-06

## Initial Stable Release

This is the first public stable release of **PhishCLI**.

### Added

#### Gmail Integration

- Google OAuth 2.0 authentication
- Gmail API integration
- Multi-profile Gmail support
- Gmail inbox investigation

#### EML Investigation

- Local EML file analysis
- Email header parsing
- Email metadata extraction

#### Detection Engine

- Sender analysis
- URL analysis
- Authentication analysis (SPF, DKIM, DMARC)
- Keyword detection
- Attachment detection

#### Threat Intelligence

- VirusTotal integration
- AbuseIPDB integration
- WHOIS lookup
- DNS lookup

#### Investigation

- Risk score calculation
- Email classification
- Investigation summaries
- Investigation history

#### Reports

- PDF report generation
- JSON report generation

#### User Interface

- Terminal-based interface
- Dashboard
- Search module
- IOC Explorer
- Settings module

#### Database

- SQLite storage
- Investigation persistence

#### Security

- Read-only Gmail access
- Local OAuth token storage
- Secure credential handling

#### Testing

- Manual functional testing
- Gmail authentication testing
- Gmail investigation testing
- EML investigation testing
- Dashboard testing
- IOC Explorer testing
- Search testing
- Report generation testing

#### Documentation

- README.md
- INSTALL.md
- SECURITY.md
- CONTRIBUTING.md
- LICENSE

---

## Known Limitations

- Gmail investigation requires Google OAuth configuration.
- Threat intelligence modules require internet connectivity.
- Some threat intelligence services require API keys.

---

## Code Quality

- Modular architecture
- Approximately 77% code coverage
- Cross-platform support (Windows and Linux)

---

## Release Status

**Stable**

Version:

```
2.0.0
```

Release Date:

```
06 August 2026
```