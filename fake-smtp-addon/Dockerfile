FROM python:3.10-slim

# Set work directory
WORKDIR /usr/src/app

# Copy files
COPY smtp_server.py .
COPY run.sh .

# Install necessary dependencies
RUN pip install requests
RUN pip install aiosmtpd

# Make the run.sh script executable
RUN chmod +x /usr/src/app/run.sh

# Expose the port for the SMTP server (important for Home Assistant)
EXPOSE 1025

# Run as user "homeassistant" (required for Home Assistant add-ons)
RUN adduser --disabled-password --gecos "" homeassistant
USER homeassistant

# Start the script via run.sh
CMD ["/usr/src/app/run.sh"]