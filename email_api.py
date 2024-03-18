import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from email.mime.text import MIMEText
from email_model import EmailData
   
class EmailAPI:
    # If modifying these scopes, delete the file token.json.
    SCOPES = ["https://www.googleapis.com/auth/gmail.readonly", "https://www.googleapis.com/auth/gmail.modify"]
    def __init__(self):
        self.creds = None

        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            self.creds = Credentials.from_authorized_user_file("token.json", self.SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", self.SCOPES
                )
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(self.creds.to_json())

        try:
            # Call the Gmail API
            self.service = build("gmail", "v1", credentials=self.creds)
        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f"An error occurred: {error}")

    def get_all_emails(self):
        try:
            # Call the Gmail API to fetch emails
            results = self.service.users().messages().list(userId='me').execute()
            messages = results.get('messages', [])
            return messages
        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f"An error occurred: {error}")

    def get_email_data(self, message):
        try:
            result = self.service.users().messages().get(userId='me', id=message['id']).execute()
            return EmailData(message['id'], result)
        except HttpError as error:
            print(f"An error occurred: {error}")

    def mark_as_read(self, message_id):
        # Create modify request body to remove the UNREAD label
        modify_request_body = {
            'removeLabelIds': ['UNREAD']
        }
        try:
            # Call the Gmail API to modify the message
            self.service.users().messages().modify(userId='me', id=message_id, body=modify_request_body).execute()
        except HttpError as error:
            print(f"An error occurred: {error}")

    def mark_as_unread(self, message_id):
        # Create modify request body to add the UNREAD label
        modify_request_body = {
            'addLabelIds': ['UNREAD']
        }
        try:
            # Call the Gmail API to modify the message
            self.service.users().messages().modify(userId='me', id=message_id, body=modify_request_body).execute()
        except HttpError as error:
            print(f"An error occurred: {error}")

    def move_email(self, message_id, destination):
        # Create modify request body to add the destination label
        modify_request_body = {
            'addLabelIds': [destination]
        }
        try:
            # Call the Gmail API to modify the message
            self.service.users().messages().modify(userId='me', id=message_id, body=modify_request_body).execute()
        except HttpError as error:
            print(f"An error occurred: {error}")
            