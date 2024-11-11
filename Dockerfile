# Base image
FROM python:3.9-slim

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt into the container
COPY requirements.txt /app/

# Update pip
RUN pip install --upgrade pip

# Install the project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the Django project into the container
COPY . /app/

# Copy the entrypoint.sh script into the container
COPY entrypoint.sh /app/

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Expose the port Gunicorn will run on
EXPOSE 8000

## Set the entrypoint to the entrypoint.sh script
ENTRYPOINT ["/app/entrypoint.sh"]
