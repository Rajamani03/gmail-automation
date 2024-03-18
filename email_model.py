import base64
# from email.mime.text import MIMEText
from datetime import datetime

class EmailData:
    def __init__(self, message_id, message):
        self.message_id = message_id
        self.from_id = ''
        self.subject = ''
        self.received_date = None
        for header in message.get('payload', {}).get('headers', {}):
            name = header.get('name', '')
            value = header.get('value', '')
            if name == 'From':
                self.from_id = self.parse_from_email(value)
            elif name == 'Subject':
                self.subject = value
            elif name == 'Date':
                self.received_date = self.parse_date(value).replace(tzinfo=None)
        self.message = self.get_message_body(message).strip()
   
    def parse_from_email(self, from_email_string):
        string_parts = from_email_string.split('<')
        return string_parts[1].split('>')[0]
    
    def parse_date(self, date_string):
        index = date_string.find(':')
        if index != -1:
            date_string = date_string[index-14:index+12]
        return datetime.strptime(date_string, "%d %b %Y %H:%M:%S %z")
    
    def get_message_body(self, message):
        payload = message['payload']
        if 'parts' in payload:
            parts = payload['parts']
            for part in parts:
                if part['mimeType'] == 'text/plain':
                    return base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
        return ""


