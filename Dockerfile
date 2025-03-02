# Use lightweight Python image
FROM python:3.10-alpine

# Set working directory
WORKDIR /app

# Install system dependencies required for PostgreSQL
RUN apk add --no-cache gcc musl-dev postgresql-dev

# Copy requirements.txt separately to improve caching
COPY requirements.txt .

# Upgrade pip before installing dependencies
RUN pip install --upgrade pip

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Copy wait-for-it script to container
COPY wait-for-it.sh /wait-for-it.sh

# Copy entrypoint script to container
COPY entrypoint.sh /entrypoint.sh

# Make the wait-for-it script executable
RUN chmod +x /wait-for-it.sh /entrypoint.sh


# Use entrypoint script to wait for DB and start the app
ENTRYPOINT ["/entrypoint.sh"]