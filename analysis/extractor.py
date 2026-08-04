"""
PhishCLI - Raw MIME & Header Extractor

Parses raw MIME structures, extracts canonical headers,
embedded URLs, authentication results, and attachment metadata.
"""

import hashlib
import re
import urllib.parse
from email import policy
from email.header import decode_header, make_header
from email.message import EmailMessage
from email.parser import BytesParser
from typing import Any, Dict, List, Tuple, cast

from config.logging_config import logger
from utils.exceptions import IngestionError


class EmailExtractor:
    """Extracts structured entities from raw email MIME streams."""

    URL_REGEX = re.compile(
        r"https?://[^\s\"'<>()]+",
        re.IGNORECASE,
    )

    IPV4_REGEX = re.compile(
        r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
    )

    @classmethod
    def parse_raw_bytes(cls, raw_bytes: bytes) -> Dict[str, Any]:
        """
        Parse raw .eml bytes into a structured dictionary.
        """

        try:
            msg = BytesParser(policy=policy.default).parsebytes(raw_bytes)
            
           

        except Exception as e:
            logger.exception("Unable to parse raw email bytes.")
            raise IngestionError(
                "Corrupted or invalid email stream.",
                details=str(e),
            ) from e

        subject = cls._decode_header(msg.get("Subject"))
        sender = cls._decode_header(msg.get("From"))
        recipient = cls._decode_header(msg.get("To"))
        reply_to = cls._decode_header(msg.get("Reply-To"))
        return_path = cls._decode_header(msg.get("Return-Path"))
        message_id = cls._decode_header(msg.get("Message-ID"))
        date_sent = cls._decode_header(msg.get("Date"))

        raw_headers = {
            key: str(value)
            for key, value in msg.items()
        }

        auth_results = cls._parse_authentication_results(msg)

        body_text, body_html = cls._extract_bodies(msg)

        urls = cls.extract_urls(
            f"{body_text}\n{body_html}"
        )

        attachments = cls._extract_attachments(msg)

        return {
            "message_id": message_id,
            "subject": subject,
            "sender": sender,
            "recipient": recipient,
            "reply_to": reply_to,
            "return_path": return_path,
            "date_sent": date_sent,
            "body_text": body_text,
            "body_html": body_html,
            "raw_headers": raw_headers,
            "auth_results": auth_results,
            "urls": urls,
            "attachments": attachments,
        }

    @staticmethod
    def _decode_header(value: Any) -> str:
        """
        Decode MIME encoded headers safely.
        """

        if value is None:
            return ""

        try:
            return str(
                make_header(
                    decode_header(str(value))
                )
            )

        except Exception:
            return str(value)

    @classmethod
    def _extract_bodies(
        cls,
        msg: EmailMessage,
    ) -> Tuple[str, str]:

        body_text = ""
        body_html = ""

        if msg.is_multipart():

            for part in msg.walk():

                if part.is_multipart():
                    continue

                disposition = (
                    part.get_content_disposition()
                )

                if disposition == "attachment":
                    continue

                content_type = part.get_content_type()

                payload = cast(bytes | None, part.get_payload(decode=True))

                if payload is None:
                    continue

                charset = (
                    part.get_content_charset()
                    or "utf-8"
                )

                try:
                    if isinstance(payload, bytes):
                        decoded = payload.decode(
                            charset,
                            errors="replace",
                        )
                    else:
                        decoded = str(payload)

                except Exception:
                    decoded = (
                        payload.decode("utf-8", errors="replace")
                        if isinstance(payload, (bytes, bytearray))
                        else str(payload)
                    )

                if content_type == "text/plain":
                    body_text += decoded + "\n"

                elif content_type == "text/html":
                    body_html += decoded + "\n"

        else:

            payload = cast(bytes | None, msg.get_payload(decode=True))

            if payload is not None:

                charset = (
                    msg.get_content_charset()
                    or "utf-8"
                )

                try:
                    if isinstance(payload, bytes):
                        decoded = payload.decode(charset, errors="replace")
                    else:
                        decoded = str(payload)

                except Exception:
                    decoded = (
                        payload.decode("utf-8", errors="replace")
                        if isinstance(payload, (bytes, bytearray))
                        else str(payload)
                    )

                if msg.get_content_type() == "text/plain":
                    body_text = decoded

                elif msg.get_content_type() == "text/html":
                    body_html = decoded

        return body_text.strip(), body_html.strip()

    @classmethod
    def extract_urls(
        cls,
        text: str,
    ) -> List[Dict[str, Any]]:

        found = cls.URL_REGEX.findall(text)

        unique = sorted(set(found))

        urls = []

        for url in unique:

            cleaned = url.rstrip(".,);\"'")

            try:
                parsed = urllib.parse.urlparse(cleaned)

                domain = parsed.hostname or ""

                urls.append(
                    {
                        "raw_url": cleaned,
                        "scheme": parsed.scheme,
                        "domain": domain,
                        "path": parsed.path,
                        "query": parsed.query,
                        "has_ip_host": bool(
                            cls.IPV4_REGEX.fullmatch(domain)
                        ),
                    }
                )

            except Exception:
                continue

        return urls

    @classmethod
    def _extract_attachments(
        cls,
        msg: EmailMessage,
    ) -> List[Dict[str, Any]]:

        attachments = []

        for part in msg.walk():

            filename = part.get_filename()

            disposition = (
                part.get_content_disposition()
            )

            if disposition != "attachment" and not filename:
                continue

            payload = part.get_payload(decode=True)

            if not payload:
                continue

            filename = filename or "unnamed_attachment"
            # Ensure payload is bytes for hashing (get_payload may return str in some policies)
            if isinstance(payload, (bytes, bytearray)):
                payload_bytes = bytes(payload)
            else:
                payload_bytes = str(payload).encode("utf-8")

            attachments.append(
                {
                    "filename": filename,
                    "content_type": part.get_content_type(),
                    "size_bytes": len(payload_bytes),
                    "sha256": hashlib.sha256(payload_bytes).hexdigest(),
                    "md5": hashlib.md5(payload_bytes).hexdigest(),
                }
            )

        return attachments

    @classmethod
    def _parse_authentication_results(
        cls,
        msg: EmailMessage,
    ) -> Dict[str, str]:

        auth = (
            str(
                msg.get(
                    "Authentication-Results",
                    "",
                )
            )
            .lower()
        )

        results = {
            "spf": "neutral",
            "dkim": "neutral",
            "dmarc": "neutral",
        }

        if "spf=pass" in auth:
            results["spf"] = "pass"

        elif (
            "spf=fail" in auth
            or "spf=softfail" in auth
        ):
            results["spf"] = "fail"

        if "dkim=pass" in auth:
            results["dkim"] = "pass"

        elif "dkim=fail" in auth:
            results["dkim"] = "fail"

        if "dmarc=pass" in auth:
            results["dmarc"] = "pass"

        elif "dmarc=fail" in auth:
            results["dmarc"] = "fail"

        return results