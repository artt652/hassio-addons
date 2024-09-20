#!/usr/bin/env python3
import os
import asyncio
from aiosmtpd.controller import Controller
from aiosmtpd.handlers import Message
import requests
from email import policy
from email.parser import BytesParser
from io import BytesIO

# Get Telegram bot token and chat ID from environment variables
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_DEFAULT_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', 'YOUR_DEFAULT_CHAT_ID')

# Rest of the script remains the same...
#!/usr/bin/env python3
"""A simple fake SMTP server using aiosmtpd that forwards messages and images to Telegram."""

#import asyncio
#from aiosmtpd.controller import Controller
#from aiosmtpd.handlers import Message
#import requests
#from email import policy
#from email.parser import BytesParser
#from io import BytesIO

# Replace these with your Telegram bot token and chat ID
#TELEGRAM_BOT_TOKEN = 'YOUR_BOT_TOKEN'
#TELEGRAM_CHAT_ID = 'YOUR_CHAT_ID'

class CustomSMTPHandler:
    """A custom handler for processing received emails."""
    
    def __init__(self):
        pass

    async def handle_DATA(self, server, session, envelope):
        mailfrom = envelope.mail_from
        rcpttos = envelope.rcpt_tos
        data = envelope.content

        print(f"Received message from: {mailfrom}")
        print(f"Message addressed to: {rcpttos}")

        # Parse the email content
        message = BytesParser(policy=policy.default).parsebytes(data)

        # Extract plain text or HTML content
        body = self.extract_body(message)
        
        # Forward the email body to Telegram
        self.send_to_telegram(mailfrom, rcpttos, body)
        
        # Check and forward any images to Telegram
        self.forward_attachments_to_telegram(message)

        return '250 OK'

    def extract_body(self, message):
        """Extracts plain text or HTML content from the email."""
        body = ""
        if message.is_multipart():
            for part in message.iter_parts():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    body = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8')
                    break
                elif content_type == "text/html" and not body:
                    body = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8')
        else:
            body = message.get_payload(decode=True).decode(message.get_content_charset() or 'utf-8')
        return body

    def forward_attachments_to_telegram(self, message):
        """Extracts attachments from the email and sends any images to Telegram."""
        if message.is_multipart():
            for part in message.iter_attachments():
                content_type = part.get_content_type()
                if content_type.startswith('image/'):
                    image_data = part.get_payload(decode=True)
                    image_name = part.get_filename()
                    self.send_image_to_telegram(image_data, image_name)

    def send_to_telegram(self, mailfrom, rcpttos, body):
        """Send a message to a Telegram chat using the Bot API."""
        message = (
            f"Received message from: {mailfrom}\n"
            f"Message addressed to: {', '.join(rcpttos)}\n"
            f"Message body:\n{body}"
        )

        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message
        }

        try:
            response = requests.post(url, data=payload)
            response.raise_for_status()
            print("Message forwarded to Telegram successfully.")
        except requests.exceptions.RequestException as e:
            print(f"Failed to send message to Telegram: {e}")

    def send_image_to_telegram(self, image_data, image_name):
        """Send an image to a Telegram chat using the Bot API."""
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
        files = {
            'photo': (image_name, BytesIO(image_data))
        }
        payload = {
            'chat_id': TELEGRAM_CHAT_ID
        }

        try:
            response = requests.post(url, files=files, data=payload)
            response.raise_for_status()
            print(f"Image {image_name} forwarded to Telegram successfully.")
        except requests.exceptions.RequestException as e:
            print(f"Failed to send image to Telegram: {e}")

if __name__ == "__main__":
    handler = CustomSMTPHandler()
    controller = Controller(handler, hostname='localhost', port=1025)
    controller.start()

    print("Running fake SMTP server on port 1025. Press Ctrl+C to stop.")
    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        controller.stop()
