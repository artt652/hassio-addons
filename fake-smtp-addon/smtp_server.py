#!/usr/bin/env python3
"""A simple fake SMTP server that forwards messages and images to Telegram."""

import os
import requests
import email
import asyncio
from email import policy
from email.parser import BytesParser
from io import BytesIO
from aiosmtpd.controller import Controller

# Read Telegram Bot Token and Chat ID from environment variables
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Ensure environment variables are set
if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    raise ValueError("Missing Telegram Bot Token or Chat ID environment variables.")


class FakeSMTPHandler:
    """SMTP Handler that processes incoming emails."""

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

        return '250 Message accepted for delivery'

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
                    image_name = part.get_filename() or "unnamed_image.jpg"  # Handle missing filenames
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
    handler = FakeSMTPHandler()
    controller = Controller(handler, hostname='0.0.0.0', port=1025)

    # Start the SMTP server
    controller.start()

    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        controller.stop()