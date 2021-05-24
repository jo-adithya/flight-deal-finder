from twilio.rest import Client
from dotenv import load_dotenv
import smtplib
import os

load_dotenv()
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
my_email = os.environ.get('EMAIL')
my_password = os.environ.get('PASSWORD')


class NotificationManager:
    def __init__(self):
        self.client = Client(account_sid, auth_token)

    def send_sms(self, message_body):
        self.client.messages.create(
            body=message_body,
            from_=os.environ.get('VIRTUAL_PHONE'),
            to=os.environ.get('PHONE_NUMBER')
        )

