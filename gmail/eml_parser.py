"""
PhishCLI - EML Parser

Parses .eml files into the standard PhishCLI email format.
"""

import re
from email import policy
from email.parser import BytesParser
from urllib.parse import urlparse


class EMLParser:
    """Parses .eml files."""

    URL_REGEX = re.compile(
        r"https?://[^\s<>\"]+",
        re.IGNORECASE,
    )

    @classmethod
    def parse(cls, file_path):
        """
        Parse an .eml file.

        Args:
            file_path (str)

        Returns:
            dict
        """

        with open(file_path, "rb") as fp:

            message = BytesParser(
                policy=policy.default
            ).parse(fp)

        body = cls._extract_body(message)

        parsed_email = {

            "message_id": message.get("Message-ID", ""),

            "sender": message.get("From", ""),

            "from": message.get("From", ""),

            "recipient": message.get("To", ""),

            "to": message.get("To", ""),

            "subject": message.get("Subject", ""),

            "date": message.get("Date", ""),

            "reply_to": message.get("Reply-To", ""),

            "return_path": message.get("Return-Path", ""),

            "body": body,

            "snippet": body[:200],

            "urls": cls.extract_urls(body),

            "attachments": cls.extract_attachments(message),

            "auth_results": cls.extract_auth_results(message),

        }

        return parsed_email

    @staticmethod
    def _extract_body(message):

        if message.is_multipart():

            for part in message.walk():

                content_type = part.get_content_type()

                if content_type == "text/plain":

                    try:

                        return part.get_content()

                    except Exception:

                        continue

        else:

            try:

                return message.get_content()

            except Exception:

                pass

        return ""

    @classmethod
    def extract_urls(cls, body):

        urls = []

        for url in cls.URL_REGEX.findall(body):

            parsed = urlparse(url)

            host = parsed.hostname or ""

            urls.append({

                "raw_url": url,

                "scheme": parsed.scheme,

                "domain": host,

                "has_ip_host": bool(

                    re.fullmatch(

                        r"\d{1,3}(\.\d{1,3}){3}",

                        host,

                    )

                ),

            })

        return urls

    @staticmethod
    def extract_attachments(message):

        attachments = []

        for part in message.iter_attachments():

            attachments.append({

                "filename": part.get_filename(),

                "sha256": None,

                "md5": None,

            })

        return attachments

    @staticmethod
    def extract_auth_results(message):

        auth = message.get(
            "Authentication-Results",
            "",
        ).lower()

        return {

            "spf": (
                "pass"
                if "spf=pass" in auth
                else "fail"
                if "spf=fail" in auth
                else "unknown"
            ),

            "dkim": (
                "pass"
                if "dkim=pass" in auth
                else "fail"
                if "dkim=fail" in auth
                else "unknown"
            ),

            "dmarc": (
                "pass"
                if "dmarc=pass" in auth
                else "fail"
                if "dmarc=fail" in auth
                else "unknown"
            ),

        }