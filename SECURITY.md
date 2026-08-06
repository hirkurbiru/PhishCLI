# Security Policy

## Supported Versions

The following versions of PhishCLI are currently supported.

| Version | Supported |
|----------|-----------|
| 2.0.0 | ✅ Yes |

---

# Reporting a Security Vulnerability

If you discover a security vulnerability in PhishCLI, please report it responsibly.

Please do **not** publicly disclose the vulnerability before it has been reviewed.

Instead:

- Open a private GitHub issue (if private reporting is available).
- Or contact the project maintainer directly.

When reporting a vulnerability, include:

- A clear description of the issue.
- Steps to reproduce.
- Expected behavior.
- Actual behavior.
- Screenshots or logs (if applicable).

---

# Security Practices

PhishCLI follows several security best practices.

## Gmail Authentication

- Uses Google's official OAuth 2.0 flow.
- Does not store Gmail passwords.
- Requests read-only Gmail access.
- Uses secure OAuth tokens.

---

## Local Storage

Sensitive information is stored locally.

The application stores:

- OAuth tokens
- Investigation database
- Reports
- Logs

These files are stored inside the user's configuration directory.

Example:

Windows

```
C:\Users\<username>\.phishcli\
```

Linux

```
~/.phishcli/
```

---

## Credentials

Google OAuth credentials are never embedded into the source code.

Users are responsible for protecting:

- credentials.json
- OAuth tokens

These files should never be committed to GitHub.

---

## API Keys

If Threat Intelligence services require API keys:

- Store them locally.
- Never publish them.
- Rotate compromised keys immediately.

---

## Third-Party Services

PhishCLI may communicate with:

- Gmail API
- VirusTotal
- AbuseIPDB
- WHOIS services
- DNS servers

Data returned from these services depends on their availability and policies.

---

## Responsible Use

PhishCLI is intended for:

- Security Operations Centers (SOC)
- Digital Forensics & Incident Response (DFIR)
- Cybersecurity education
- Defensive security research

Users are responsible for complying with:

- Applicable laws
- Organizational policies
- Service provider terms

---

## Scope

This project is intended as a defensive security tool.

It is not designed to facilitate unauthorized access, offensive operations, or malicious activity.

---

## Security Updates

Security-related fixes will be documented in the CHANGELOG when applicable.