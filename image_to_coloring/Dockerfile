FROM python:3.9-slim

# Install necessary system packages
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0

# Install Python dependencies
RUN pip install --no-cache-dir Flask Pillow opencv-python

# Set working directory
WORKDIR /app

# Copy application files
COPY app /app

# Ensure the run.sh file is executable
RUN chmod +x /app/run.sh

# Expose port 5000
EXPOSE 5000

# Run the application using run.sh
CMD ["/app/run.sh"]