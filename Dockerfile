# Use Python 3.13 as base image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    wget \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create directories for output
RUN mkdir -p output

# Set environment variables
ENV PYTHONPATH=/app
ENV HF_TOKEN=${HF_TOKEN}

# Expose port if needed (optional)
# EXPOSE 8000

# Command to run the application
CMD ["python", "app1.py"]
