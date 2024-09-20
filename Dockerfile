# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables to prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN pip install --no-cache-dir aiosmtpd requests

# Set the working directory inside the container
WORKDIR /app

# Copy the script into the container
COPY fake_smtp.py /app/fake_smtp.py

# Expose port 1025 for SMTP
EXPOSE 1025

# Run the script
CMD ["python3", "/app/fake_smtp.py"]

ENV TELEGRAM_BOT_TOKEN="your_bot_token"
ENV TELEGRAM_CHAT_ID="your_chat_id"
