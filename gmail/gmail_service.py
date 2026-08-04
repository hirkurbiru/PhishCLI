from googleapiclient.discovery import build

from gmail.gmail_auth import GmailAuthenticator


class GmailService:
    """Creates an authenticated Gmail API service."""

    @staticmethod
    def get_service():
        creds = GmailAuthenticator.authenticate()
        service = build("gmail", "v1", credentials=creds)
        return service