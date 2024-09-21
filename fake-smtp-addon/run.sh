#!/bin/bash

# Export the environment variables from Home Assistant's add-on configuration
export TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN
export TELEGRAM_CHAT_ID=$TELEGRAM_CHAT_ID

# Start the fake SMTP server
python3 /usr/src/app/smtp_server.py