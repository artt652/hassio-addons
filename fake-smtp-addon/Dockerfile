FROM python:3.10-slim

# Set work directory
WORKDIR /usr/src/app

# Copy files
COPY smtp_server.py .
COPY run.sh .

# Install necessary dependencies
RUN pip install requests aiosmtpd

# Make the run.sh executable
RUN chmod +x /usr/src/app/run.sh

# Expose the port for the SMTP server
EXPOSE 1025

# Add environment variables explicitly
ENV TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
ENV TELEGRAM_CHAT_ID=${TELEGRAM_CHAT_ID}

# Start the script
CMD ["/usr/src/app/run.sh"]