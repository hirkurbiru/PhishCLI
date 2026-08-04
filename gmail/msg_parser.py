"""
PhishCLI - MSG Parser

Parses Outlook .msg files into the standard
PhishCLI email format.
"""

import re
from urllib.parse import urlparse

import extract_msg


class MSGParser:

    URL_REGEX = re.compile(
        r"https?://[^\s<>\"]+",
        re.IGNORECASE,
    )

    @classmethod
    def parse(cls, file_path):

        msg = extract_msg.Message(file_path)

        body = msg.body or ""

        parsed_email = {

            "message_id": "",

            "sender": msg.sender or "",

            "from": msg.sender or "",

            "recipient": msg.to or "",

            "to": msg.to or "",

            "subject": msg.subject or "",

            "date": str(msg.date) if msg.date else "",

            "reply_to": "",

            "return_path": "",

            "body": body,

            "snippet": body[:200],

            "urls": cls.extract_urls(body),

            "attachments": cls.extract_attachments(msg),

            "auth_results": {

                "spf": "unknown",

                "dkim": "unknown",

                "dmarc": "unknown",

            },

        }

        return parsed_email

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

                "has_ip_host": False,

            })

        return urls

    @staticmethod
    def extract_attachments(msg):

        attachments = []

        for attachment in msg.attachments:

            attachments.append({

                "filename": attachment.longFilename
                or attachment.shortFilename,

                "sha256": None,

                "md5": None,

            })

        return attachments