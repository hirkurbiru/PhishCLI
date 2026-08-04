"""
PhishCLI - Gmail Parser

Parses Gmail API messages into a standard format.
"""

import base64
import re
from urllib.parse import urlparse


class GmailParser:
    """Parses Gmail API messages."""

    URL_REGEX = re.compile(
        r"https?://[^\s<>\"]+",
        re.IGNORECASE,
    )

    @staticmethod
    def get_header(headers, name):
        """Return the value of a header."""

        for header in headers:

            if header["name"].lower() == name.lower():

                return header["value"]

        return ""

    @staticmethod
    def decode_body(data):
        """Decode Gmail Base64 URL-safe body."""

        if not data:
            return ""

        try:

            data += "=" * (-len(data) % 4)

            return base64.urlsafe_b64decode(
                data
            ).decode(
                "utf-8",
                errors="ignore",
            )

        except Exception:

            return ""

    @classmethod
    def extract_urls(cls, body):
        """
        Extract URLs from email body.
        """

        urls = []

        matches = cls.URL_REGEX.findall(body)

        for url in matches:

            parsed = urlparse(url)

            host = parsed.hostname or ""

            is_ip = bool(
                re.fullmatch(
                    r"\d{1,3}(\.\d{1,3}){3}",
                    host,
                )
            )

            urls.append(
                {
                    "raw_url": url,
                    "scheme": parsed.scheme.lower(),
                    "domain": host.lower(),
                    "has_ip_host": is_ip,
                }
            )

        return urls

    @classmethod
    def extract_attachments(cls, payload):
        """
        Extract attachment metadata.
        """

        attachments = []

        for part in payload.get("parts", []):

            filename = part.get("filename")

            if filename:

                attachments.append(
                    {
                        "filename": filename,
                        "sha256": None,
                        "md5": None,
                    }
                )

        return attachments

    @classmethod
    def extract_auth_results(cls, headers):
        """
        Extract SPF, DKIM and DMARC results from
        Authentication-Results header.
        """

        auth_header = cls.get_header(
            headers,
            "Authentication-Results",
        ).lower()

        auth_results = {
            "spf": "unknown",
            "dkim": "unknown",
            "dmarc": "unknown",
        }

        if "spf=pass" in auth_header:
            auth_results["spf"] = "pass"

        elif "spf=fail" in auth_header:
            auth_results["spf"] = "fail"

        if "dkim=pass" in auth_header:
            auth_results["dkim"] = "pass"

        elif "dkim=fail" in auth_header:
            auth_results["dkim"] = "fail"

        if "dmarc=pass" in auth_header:
            auth_results["dmarc"] = "pass"

        elif "dmarc=fail" in auth_header:
            auth_results["dmarc"] = "fail"

        return auth_results

    @classmethod
    def parse(cls, message):
        """
        Parse Gmail message into a standardized format.
        """

        payload = message.get("payload", {})

        headers = payload.get("headers", [])

        parsed_email = {

            "message_id": message.get("id"),

            "sender": cls.get_header(headers, "From"),

            "from": cls.get_header(headers, "From"),

            "recipient": cls.get_header(headers, "To"),

            "to": cls.get_header(headers, "To"),

            "subject": cls.get_header(headers, "Subject"),

            "date": cls.get_header(headers, "Date"),

            "reply_to": cls.get_header(headers, "Reply-To"),

            "return_path": cls.get_header(headers, "Return-Path"),

            "body": "",

            "snippet": message.get("snippet", ""),

            "urls": [],

            "attachments": [],

            "auth_results": {},
        }

        body = payload.get("body", {}).get("data")

        if body:

            parsed_email["body"] = cls.decode_body(
                body
            )

        else:

            for part in payload.get("parts", []):

                mime = part.get(
                    "mimeType",
                    "",
                )

                if mime == "text/plain":

                    parsed_email["body"] = cls.decode_body(
                        part.get(
                            "body",
                            {},
                        ).get("data")
                    )

                    break

                elif mime == "text/html":

                    parsed_email["body"] = cls.decode_body(
                        part.get(
                            "body",
                            {},
                        ).get("data")
                    )

        parsed_email["urls"] = cls.extract_urls(
            parsed_email["body"]
        )

        parsed_email["attachments"] = (
            cls.extract_attachments(payload)
        )

        parsed_email["auth_results"] = (
            cls.extract_auth_results(headers)
        )

        return parsed_email