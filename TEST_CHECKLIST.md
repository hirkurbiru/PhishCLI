# PhishCLI Test Checklist

## Project Version

Version: 1.0.0

Date:

Tester:

---

# Gmail Connection

| Test | Expected | Result | Status |
|------|----------|--------|--------|
| Connect Gmail | Gmail connects successfully | | ⬜ |
| Disconnect Gmail | Gmail disconnects successfully | | ⬜ |
| Connect different Gmail account | New account opens correctly | | ⬜ |
| Reconnect previous account | Works correctly | | ⬜ |

---

# Gmail Investigation

| Test | Expected | Result | Status |
|------|----------|--------|--------|
| Latest 10 Emails | 10 emails analyzed | | ⬜ |
| Latest 25 Emails | 25 emails analyzed | | ⬜ |
| Latest 50 Emails | 50 emails analyzed | | ⬜ |
| Latest 100 Emails | 100 emails analyzed | | ⬜ |
| Entire Inbox | Investigation completes | | ⬜ |

---

# EML Investigation

| Test | Expected | Result | Status |
|------|----------|--------|--------|
| Open valid .eml | Parsed successfully | | ⬜ |
| Invalid file | Error displayed | | ⬜ |
| Cancel file picker | Returns to menu | | ⬜ |
| HTML email | Parsed correctly | | ⬜ |
| Plain text email | Parsed correctly | | ⬜ |

---

# MSG Investigation

| Test | Expected | Result | Status |
|------|----------|--------|--------|
| Open valid .msg | Parsed successfully | | ⬜ |
| Invalid .msg | Error displayed | | ⬜ |
| Cancel file picker | Returns to menu | | ⬜ |

---

# Authentication Detector

| Test | Expected | Result | Status |
|------|----------|--------|--------|
| SPF Pass | No penalty | | ⬜ |
| SPF Fail | Detector triggers | | ⬜ |
| DKIM Fail | Detector triggers | | ⬜ |
| DMARC Fail | Detector triggers | | ⬜ |

---

# Sender Detector

| Test | Expected | Result | Status |
|------|----------|--------|--------|
| Reply-To mismatch | Triggered | | ⬜ |
| Return-Path mismatch | Triggered | | ⬜ |
| Legitimate sender | Not triggered | | ⬜ |

---

# URL Detector

| Test | Expected | Result | Status |
|------|----------|--------|--------|
| HTTP URL | Triggered | | ⬜ |
| HTTPS URL | No penalty | | ⬜ |
| IP Address URL | Triggered | | ⬜ |
| URL Shortener | Triggered | | ⬜ |
| Suspicious TLD | Triggered | | ⬜ |

---

# Keyword Detector

| Test | Expected | Result | Status |
|------|----------|--------|--------|
| Verify your account | Triggered | | ⬜ |
| Password expired | Triggered | | ⬜ |
| Wire transfer | Triggered | | ⬜ |
| Normal email | Not triggered | | ⬜ |

---

# Attachment Detector

| Test | Expected | Result | Status |
|------|----------|--------|--------|
| PDF | Parsed | | ⬜ |
| ZIP | Parsed | | ⬜ |
| DOCM | Triggered (if supported) | | ⬜ |
| EXE | Triggered (if supported) | | ⬜ |

---

# Risk Engine

| Test | Expected | Result | Status |
|------|----------|--------|--------|
| Safe email | Safe | | ⬜ |
| Suspicious email | Suspicious | | ⬜ |
| High-risk email | High Risk | | ⬜ |
| Phishing sample | Phishing | | ⬜ |

---

# Reports

| Test | Expected | Result | Status |
|------|----------|--------|--------|
| PDF Export | Opens successfully | | ⬜ |
| JSON Export | Valid JSON | | ⬜ |

---

# Dashboard

| Test | Expected | Result | Status |
|------|----------|--------|--------|
| Statistics | Correct | | ⬜ |
| Top Senders | Correct | | ⬜ |
| Recent Investigations | Correct | | ⬜ |

---

# Database

| Test | Expected | Result | Status |
|------|----------|--------|--------|
| Investigation saved | Yes | | ⬜ |
| Risk Score saved | Yes | | ⬜ |
| IOCs saved | Yes | | ⬜ |

---

# Error Handling

| Test | Expected | Result | Status |
|------|----------|--------|--------|
| Invalid Gmail Token | Error shown | | ⬜ |
| No Internet | Error shown | | ⬜ |
| Invalid EML | Error shown | | ⬜ |
| Invalid MSG | Error shown | | ⬜ |
| Invalid API Key | Error shown | | ⬜ |

---

# Performance

| Test | Expected | Result | Status |
|------|----------|--------|--------|
| 10 Emails | Pass | | ⬜ |
| 100 Emails | Pass | | ⬜ |
| Entire Inbox | Pass | | ⬜ |

---

# Final Release Checklist

- ⬜ Gmail Investigation
- ⬜ EML Investigation
- ⬜ MSG Investigation
- ⬜ Dashboard
- ⬜ History
- ⬜ Reports
- ⬜ Settings
- ⬜ Threat Intelligence
- ⬜ PDF Export
- ⬜ JSON Export
- ⬜ No crashes
- ⬜ Version 1.0 Ready