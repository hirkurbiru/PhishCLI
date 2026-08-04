"""
PhishCLI - Gmail Fetcher

Fetches and searches Gmail messages.
"""

from googleapiclient.errors import HttpError

from gmail.gmail_service import GmailService

from config.logging_config import logger
from utils.exceptions import GmailError


class GmailFetcher:
    """Fetches emails from Gmail."""

    def __init__(self):
        self.service = GmailService.get_service()

    # ==========================================================
    # Fetch Messages
    # ==========================================================

    def get_latest_messages(self, max_results=10):
        """
        Fetch Gmail messages.

        Args:
            max_results (int):
                Number of emails to fetch.
                Use -1 to fetch the entire inbox.

        Returns:
            list
        """

        try:

            # --------------------------------------------------
            # Entire Inbox
            # --------------------------------------------------

            if max_results == -1:
                messages = []
                page_token = None
                page = 1

                while True:
                    response = (
                        self.service.users()
                        .messages()
                        .list(
                            userId="me",
                            maxResults=500,
                            pageToken=page_token,
                        )
                        .execute()
                    )

                    current_messages = response.get(
                        "messages",
                        [],
                    )

                    messages.extend(current_messages)

                    page_token = response.get("nextPageToken")
                    if not page_token:
                        break

                    page += 1

                return messages

            # --------------------------------------------------
            # Limited Emails
            # --------------------------------------------------

            response = (
                self.service.users()
                .messages()
                .list(
                    userId="me",
                    maxResults=max_results,
                )
                .execute()
            )

            return response.get(
                "messages",
                [],
            )

        except HttpError as e:

            logger.error(f"Gmail API error: {e}")

            raise GmailError(
                "Unable to fetch Gmail emails.",
                details=str(e),
            )

        except Exception as e:

            logger.error(f"Gmail connection error: {e}")

            raise GmailError(
                "Unable to connect to Gmail.",
                details=str(e),
            )

    # ==========================================================
    # Fetch One Message
    # ==========================================================

    def get_message(self, message_id):
        """
        Fetch a complete Gmail message.
        """

        try:

            return (
                self.service.users()
                .messages()
                .get(
                    userId="me",
                    id=message_id,
                    format="full",
                )
                .execute()
            )

        except HttpError as e:

            logger.error(f"Gmail API error: {e}")

            raise GmailError(
                "Unable to retrieve email.",
                details=str(e),
            )

        except Exception as e:

            logger.error(f"Gmail connection error: {e}")

            raise GmailError(
                "Unable to retrieve email.",
                details=str(e),
            )

    # ==========================================================
    # Header Extraction
    # ==========================================================

    @staticmethod
    def _extract_headers(full_msg):
        """
        Extract sender, subject and date.
        """

        headers = full_msg["payload"].get(
            "headers",
            [],
        )

        sender = ""
        subject = ""
        date = ""

        for header in headers:

            if header["name"] == "From":

                sender = header["value"]

            elif header["name"] == "Subject":

                subject = header["value"]

            elif header["name"] == "Date":

                date = header["value"]

        return {

            "sender": sender,

            "subject": subject,

            "date": date,

        }

    # ==========================================================
    # Email List
    # ==========================================================

    def get_email_list(self, max_results=10):
        """
        Returns email metadata.
        """

        messages = self.get_latest_messages(
            max_results
        )

        email_list = []

        for msg in messages:

            full_msg = self.get_message(
                msg["id"]
            )

            headers = self._extract_headers(
                full_msg
            )

            email_list.append(
                {

                    "id": msg["id"],

                    "sender": headers["sender"],

                    "subject": headers["subject"],

                    "date": headers["date"],

                }
            )

        return email_list

    # ==========================================================
    # Gmail Search
    # ==========================================================

    def search_messages(self, query, max_results=10):
        """
        Search Gmail using Gmail search operators.
        """

        try:

            response = (
                self.service.users()
                .messages()
                .list(
                    userId="me",
                    q=query,
                    maxResults=max_results,
                )
                .execute()
            )

            return response.get(
                "messages",
                [],
            )

        except HttpError as e:

            logger.error(f"Gmail API error: {e}")

            raise GmailError(
                "Unable to search Gmail.",
                details=str(e),
            )

        except Exception as e:

            logger.error(f"Gmail connection error: {e}")

            raise GmailError(
                "Unable to search Gmail.",
                details=str(e),
            )

    # ==========================================================
    # Search Email List
    # ==========================================================

    def search_email_list(self, query, max_results=10):
        """
        Returns formatted search results.
        """

        messages = self.search_messages(
            query,
            max_results,
        )

        email_list = []

        for msg in messages:

            full_msg = self.get_message(
                msg["id"]
            )

            headers = self._extract_headers(
                full_msg
            )

            email_list.append(
                {

                    "id": msg["id"],

                    "sender": headers["sender"],

                    "subject": headers["subject"],

                    "date": headers["date"],

                }
            )

        return email_list