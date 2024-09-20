#!/bin/bash

# Export the options from Home Assistant configuration
export TELEGRAM_BOT_TOKEN="${TELEGRAM_BOT_TOKEN}"
export TELEGRAM_CHAT_ID="${TELEGRAM_CHAT_ID}"

# Run the Python SMTP server
python3 /usr/src/app/smtp_server.py