# Stage 1: Builder
FROM python:3.10-alpine AS builder

WORKDIR /app

# Install system dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-dev \
    libpq \
    python3-dev \
    libc-dev \
    linux-headers

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Final Image
FROM python:3.10-alpine

WORKDIR /app

# Install system dependencies again
RUN apk add --no-cache \
    postgresql-dev \
    libpq

# Copy installed dependencies from builder stage
COPY --from=builder /install /usr/local

# Copy project files
COPY . .

# Expose port for Gunicorn
EXPOSE 10000

# Run migrations & start the application
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn task_manager.wsgi:application --bind 0.0.0.0:10000"]
